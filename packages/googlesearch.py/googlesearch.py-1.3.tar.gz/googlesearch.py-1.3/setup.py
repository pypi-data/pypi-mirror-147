import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googlesearch.py",
    version="1.3",
    author="Sijey Praveen",
    author_email="cjpraveen@hotmail.com",
    description="Library for scraping google search results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sijey-praveen/googlesearch.py",
    keywords = "googlesearch.py, python google search, google search pypi, sijey-praveen pypi, google api, sijey, sijey-praveen, sijey praveen projects",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
