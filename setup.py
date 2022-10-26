import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DynamoBase",
    version="0.1.0",
    author="Jaguar",
    author_email="jack.v.yang@gmail.com",
    description="A Json Model that is the easiest way to query DynamoDB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaguaryang/dynamo-base",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
