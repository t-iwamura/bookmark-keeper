from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bsafe",
    version="1.1.0",
    author="Taiki Iwamura",
    author_email="takki.0206@gmail.com",
    description=("CLI app to automatically backup Pocket items and Raindrop.io items"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t-iwamura/bsafe",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">= 3.9",
    entry_points={
        "console_scripts": [
            "bsafe=bsafe.scripts.main:main",
        ]
    },
)
