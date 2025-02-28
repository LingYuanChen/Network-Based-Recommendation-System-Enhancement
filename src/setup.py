from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="amazon-recommendation-system",
    version="1.0.0",
    author="Yan-Da Chen, Ling-Yuan Chen",
    author_email="topangutppy@gmail.com",
    description="A graph-based recommendation system for Amazon products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LingYuanChen/Network-Based-Recommendation-System-Enhancement",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
) 