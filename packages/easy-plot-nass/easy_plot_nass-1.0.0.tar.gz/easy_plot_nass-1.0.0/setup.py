from setuptools import setup, find_packages

setup(
    name="easy_plot_nass",  # Nom de votre module
    version="1.0.0",  # Numéro de version
    description="A simple module for creating plots with Matplotlib.",  # Une courte description
    long_description=open("README.md").read(),  # Une description complète (issue du fichier README)
    long_description_content_type="text/markdown",  # Spécifie que README.md est en Markdown
    author="Abdallah Nassur",
    author_email="nassur1607@gmail.com",
    url="https://github.com/NassAbd/easy_plot",  # (Facultatif) URL vers votre dépôt GitHub
    packages=find_packages(),  # Recherche automatique de vos fichiers Python
    install_requires=[
        "matplotlib>=3.0"  # Dépendance pour Matplotlib
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Spécifie la version minimale de Python
)
