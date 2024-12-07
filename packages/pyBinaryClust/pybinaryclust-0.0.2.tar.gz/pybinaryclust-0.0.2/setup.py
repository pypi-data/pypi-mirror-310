from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'BinaryClust Python'
LONG_DESCRIPTION = 'Python Reimplementation of the R package BinaryClust'


setup(
        name="pyBinaryClust", 
        version=VERSION,
        author="Desmond Choy",
        author_email="<desmondchoy@cantab.net>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(where = "src/pyBinaryClust"),
        install_requires=["numpy", "scipy", "matplotlib"],
        keywords=['python', 'BinaryClust', 'CyTOF', 'bioinformatics', 'cytometry']
)