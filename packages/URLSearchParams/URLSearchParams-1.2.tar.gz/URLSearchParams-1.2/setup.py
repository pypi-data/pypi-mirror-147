import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="URLSearchParams",
    version="1.2",
    author="Sijey Praveen",
    author_email="cjpraveen@hotmail.com",
    description="The URLSearchParams interface defines utility methods to work with the query string of a URL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sijey-praveen/googlesearch.py",
    keywords = "URLSearchParams Python, python3, sijey, sijey-praveen, sijey praveen, urlsearchparams, URLSearchParams",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
