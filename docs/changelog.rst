Changelog
=========
`Semantic versioning`_ is used. When depending on this project,
pin the major version, e.g. ``install_requires =
['morphbio==2.*']``.

2.0.0
-----
First release of the Python implementation.

TODO compare differences in output to C++, the one installed on server.

Backwards incompatible changes:

- CLI: change::

      morph path/to/config.yaml path/to/joblist.yaml path/to/output_directory top_k [--output-yaml]

  to::

      morph --config path/to/config.yaml --run-config path/to/run_config.yaml --output path/to/output_directory

  and always output both txt and YAML.

- ``config.yaml``:

  - Remove ``data_path`` and ``species_data_path``. All ``path`` must be absolute.
  - List species, matrices and clusterings as dicts by name instead of lists.

- Replace ``joblist.yaml`` and ``top_k`` argument with ``run_config.yaml``.

- Gene descriptions file must be YAML file::

      gene: desc
      gene2: desc2

  instead of previously::

      gene\tdesc
      gene2\tdesc2

- Gene mappings file must be YAML file::

      gene: ['target1', 'target2']
      gene2: ['target3']

  instead of previously::

      gene\ttarget
      gene\ttarget2
      gene2\ttarget3

Enhancements and additions:

- Add documentation

- Add morph.log to output

- Print informative error on YAML syntax error, including the line number of the
  error.

- ``config.yaml``:

  - ``cache_path`` no longer required. Data files are no longer converted to a
    binary format or stored in a cached dir. This simplifies matters at the cost
    of a minor performance hit.

1.0.6
-----
Last release of the C++ implementation.

.. _semantic versioning: http://semver.org/spec/v2.0.0.html
