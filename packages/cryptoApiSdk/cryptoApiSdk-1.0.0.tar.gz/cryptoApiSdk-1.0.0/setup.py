from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name="cryptoApiSdk",
    version="1.0.0",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadow-twitter/sdk.git",
    author="Jared Williams",
    author_email="williamsjared62@gmail.com",
    #To find more licenses or classifiers go to: https://pypi.org/classifiers/
    license="",
    packages=['sdk'],
    classifiers=[
    ],
    zip_safe=True,
    python_requires=">=3.0",
)
