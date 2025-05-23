from setuptools import setup, find_packages

setup(
    name="whosampled",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.1",
        "networkx>=3.2.1",
        "plotly>=5.18.0",
        "streamlit>=1.32.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-mock>=3.12.0",
            "pytest-cov>=4.1.0",
            "requests-mock>=1.12.0",
        ],
    },
    python_requires=">=3.8",
) 