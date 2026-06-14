from setuptools import setup, find_packages

setup(
    name="lead-enrichment-tool",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.7",
        "pandas>=2.1.4",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "dnspython>=2.4.2",
        "tabulate>=0.9.0",
        "tqdm>=4.66.1",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "enrich=enricher.cli:cli",
        ],
    },
    python_requires=">=3.9",
)
