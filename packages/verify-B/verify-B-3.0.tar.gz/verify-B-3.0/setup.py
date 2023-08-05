# author : wangcwangc
# time : 2021/12/28 2:37 PM
import setuptools

setuptools.setup(
    name="verify-B",
    version="3.0",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description="lab a",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests>=2.26.0"],
)
