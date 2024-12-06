from setuptools import setup, find_packages

setup(
    name="bdacode",  # Package name (unique on PyPI)
    version="0.1.1",  # Initial version
    author="Naveen Sakthi",
    author_email="naveendgp@gmail.com",
    description="A Python package for BDA answers.",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically discover sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",  # Example dependency
    ],
)
