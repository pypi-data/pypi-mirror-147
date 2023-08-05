import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kopl-engine-macos",
    version="2022.4",
    author="THU KEG",
    author_email="",
    description="Knowledge oriented Programing Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShulinCao/KoPLEngine",
    project_urls={
        "Documents": "https://kopl.xlore.cn/doc/",
    },
    install_requires=[
        "tqdm>=4.62"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"kopl_engine": ["libKoPL.dylib"]},
    python_requires=">=3.6",
)