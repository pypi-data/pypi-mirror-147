import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="duyan-debug",
    version="0.0.1",
    author="WuMenghao",
    author_email="menghao.wu@duyansoft.com",
    description="Using for Debug, finding problem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["debug_util"],
    python_requires=">=3.6",
    install_requires=[
        'objgraph'
    ]
)
