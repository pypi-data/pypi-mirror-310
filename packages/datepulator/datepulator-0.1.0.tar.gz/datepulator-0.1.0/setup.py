from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datepulator",
    version="0.1.0",
    author="Ashutosh Bele",
    author_email="your.email@example.com",
    description="A powerful Python library for date manipulation and formatting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/datepulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "python-dateutil>=2.8.0",
        "pytz>=2021.1",
    ],
)
