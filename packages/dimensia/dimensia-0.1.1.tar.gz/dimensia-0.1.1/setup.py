from setuptools import setup, find_packages

setup(
    name="Dimensia",
    version="0.1.1",
    packages=find_packages(where="."),
    install_requires=[
        "sentence-transformers==3.3.1",
        "torch==2.2.2",
        "numpy==1.26.4",
    ],
    description="A custom vector storage and search solution",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aniruddha Salve",
    author_email="salveaniruddha180@gmail.com",
    url="https://github.com/aniruddhasalve/dimensia/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
