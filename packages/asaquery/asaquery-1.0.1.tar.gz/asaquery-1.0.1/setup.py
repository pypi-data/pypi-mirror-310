import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="asaquery",
    version="1.0.1",
    author="nattyan-tv",
    description="A simple library for querying ASA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nattyan-tv/asa-query-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
)
