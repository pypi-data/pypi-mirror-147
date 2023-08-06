from setuptools import setup, find_packages

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]

setup(
    name="teachstack",
    version="0.1",
    description="Python SDK for teachstack APIs",
    long_description="This module can be used to call teachstack APIs by just using a function. Refer https://docs.teachmint.com for more details.",
    url="https://docs.teachmint.com/",
    author="Parth Agrawal",
    author_email="parth@teachmint.com",
    license="MIT",
    classifiers=classifiers,
    keywords="teachstack, teachmint, python",
    packages=find_packages(),
    install_requires=["requests", "python-dotenv"],
)
