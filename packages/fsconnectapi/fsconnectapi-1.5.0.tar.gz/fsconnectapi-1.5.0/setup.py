from setuptools import setup, find_packages

setup(
    name="fsconnectapi",  # Ensure this is a unique name
    version="1.5.0",
    description="A simple Python API for key management and summarization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="FSConnect",
    author_email="logtkenn@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
