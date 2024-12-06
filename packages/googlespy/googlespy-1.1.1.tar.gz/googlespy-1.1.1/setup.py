from setuptools import setup, find_packages

setup(
    name="googlespy",
    version="1.1.1",
    description="A Python package to search Google and retrieve filtered links.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
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
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords=[
        "mrfidal", 
        "fidal palamparambil", 
        "google", 
        "search", 
        "scraping", 
        "web scraping", 
        "python", 
        "googlesearch", 
        "api", 
        "filtered links",
        "alpha"
    ],
)
