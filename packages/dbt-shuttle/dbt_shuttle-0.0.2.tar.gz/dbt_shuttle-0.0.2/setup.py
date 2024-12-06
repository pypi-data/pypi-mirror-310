from setuptools import setup, find_packages

# Read the README file for a long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dbt-shuttle",
    version="0.0.2",
    author="zhuang mei",
    author_email="1213258400@qq.com",
    description="A toolkit for managing DBT and data shuttle SQL transformations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mz223032/dbt-shuttle",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0",
        "pyyaml>=6.0",
        "google-auth>=2.21.0",
        "google-cloud-secret-manager>=2.16.0",
    ],
    entry_points={
        "console_scripts": [
            "dbt-shuttle=dbt_shuttle.cli:main",
        ]
    },
)
