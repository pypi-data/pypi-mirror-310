from setuptools import setup, find_packages

setup(
    name="dimensia",
    version="0.1.2",
    author="Aniruddha Salve",
    author_email="salveaniruddha180@gmail.com",
    description="Dimensia is a Python library for managing document embeddings and performing efficient similarity-based searches using various distance metrics. It supports creating collections, adding documents, and querying over long text data with customizable vector-based search capabilities.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aniruddhasalve/dimensia/",
    packages=find_packages(),
    install_requires=[
        "requests",
        "sentence-transformers",
        "tqdm",
        "numpy",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="vector database embeddings NLP AI search",
    project_urls={
        "Bug Tracker": "https://github.com/aniruddhasalve/dimensia/issues",
        "Source Code": "https://github.com/aniruddhasalve/dimensia/",
    },
)
