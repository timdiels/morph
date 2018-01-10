# Copyright (C) 2015, 2016 VIB/BEG/UGent - Tim Diels <timdiels.m@gmail.com>
#
# This file is part of MORPH.
#
# MORPH is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MORPH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with MORPH.  If not, see <http://www.gnu.org/licenses/>.

'''
Application programmer interface (API)
'''

import logging

from pytil.various import join_multiline
from varbio import clean, parse
from varbio.correlation import pearson_df
import attr
import pandas as pd
import yaml


# Note: if performance is an issue, profile the code to find the bottleneck. If
# pandas is the problem, (partly) use numpy instead. Note that
# varbio.correlation also has `pearson`, the plain numpy equivalent of
# `pearson_df`.

_logger = logging.getLogger(__name__)

def morph(config):
    '''
    Run MORPH.

    Parameters
    ----------
    config : ~typing.Dict
        Union of config.yaml and run_config.yaml. See user documentation.

    Returns
    -------
    ~typing.Iterable[Result]
        The result of each matrix, clustering, bait group combination.
    '''
    # Note: we do not to modify config, that would surprise the user of this
    # function.

    _logger.info(join_multiline('''
        For each expression matrix and clustering combination, baits missing
        from either are temporarily excluded. The excluded baits are also
        excluded from the AUSR calculation.
    '''))

    min_genes_present = 8
    top_k = _get_top_k(config)
    bait_groups_by_species = _tidy_grouped_bait_groups(config)
    for species_name, bait_groups in bait_groups_by_species.items():
        species_info = config['species'][species_name]
        _logger.info('Ranking {!r} bait groups'.format(species_name))
        for matrix_name, matrix_info in species_info['expression_matrices'].items():
            with open(matrix_info['path']) as f:
                matrix = parse.expression_matrix(clean.plain_text(f))
            clusterings = _parse_clusterings(matrix_info['clusterings'])
            for group_id, group in bait_groups.items():
                group_name = group['name']
                baits = group['genes']
                baits_in_matrix = matrix.index.intersection(baits)
                correlations = pearson_df(matrix, matrix.loc[baits_in_matrix])
                for clustering_name, clustering in clusterings.items():
                    baits_in_both = clustering.index.intersection(baits_in_matrix)

                    # Skip if not enough baits left
                    log_prefix = '{!r}: {!r}: {!r}:'.format(matrix_name, group_name, clustering_name)
                    baits_present_msg = '{} {}/{} baits present in matrix and clustering.'.format(log_prefix, len(baits_in_both), len(baits))
                    missing_baits = baits_in_both.difference(baits_in_both)
                    if len(baits_in_both) < min_genes_present:
                        skip_reason = 'need at least {} baits present'.format(min_genes_present)
                        _logger.info('{} Skipping; {}'.format(baits_present_msg, skip_reason))
                        yield Result(
                            group_id, group_name, matrix_name, clustering_name,
                            baits_in_both, missing_baits, ranking=None,
                            ausr=None, skip_reason=skip_reason
                        )
                        continue

                    #
                    _logger.info('{} Calculating'.format(baits_present_msg))
                    ranking, ausr = _rank_genes(correlations[baits_in_both], clustering, baits_in_both)
                    _logger.info('{} AUSR={}'.format(log_prefix, ausr))
                    yield Result(
                        group_id, group_name, matrix_name, clustering_name,
                        baits_in_both, missing_baits, ranking.iloc[:top_k],
                        ausr, skip_reason=None
                    )

@attr.s(frozen=True, slots=True)
class Result:

    '''
    MORPH result.

    Attributes
    ----------
    bait_group_id : str
        Bait group identifier.
    bait_group_name : str
        Bait group identifier.
    matrix_name : str
        Expression matrix name.
    clustering_name : str
        Clustering name.
    present_baits : ~typing.Collection[str]
        Baits (after mapping) present in both expression matrix and clustering.
    missing_baits : ~typing.Collection[str]
        Baits (after mapping) missing from expression matrix or clustering.
        Complement of ``present_baits``.
    ranking : pd.Series or None
        Top k ranked genes sorted from best to worst score. Series with gene
        names as index and normalised scores as values. Or `None` if this
        combination (bait group, matrix and clustering) was skipped.
    ausr : float or None
        AUSR of the ranking. Or `None` if this combination was skipped.
    skip_reason : str or None
        Reason the combination was skipped or `None` if it wasn't skipped.
    '''

    bait_group_id = attr.ib()
    bait_group_name = attr.ib()
    matrix_name = attr.ib()
    clustering_name = attr.ib()
    present_baits = attr.ib()
    missing_baits = attr.ib()
    ranking = attr.ib()
    ausr = attr.ib()
    skip_reason = attr.ib()

def _rank_genes(correlations, clustering):
    '''
    Rank genes by correlations and clustering.

    Parameters
    ----------
    correlations : ~pandas.DataFrame
        Correlations between baits and all genes in expression matrix. Column
        names are baits, index names are all genes.
    clustering : ~pandas.Series
        Clustering as series with gene names as index, cluster names as values
        and ``cluster`` as series name.

    Returns
    -------
    ~typing.Tuple[pandas.Series, float]
        Ranking and its AUSR.
    '''
    # Take only row genes present in clustering and add 'cluster' column
    original_row_count = len(correlations)
    correlations = correlations.join(clustering, how='inner')
    dropped_rows = original_row_count - len(correlations)
    if dropped_rows:
        _logger.info(join_multiline(
            '''
            Ignoring {}/{} rows from expression matrix because the corresponding
            genes do not appear in the clustering.
            '''
            .format(dropped_rows, original_row_count)
        ))

    # Calculate ranking
    pre_ranking = []
    ranking = []
    for _, corrs in correlations.groupby('cluster'):
        corrs = corrs.drop('cluster', axis=1)
        cluster_baits = corrs.columns.intersection(corrs.index).to_series()  # baits in cluster
        if not cluster_baits.empty: # only clusters with baits
            pre_ranking.append(corrs[cluster_baits].sum(axis=1))
            ranking.append(_finalise(pre_ranking[-1], cluster_baits))
    pre_ranking = pd.concat(pre_ranking)
    ranking = pd.concat(ranking)

    # For each bait, leave it out, calculate ranking based on pre_ranking
    # and check its position in the ranking
    tmp_ranking = pre_ranking.copy()
    indices = []
    for _, corrs in correlations.groupby('cluster'):
        corrs = corrs.drop('cluster', axis=1)
        cluster_baits = corrs.columns.intersection(corrs.index).to_series()  # baits in cluster
        if not cluster_baits.empty:
            for bait in cluster_baits:
                tmp_ranking.loc[corrs.index] = pre_ranking.loc[corrs.index] - corrs[bait]
                _finalise(tmp_ranking.loc[corrs.index], cluster_baits.drop(bait))
                tmp_ranking.sort_values(inplace=True)
                indices.append(tmp_ranking.index.get_loc(bait))
            tmp_ranking = pre_ranking.copy()

    # Apply area under the curve to indices to get the AUSR
    ausr = _get_auc(pd.Series(indices))

    return ranking, ausr

def _normalise(ranking):
    return (ranking - ranking.values.mean()) / ranking.values.std()

def _finalise(ranking, baits):
    '''
    Finalise ranking, see _rank_genes.

    Parameters
    ----------
    ranking : pandas.Series
    baits : ~pandas.Series
        Series with bait gene names as values.
    '''
    non_baits = ~ranking.index.isin(baits)
    ranking = ranking.loc[non_baits]
    if not ranking.empty:
        ranking = ranking / len(baits)
        ranking = _normalise(ranking)
    return ranking

def _get_auc(indices):
    # TODO warn if there are fewer than 1000?
    return indices[indices < 1000].sum() / (1000 * len(indices))

def _tidy_grouped_bait_groups(config):
    _logger.debug('Tidying bait groups')
    return {
        species_name: _tidy_bait_groups(config, species_name, bait_groups)
        for species_name, bait_groups in config['bait_groups'].items()
    }

def _tidy_bait_groups(config, species_name, bait_groups):
    def parse_gene_mapping_or_default():
        if gene_mapping_path:
            with gene_mapping_path.read() as f:
                return yaml.load(f)
        else:
            return {}

    def drop_duplicates_and_map_names(gene_mapping):
        def map_genes(genes):
            return {
                mapped_gene
                for gene in genes
                for mapped_gene in gene_mapping.get(gene, (gene,))
            }
        def map_group(group):
            group = group.copy()
            group['genes'] = map_genes(group['genes'])
            return group
        return {
            group_id: map_group(group)
            for group_id, group in bait_groups.items()
        }

    gene_mapping_path = config['species'][species_name].get('gene_mapping')
    gene_mapping = parse_gene_mapping_or_default(gene_mapping_path)
    return drop_duplicates_and_map_names(gene_mapping)

def _get_top_k(config):
    top_k = config['top_k']
    if not isinstance(top_k, int):
        raise ValueError('top_k must be an int >=1. Got: {!r}'.format(top_k))
    if top_k < 1:
        raise ValueError('top_k must be >=1. Got: {!r}'.format(top_k))

def _parse_clusterings(clusterings):
    '''
    Parse clustering files.

    Parameters
    ----------
    clusterings : ~typing.Mapping[str, str]
        Mapping of clustering names to paths.

    Returns
    -------
    ~typing.Mapping[str, ~pandas.Series]
        Mapping of clustering names to clustering series. Each series has gene
        names as index, cluster names as values and ``cluster`` as series name.
    '''
    return {
        name: _parse_clustering(path)
        for name, path in clusterings.items()
    }

def _parse_clustering(path):
    with open(path) as f:
        clustering = parse.clustering(clean.plain_text(f))
        df = pd.DataFrame(
            (
                (gene, cluster_name)
                for cluster_name, cluster in clustering.items()
                for gene in cluster
            ),
            columns=('gene', 'cluster')
        )
        return df.set_index('gene')['cluster']
