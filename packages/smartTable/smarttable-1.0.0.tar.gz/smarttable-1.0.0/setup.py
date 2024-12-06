from setuptools import setup, find_packages

setup(
    name="smartTable",  # Nom du package
    version="1.0.0",  # Version initiale
    description="Module Python pour la manipulation et la visualisation de tableaux dynamiques",
    long_description=open("README.md").read(),  # Récupérer la description longue
    long_description_content_type="text/markdown",
    author="Abdallah Nassur",
    author_email="nassur1607@gmail.com",
    url="https://github.com/NassAbd/smartTable",  # Lien vers le dépôt GitHub
    license="MIT",
    packages=find_packages(),  # Inclut tous les packages dans smart_table/
    install_requires=[
        "numpy>=1.21",
        "pandas>=1.3",
        "matplotlib>=3.0",
    ],
    python_requires=">=3.7",  # Version minimale de Python
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
