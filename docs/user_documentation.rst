User documentation
==================

MORPH is an algorithm for revealing missing genes in biological pathways or
other groups of related genes; using gene expression data and gene clusterings.
MORPH can be run through the `website`_, on the command line or from Python
using the API.

Preparing clusterings and expression matrices
---------------------------------------------
TODO how to generate clusterings and exp mats. Consider adding scripts to do so
to the repo. Describe expected clustering and expression matrix format.

If genes have multiple names, choose a canonical name per gene. Each clustering
and expression matrix must refer to genes by their canonical name. Bait sets can
use other names so long as a mapping file is provided.

config.yaml
-----------
The config.yaml file passed to --config lists the species, their expression
matrices and per matrix the clusterings it should be combined with. For example::

    species:
        Arabidopsis:
            gene_pattern: 'AT[0-9]G[0-9]{5}'
            expression_matrices:
                Seed GH:
                    path: /mnt/data/seed_gh.txt
                    clusterings:
                        PPI matisse: /mnt/data/seed_gh_ppi_matisse.txt
                        CLICK: /mnt/data/seed_gh_click.txt
                        IsEnzyme: /mnt/data/seed_gh_is_enzyme.txt

The example lists a single species, species names must be unique. The ``name``,
``gene_pattern`` and ``expression_matrices`` attributes are required.
``gene_pattern`` is a regex pattern in Perl syntax that matches all genes of the
species; this is used to determine which species a gene belongs to.
``expression_matrices`` lists the expression matrices available to the species.
You must list at least 1. Each expression matrix contains a subset of the
species' genes as row indices and shouldn't contain genes of any other species.
You must specify the path and a name. Each expression matrix must list at least
one clustering. The clustering must have a path and a name. When running MORPH,
each matrix is tried along with each of the matrix' clusterings. E.g.::

    expression_matrices:
        Seed GH:
            path: /mnt/data/seed_gh.txt
            clusterings:
                PPI matisse: /mnt/data/seed_gh_ppi_matisse.txt
                IsEnzyme: /mnt/data/seed_gh_is_enzyme.txt
        Root:
            path: data_sets/root.txt
            clusterings:
                CLICK: /mnt/data/root_gh_click.txt
                IsEnzyme: /mnt/data/root_gh_is_enzyme.txt

will combine ``Seed GH`` with ``PPI matisse`` and its ``IsEnzyme``, and combine
``Root`` with ``CLICK`` and its ``IsEnzyme``. All paths must be absolute.

Optionally ``gene_descriptions`` can be specified on a species. This is a path
to a YAML file listing the gene name in the first column and
its description in the second column. E.g.::

    AT5G07842: conserved peptide upstream open reading frame 16
    AT5G05200: Protein kinase superfamily protein
    AT4G18197: purine permease 7

Optionally ``gene_mapping`` can be specified on a species. This is a path to a
YAML file without header which lists gene names to map from in the first column
and canonical gene names to map to in the second column. Remember, clusterings and
matrices may only use canonical gene names. E.g.::

    loc_os07g36740: ['os07g0553300']
    loc_os03g14130: ['os03g0245200', 'os03g0245201']
    loc_os11g47780.1: ['os11g0704100']
    loc_os08g25490.1: ['os08g0343600']
    loc_os05g41230.1: ['os05g0491400']

This allows specifying baits both as ``loc*`` and ``os*`` genes. ``loc*`` baits
are replaced with their ``os*`` counterpart. A gene name can map to multiple
names.

run_config.yaml
---------------
The run config file passed to --run-config lists the bait groups to use and the
number of genes to include in each ranking. E.g.::

    top_k: 10
    bait_groups:
        Arabidopsis:
            pathway1:  # pathway identifier, must be alphanumeric, may also contain underscores
                name: Pathway 1  # Human readable name
                genes
                    - gene1
                    - gene2
        Rice:
            other_pathway:
                name: Other pathway
                genes: ['gene2', 'gene3']
            another_pathway:
                name: Another pathway
                genes: ['gene5']

All the above are required. ``top_k`` specifies the number of genes to output in
each ranking (at least 1). ``bait_groups`` lists the groups of bait genes to run
MORPH on grouped by species. All genes in a group must be of the species the
group is listed in. The species must match the species names in ``config.yaml``.
In the above example, ``pathway1`` is the identifier of a baits group, ``Pathway
1`` is its human readable name. It contains 2 bait genes ``gene1`` and
``gene2``, both are Arabidopsis genes.

API
---
For example::

    from morphbio.algorithm import morph
    for result in morph({'species': ..., 'baits_groups': ...}):  # same as union of config YAML files
        pass  # use or write out resulting rankings

.. _website: http://bioinformatics.psb.ugent.be/webtools/morph/
