from setuptools import setup, find_packages

setup(
    name="PyCCWF",
    version="0.1.0",
    author="Maya Ramchandran",
    description="Implementation of Cross-cluster Weighted Forests",
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