import setuptools

with open("README.md") as f:
    long_description = f.read()

name = "prozt"
version = "0.0.1"
author = "Prootzel"

short_description = "better print command"

#github repo url
url = ""

setuptools.setup(
    name = name,
    version = version,
    author = author,
    author_email = "lirkel123@gmail.com",
    description = short_description,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = url,
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)