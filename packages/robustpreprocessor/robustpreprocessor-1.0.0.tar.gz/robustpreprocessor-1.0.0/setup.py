from setuptools import setup, find_packages

setup(
    name="robustpreprocessor",
    version="1.0.0",
    description="RobustPreprocessor is designed to preprocess datasets effectively to ensure robust data preparation before further analysis or modeling.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mohd Adil",
    author_email="mohdadil@live.com",
    url="https://github.com/nqmn/robustpreprocessor",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "scipy>=1.7.0",
        "matplotlib>=3.2.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    # Keywords for PyPI
    keywords=[
        "data preprocessing",
        "outlier handling",
        "missing data",
        "data cleaning",
        "feature engineering",
        "robust preprocessing",
    ],

)
