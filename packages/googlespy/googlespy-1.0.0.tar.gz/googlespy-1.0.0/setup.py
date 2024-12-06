from setuptools import setup, find_packages

setup(
    name="googlespy",
    version="1.0.0",
    description="A Python package to search Google and retrieve filtered links.",
    author="Fidal",
    author_email="mrfidal@proton.me",
    url="https://mrfidal.in/py/package/googlespy",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
