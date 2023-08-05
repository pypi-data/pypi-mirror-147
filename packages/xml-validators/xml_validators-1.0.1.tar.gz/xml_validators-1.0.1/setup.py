from setuptools import setup, find_packages

setup(
    name="xml_validators",
    version="1.0.1",
    description="For XML Preprocessing",
    author="Wonseok An",
    author_email="wonseok.an95@gmail.com",
    url="https://github.com/Wonseok-An/xml_validators",
    license="MIT",
    py_modules=["validators"],
    packages=find_packages(),
    python_requires=">=3"
)
