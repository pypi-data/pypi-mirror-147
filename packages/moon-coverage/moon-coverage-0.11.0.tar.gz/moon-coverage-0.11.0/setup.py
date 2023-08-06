"""Moon coverage setup."""

import re

from setuptools import find_packages, setup


with open('moon_coverage/version.py', encoding='utf-8') as f:
    __version__ = re.findall(
        r'__version__ = \'(\d+\.\d+\.\d+)\'',
        f.read()
    )[0]

with open('README.md', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='moon-coverage',
    version=__version__,
    description='Moon Coverage toolbox',
    author='Benoit Seignovert, Rozenn Robidel',
    author_email='moon-coverage@univ-nantes.fr',
    url='https://juigitlab.esac.esa.int/datalab/moon-coverage',
    project_urls={
        'Documentation': 'https://moon-coverage.moon-coverage.fr',
        'Source': 'https://juigitlab.esac.esa.int/datalab/moon-coverage',
        'Tracker': 'https://juigitlab.esac.esa.int/datalab/moon-coverage/-/issues',
        'Changelog': 'https://moon-coverage.moon-coverage.fr/en/latest/CHANGELOG.html',
    },
    license='BSD',
    python_requires='>=3.8',
    install_requires=[
        'numpy==1.22.2',
        'matplotlib==3.4.3',
        'spiceypy==5.0.0',
        'Pillow==9.0.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['moon', 'coverage', 'esa', 'juice'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
    long_description=readme,
    long_description_content_type='text/markdown',
)
