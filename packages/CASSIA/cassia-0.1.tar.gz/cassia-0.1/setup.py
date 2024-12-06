from setuptools import setup, find_packages

setup(
    name="CASSIA",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "openai",
        "anthropic"
    ],
)