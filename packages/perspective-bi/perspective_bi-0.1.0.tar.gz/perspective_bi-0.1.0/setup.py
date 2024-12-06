from setuptools import setup, find_packages

setup(
    name="perspective-bi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "plotly>=5.13.0",
        "numpy>=1.24.0",
        "python-dateutil>=2.8.2",
    ],
    author="Robert Ritz",
    description="A declarative business intelligence library designed for natural language interactions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/perspective-bi/perspective-bi",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
