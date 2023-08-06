import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="print_wcolor",
    version="0.0.8",
    author="wgp",
    author_email="819032030@qq.com",
    description="print_wcolor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wanggaoping/print_wcolor.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
