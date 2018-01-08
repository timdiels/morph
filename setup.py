from setuptools import setup, find_packages
from collections import defaultdict
from pathlib import Path
import os

setup_args = dict(
    version='2.0.0.dev',
    name='morphbio',
    description='Reveal missing genes in biological pathways or groups of related genes',
    long_description=Path('README.rst').read_text(),
    url='https://gitlab.psb.ugent.be/deep_genome/morph',
    author='VIB/UGent/BEG',
    author_email='tidie@psb.ugent.be',
    license='LGPL3',
    keywords='bioinformatics coexpression guilt-by-association',
    packages=find_packages(),
    install_requires=[
        'click',
        'numpy',
        'pandas',
        'plumbum',
        'more_itertools',
        'chicken_turtle_util',
    ],
    extras_require={
        'dev': [
            'sphinx==1.*',
            'sphinx-rtd-theme==0.*',
            'coverage-pth==0.*',
            'pytest==3.*',
            'pytest-cov==2.*',
            'pytest-env==0.*',
        ],
    },
    entry_points={'console_scripts': [
        'morph = morphbio.main:main'
    ]},
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Environment :: Console',
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)

# Generate extras_require['all'], union of all extras
all_extra_dependencies = []
for dependencies in setup_args['extras_require'].values():
    all_extra_dependencies.extend(dependencies)
all_extra_dependencies = list(set(all_extra_dependencies))
setup_args['extras_require']['all'] = all_extra_dependencies

# Generate package data
#
# Anything placed underneath a directory named 'data' in a package, is added to
# the package_data of that package; i.e. included in the sdist/bdist and
# accessible via pkg_resources.resource_*
project_root = Path(__file__).parent
package_data = defaultdict(list)
for package in setup_args['packages']:
    package_dir = project_root / package.replace('.', '/')
    data_dir = package_dir / 'data'
    if data_dir.exists() and not (data_dir / '__init__.py').exists():
        # Found a data dir
        for parent, _, files in os.walk(str(data_dir)):
            package_data[package].extend(str((data_dir / parent / file).relative_to(package_dir)) for file in files)
setup_args['package_data'] = {k: sorted(v) for k,v in package_data.items()}  # sort to avoid unnecessary git diffs

# setup
setup(**setup_args)

