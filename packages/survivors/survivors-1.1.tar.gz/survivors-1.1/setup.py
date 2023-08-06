from setuptools import setup, find_packages
from os.path import join, dirname
from pkg_resources import parse_requirements as _parse_requirements

SELF_DATASETS = []#["datasets/data/ONK/*", "datasets/data/COVID/*"]

PACKAGE_DATA = {"survivors": ["datasets/data/*"] + SELF_DATASETS}

def parse_requirements(filename):
    with open(filename) as fin:
        parsed_requirements = _parse_requirements(
            fin)
        requirements = [str(ir) for ir in parsed_requirements]
    return requirements

setup(
    name='survivors',
    version='1.1',
    author='Iulii Vasilev',
    author_email='iuliivasilev@gmail.com',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data = False,
    package_data=PACKAGE_DATA,
    python_requires='>=3.7',
    install_requires=parse_requirements('requirements/prod.txt'),
)