from setuptools import setup, find_packages

setup(
    name="crab-lib",
    version="1.0.0",
    description="A Python library for analyzing GPS data from fishing grounds.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Joe Stem - Red Glove Productions",
    author_email="joestem25@gmail.com",
    url="https://github.com/RedGloveProductions/crab-lib",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="gps fishing data analysis visualization",
    project_urls={
        "Bug Tracker": "https://github.com/RedGloveProductions/crab-lib/issues",
        "Source Code": "https://github.com/RedGloveProductions/crab-lib",
    },
)
