from setuptools import setup, find_packages

setup(
    name="machine-id-retriever",  # Unique package name
    version="0.1",
    description="A Python package to retrieve the machine ID",
    author="Harisha P C",
    author_email="info@xtal.in",
    packages=find_packages(),
    install_requires=[],  # No external dependencies required
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
