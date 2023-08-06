import setuptools

from version import VERSION

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="toolsgram",
    version=VERSION,
    author="Sergio Abad",
    author_email="sergio.abad@bytelix.com",
    description="Python toolbox for Telegram bots development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/sergioteula/toolsgram",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
