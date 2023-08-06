from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='xvideos',
    version='0.2',
    author="Alexander Timofeev",
    author_email="tam2511@mail.ru",
    python_requires=">=3.6",
    package_dir={"": "xvideos"},
    packages=find_packages(where="xvideos"),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tam2511/xvideos",
    install_requires=[
        'opencv-python'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
