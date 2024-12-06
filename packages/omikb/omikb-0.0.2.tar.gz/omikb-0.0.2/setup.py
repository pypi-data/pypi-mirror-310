from setuptools import setup, find_packages

setup(
    name="omikb",
    version="0.0.2",
    packages=find_packages(where='./'),
    package_dir={'': './'},
    install_requires=[
        'requests', 'rdflib'
    ],
    author="'Materials Discovery Group (UCL)",
    author_email="a.hashibon@ucl.ac.uk",
    description="A set of methods to manage the OpenModel Knowledge Base Management",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/H2020-OpenModel/OMIKB-toolbox/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
