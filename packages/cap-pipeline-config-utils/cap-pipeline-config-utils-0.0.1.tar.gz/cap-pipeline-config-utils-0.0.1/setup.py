import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cap-pipeline-config-utils",
    version="0.0.1",
    author="Ugur Bayindir",
    author_email="ugur@ebi.ac.uk",
    description="Utility package to autogenerate of semantic tags in ontology pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ubyndr/config_utils",
    project_urls={
        "Bug Tracker": "https://github.com/ubyndr/config_utils/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'jsonschema==4.4.0',
        'SPARQLWrapper==1.8.5'
      ],
    python_requires=">=3.6",
)