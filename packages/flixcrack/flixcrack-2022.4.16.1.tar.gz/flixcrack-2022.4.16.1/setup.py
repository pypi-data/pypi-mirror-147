import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flixcrack",
    version="2022.4.16.1",
    author="stefanodvx",
    author_email="pp.stefanodvx@gmail.com",
    description="Netflix API Metadata & Downloader for Windows and Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stefanodvx/flixcrack",
    project_urls={
        "Tracker": "https://github.com/stefanodvx/flixcrack/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "protobuf",
        "pycryptodomex",
        "hyper"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9.8",
)
