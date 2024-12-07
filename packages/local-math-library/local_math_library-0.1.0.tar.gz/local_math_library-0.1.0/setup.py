
from setuptools import setup, find_packages

setup(
    name="local_math_library",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List any dependencies here
    ],
    author="Anup Ghosh",
    author_email="anup.ghosh@bjitacademy.com",
    description="An example of a custom library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shamim-hossen-razu/core_python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)