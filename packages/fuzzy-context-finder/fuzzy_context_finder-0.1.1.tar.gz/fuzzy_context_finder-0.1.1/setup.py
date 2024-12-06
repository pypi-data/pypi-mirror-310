from setuptools import setup, find_packages

setup(
    name="fuzzy_context_finder",  # Your package name
    version="0.1.1",  # Initial version
    description="search for keywords and their context",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sandeep Junnarkar",
    author_email="sjnews@gmail.com",
    url="https://github.com/sandeepmj/fuzzy_context_finder",  # Repo URL or project homepage
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum Python version
    install_requires=[  # Dependencies
        "regex",
        "pandas>=1.0.0",
        "rapidfuzz>=2.0.0"
    ],
)
