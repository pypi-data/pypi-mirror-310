from setuptools import setup, find_packages

setup(
    name="Lavender-GitHub",
    version="1.0.1",
    author="Zeyu Xie",
    author_email="xie.zeyu20@gmail.com",
    description="A python package for packaging GitHub REST API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zeyu-Xie/Lavender-GitHub",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
