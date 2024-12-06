from setuptools import setup, find_packages

setup(
    name="kaiban",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    author="Kaiban Team",
    description="Python SDK for Kaiban",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kaiban/kaiban-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)