from setuptools import setup, find_packages

setup(
    name="xvs",  # Replace with your CLI tool name
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",  # Dependencies
    ],
    entry_points={
        "console_scripts": [
            "xvs=xvs.vs:main",  # Define the command and entry point
        ],
    },
    author="Ghost",
    description="A simple tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
