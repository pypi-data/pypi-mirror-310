from setuptools import setup, find_packages

setup(
    name="ml_algorithms",
    version="0.1.2",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["matplotlib>=3.9.2", "numpy>=2.1.3"],
)
