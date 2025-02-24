from setuptools import setup, find_packages

setup(
    name="pyMDBTerminal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyserial~=3.5"
    ],
    python_requires=">=3.7",
)
