from setuptools import setup, find_packages

setup(
    name="aimluvce",  # Replace with your package name
    version="0.1.1",  # Update the version as needed
    description="A custom library with various functions and models for ANN labouratory",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="prashanthktgowda",
    author_email="prashanthktgowda123@gmail.com",
    url="https://github.com/prashanthktgowda/aimluvce",  # Replace with your GitHub URL
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy",  # List all dependencies here
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
