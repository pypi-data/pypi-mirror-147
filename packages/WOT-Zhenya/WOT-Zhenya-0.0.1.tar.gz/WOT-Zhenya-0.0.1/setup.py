import setuptools

setuptools.setup(
    name="WOT-Zhenya",
    version="0.0.1",
    author="ZHENYA",
    author_email="sluckltu@gmail.com",
    description="Игра в танки",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "wot"},
    packages=setuptools.find_packages(where="wot"),
    python_requires=">=3.6",
)