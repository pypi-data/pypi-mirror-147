import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Simple_Logger_Tool",
    version="1.0.5",
    author="Matt Inwards",
    author_email="",
    description="Just some simple logging functions that can be used in pretty much any program.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m-inwards/Simple-Logging",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
