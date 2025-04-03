from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A better markdown library"

setup(
        name="Better-MD", 
        version=VERSION,
        author="R5dan",
        description=DESCRIPTION,
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
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