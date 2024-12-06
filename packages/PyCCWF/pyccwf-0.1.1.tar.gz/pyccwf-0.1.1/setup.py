from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="PyCCWF",
    version="0.1.1",
    author="Maya Ramchandran",
    description="Implementation of Cross-cluster Weighted Forests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy",
        "matplotlib"
    ],
    python_requires=">=3.7",
)