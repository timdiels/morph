# Auto generated by ct-mksetup
# Do not edit this file, edit ./project.py instead

from setuptools import setup
setup(
    **{   'author': 'VIB/BEG/UGent',
    'author_email': 'timdiels.m@gmail.com',
    'classifiers': [   "'Intended Audience :: Science/Research',",
                       'Development Status :: 2 - Pre-Alpha',
                       'Environment :: Console',
                       'License :: OSI Approved',
                       'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                       'Natural Language :: English',
                       'Operating System :: POSIX',
                       'Operating System :: POSIX :: AIX',
                       'Operating System :: POSIX :: BSD',
                       'Operating System :: POSIX :: BSD :: BSD/OS',
                       'Operating System :: POSIX :: BSD :: FreeBSD',
                       'Operating System :: POSIX :: BSD :: NetBSD',
                       'Operating System :: POSIX :: BSD :: OpenBSD',
                       'Operating System :: POSIX :: GNU Hurd',
                       'Operating System :: POSIX :: HP-UX',
                       'Operating System :: POSIX :: IRIX',
                       'Operating System :: POSIX :: Linux',
                       'Operating System :: POSIX :: Other',
                       'Operating System :: POSIX :: SCO',
                       'Operating System :: POSIX :: SunOS/Solaris',
                       'Operating System :: Unix',
                       'Programming Language :: Python',
                       'Programming Language :: Python :: 3',
                       'Programming Language :: Python :: 3 :: Only',
                       'Programming Language :: Python :: 3.2',
                       'Programming Language :: Python :: 3.3',
                       'Programming Language :: Python :: 3.4',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: Implementation',
                       'Programming Language :: Python :: Implementation :: CPython',
                       'Programming Language :: Python :: Implementation :: Stackless',
                       'Topic :: Scientific/Engineering',
                       'Topic :: Scientific/Engineering :: Artificial Intelligence',
                       'Topic :: Scientific/Engineering :: Bio-Informatics'],
    'description': 'MOdule guided Ranking of candidate PatHway genes',
    'entry_points': {'console_scripts': ['morph = deep_genome.morph.main:main']},
    'extras_require': {   'dev': ['numpydoc', 'sphinx', 'sphinx-rtd-theme'],
                          'test': ['coverage-pth', 'pytest', 'pytest-cov', 'pytest-env', 'pytest-xdist']},
    'install_requires': [   'bottleneck',
                            'chicken-turtle-util',
                            'click',
                            'freezegun>0.3.5',
                            'frozendict',
                            'inflection',
                            'matplotlib',
                            'memory-profiler',
                            'more-itertools',
                            'networkx',
                            'numexpr',
                            'numpy',
                            'pandas',
                            'plumbum',
                            'psutil',
                            'pymysql',
                            'pytest',
                            'pytest-benchmark',
                            'pytest-timeout',
                            'pytest-xdist',
                            'pyxdg',
                            'requests',
                            'scikit-learn',
                            'scipy',
                            'sqlalchemy'],
    'keywords': 'bioinformatics coexpression guilt-by-association',
    'license': 'LGPL3',
    'long_description': 'Required Python 3 libraries:\n'
                        '\n'
                        'Additional Python 3 libraries required for development:\n'
                        '\n'
                        '-  twine\n'
                        '-  pypandoc\n',
    'name': 'deep-genome-morph',
    'package_data': {'deep_genome.morph': ['data/cli.conf', 'data/cli.defaults.conf', 'data/main.defaults.conf']},
    'packages': ['deep_genome', 'deep_genome.morph', 'deep_genome.morph.tests'],
    'url': 'https://gitlab.psb.ugent.be/deep_genome/morph.git',
    'version': '0.0.0'}
)
