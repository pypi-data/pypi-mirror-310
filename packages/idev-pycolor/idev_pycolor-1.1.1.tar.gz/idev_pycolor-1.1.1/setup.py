import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "idev-pycolor",
    version = "1.1.1",
    author = "IrtsaDevelopment",
    author_email = "irtsa.development@gmail.com",
    description = "A python collection of classes and functions to convert between multiple color models, generate palettes, and more.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/irtsa-dev/PyColor",
    project_urls = {
        "Bug Tracker": "https://github.com/irtsa-dev/PyColor/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "idev-pycolor"},
    packages=["PyColor"],
    python_requires = ">=3.6"
)