from setuptools import setup, find_packages

setup(
    name="findhuman",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy"
    ],
    description="A face and human detection package with optional features like distance measurement and image saving.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="MrFidal",
    author_email="mrfidal@proton.me",
    url="https://mrfidal.in/py/findhuman", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
