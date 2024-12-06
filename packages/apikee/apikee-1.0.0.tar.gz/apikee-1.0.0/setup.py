from setuptools import setup, find_packages

setup(
    name="apikee",
    version="1.0.0",
    author="usmhic",
    description="ApiKee - A lightweight API key validation library for FastAPI",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    url="https://github.com/apikee-dev/apikee-python",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
