from setuptools import setup, find_packages

setup(
    name="kfircli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "kfircli = main:main",
        ],
    },
)
