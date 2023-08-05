import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connectNvironment",
    version="1.0.2",
    author="Rick Vink",
    author_email="justrickschannel@gmail.com",
    description="Connect 4 and more (or less)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IRiViI/connect_n",
    packages=setuptools.find_packages(),
    keywords=["connect4", "connectn", "connect_n", "environment"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["scipy", "numpy"],
)