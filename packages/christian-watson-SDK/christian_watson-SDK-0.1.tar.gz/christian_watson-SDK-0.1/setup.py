from platform import python_revision
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='christian_watson-SDK',
    version="0.1",
    author="Christian Watson",
    author_email="chris23w@gmail.com",
    description="SDK for use with The One API, a Lord of the Rings API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicofasho/christian_watson-SDK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'aiohttp',
        'pytest'
    ],
    keywords='sdk lord of the rings',
)
