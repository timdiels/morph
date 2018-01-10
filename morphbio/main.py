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
Command line interface (CLI)
'''

from pathlib import Path
from textwrap import dedent
import logging

from pytil import logging as logging_
import click
import pandas as pd
import yaml

from morphbio import __version__
from morphbio.algorithm import morph


_logger = logging.getLogger(__name__)

@click.command()
@click.version_option(__version__)
@click.option(  # For things which don't change often
    '--config', 'config_file',
    required=True,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help='Configuration YAML file, see config.yaml in the documentation.'
)
@click.argument(  # For things which often change between runs
    '--run_config', 'run_config_file',
    required=True,
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    help='Run config YAML file, see run_config.yaml in the documentation.'
)
@click.option(
    '-o', '--output', 'output_dir',
    required=True,
    show_default=True,
    default='.',
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help='Output directory'
)
def main(config_file, run_config_file, output_dir):
    '''
    Run MORPH.

    For example:

    \b
        morph --config config.yaml --run-config run_config.yaml --output output
    '''
    logging_.configure(output_dir / 'morph.log')

    # Parse
    _logger.info('')
    config_file = Path(config_file)
    run_config_file = Path(run_config_file)
    output_dir = Path(output_dir)
    with config_file.open() as f:
        config = yaml.load(f)
    with run_config_file.open() as f:
        config.update(yaml.load(f))

    # Run alg
    results = pd.DataFrame(
        (
            (result.bait_group, result.ausr, result)
            for result in morph(config)
        ),
        columns=('bait_group_id', 'ausr', 'result')
    )

    # Write best result per bait group to output directory
    rankings_dir = output_dir / 'rankings'
    rankings_dir.mkdir()
    for bait_group_id, group in results.groupby('bait_group_id'):
        output_file = rankings_dir / '{}.txt'.format(bait_group_id)
        best_index = group['ausr'].idxmax()
        if pd.isnull(best_index):
            # Note: All combinations were skipped, no results
            best_result = group.iloc[0]
            _write_result_txt(
                output_file,
                ausr='NA',
                bait_group_name=best_result.bait_group_name,
                matrix_name='NA',
                clustering_name='NA',
                present_baits=best_result.present_baits,
                missing_baits=best_result.missing_baits,
                ausr_stats='NA',
                ranking='NA'
            )
        else:
            best_result = group.iloc[best_index]
            _write_result_txt(
                output_file,
                best_result.ausr,
                best_result.bait_group_name,
                best_result.matrix_name,
                best_result.clustering_name,
                best_result.present_baits,
                best_result.missing_baits,
                ausr_stats=group['ausr'].describe().to_string(),
                ranking=best_result.ranking.to_string()
            )
        # TODO also write YAML

    # Write overview of best AUSRs
    overview_file = output_dir / 'overview.txt'
    _logger.info('Writing overview of results to {}'.format(overview_file))
    with overview_file.open('w') as f:
        best_ausrs = results.groupby('bait_group_id')['ausr'].max()  #TODO this might filter out all NA groups
        best_ausrs.sort_values(inplace=True, ascending=False)
        f.write(dedent('''
            Statistics of best AUSRs:
            {}
            
            List of best AUSRs:
            {}
            ''').strip().format(
                best_ausrs.describe().to_string(), # TODO consider how NA affects the stats
                best_ausrs.to_string(header=False)
            )
        )

def _write_result_txt(output_file, ausr, bait_group_name, matrix_name, clustering_name, present_baits, missing_baits, ausr_stats, ranking):
    _logger.info('Writing result to {}'.format(output_file))
    present_baits = sorted(present_baits)
    missing_baits = sorted(missing_baits)
    with output_file.open('w') as f:
        f.write(dedent('''
            AUSR: {}
            Bait group: {}
            Expression matrix used: {}
            Clustering used: {}
            Baits present in both ({}): {}
            Baits missing ({}): {}
            
            Statistics of AUSRs of other rankings of same bait group:
            {}
            
            Candidates:
            {}
            ''').strip().format(
                ausr,
                bait_group_name,
                matrix_name,
                clustering_name,
                len(present_baits),
                ' '.join(present_baits),
                len(missing_baits), 
                ' '.join(missing_baits),
                ausr_stats,
                ranking
            )
        )
