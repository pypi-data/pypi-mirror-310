from setuptools import setup, find_packages

def readme():
    return "None"

setup(
    name="faio",
    version="1.0.1",
    author="Mazga",
    author_email="agzamikail@gmail.com",
    description=" ",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages= find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="",
    project_urls=dict(),
    python_requires=">=3.0",
)
