from setuptools import setup, find_packages

setup(
    name="optimal_regressors",
    version="0.1.0",
    description="A library to determine optimal configurations for regressors.",
    author="Rehan Taneja",
    author_email="rehan.taneja4321@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "scikit-learn>=1.0",
        "xgboost>=1.7.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)