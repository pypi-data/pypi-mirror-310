from setuptools import setup, find_packages

setup(
    name="aew_api",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'aew_api': ['data/*.json'],
    },
    author="Wrestle Blitz",
    author_email="wrestleblitz@gmail.com",
    description="An API for accessing AEW wrestler data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amin-97/aew_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)