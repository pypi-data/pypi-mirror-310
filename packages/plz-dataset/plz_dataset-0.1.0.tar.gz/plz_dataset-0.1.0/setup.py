from setuptools import setup, find_packages

setup(
    name = 'plz_dataset',
    version = '0.1.0',
    packages=find_packages(),
    install_requires=["pandas>=1.3.0"],  # Abhängigkeiten, falls vorhanden
    description="Package for generating PLZ lists for german cities.",
    author="AbakusNantis",
    author_email="privat@bastianknaus.de",
    url="https://github.com/AbakusNantis/dataset_plz",  # Optionale GitHub-URL
    python_requires=">=3.6",
    )