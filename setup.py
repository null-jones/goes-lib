import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goes-lib",
    version="0.0.1",
    author="Isaac jones",
    author_email="isaac@isaacjones.ca",
    description="Library for processing GOES-16 & GOES-17 files from AWS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/null-jones/goes-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
