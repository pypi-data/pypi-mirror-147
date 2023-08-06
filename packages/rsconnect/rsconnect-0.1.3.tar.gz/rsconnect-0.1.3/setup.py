import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rsconnect",
    version="0.1.3",
    author="Mark Sellors",
    author_email="python@5vcc.com",
    description="A small meta-package to install package to use with RStudio Connect.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sellorm/rsconnect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'rsconnect-jupyter',
        'rsconnect-python',
        'pins',
    ],
)
