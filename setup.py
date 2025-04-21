from setuptools import setup, find_packages

VERSION = "0.3.2"
DESCRIPTION = "A better markdown library"

def read(path):
    with open(path, "r") as f:
        return f.read()

setup(
        name="Better-MD", 
        version=VERSION,
        author="R5dan",
        description=DESCRIPTION,
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        packages=find_packages(exclude="tests"),
        install_requires=[],
        extras_require={
            "tables": ["pandas==2.2.3"]
        },
        keywords=['python', 'better markdown', 'markdown'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ],
        url="https://github.com/Better-MD/better-md"
)
