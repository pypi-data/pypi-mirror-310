from setuptools import setup, find_packages

setup(
    name="brown-logger",
    version="0.1.0",
    author="Lam",
    author_email="huynhnhathanhtruc@gmail.com",
    description="A Singleton Logger implementation with console and file logging support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iamlamm/brown-logger",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
