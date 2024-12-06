from setuptools import setup, find_packages

setup(
    name="tabular_2_text",  # Your package name
    version="0.1.4",  # Initial version
    description="Take a df or csv and convert to text",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sandeep Junnarkar",
    author_email="sjnews@gmail.com",
    url="https://github.com/sandeepmj/tabular_2_text",  # Repo URL or project homepage
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum Python version
    install_requires=[  # Dependencies
        "numpy>=1.21.0",
        "pandas>=1.3.0"
    ],
)
