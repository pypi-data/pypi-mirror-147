import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # name="layerai", # Replace with desired PyPI package name
    # name="dbt-layer-bigquery", # Replace with desired PyPI package name
    name="layer-api", # Replace with desired PyPI package name
    version="0.0.1",
    author="Layer",
    author_email="python-sdk@layer.ai",
    description="The Layer SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://layer.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
