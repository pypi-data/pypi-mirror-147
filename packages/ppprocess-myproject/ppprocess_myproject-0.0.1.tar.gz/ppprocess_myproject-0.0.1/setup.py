from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ppprocess_myproject",
    version="0.0.1",
    author="Marcelo Goulart Lima",
    author_email="glima.marcelo@gmail.com",
    description="2ªversão projeto DIO processamento de imagens com Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
