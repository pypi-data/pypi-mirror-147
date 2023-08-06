# from setuptools import setup, find_packages
#
# setup(
#     name="DuyanUtils",
#     version="1.1",
#     packages=find_packages("src"),
#     package_dir={"": "src"}
# )
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DuyanUtils",
    version="1.0.4",
    author="Jianguo.Wang",
    author_email="chunyang.wang@duyansoft.com",
    description="常用工具 轻量化处理",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
