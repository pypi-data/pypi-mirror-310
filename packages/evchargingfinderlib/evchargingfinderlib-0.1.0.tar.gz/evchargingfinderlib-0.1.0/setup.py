from setuptools import setup, find_packages

setup(
    name="evchargingfinderlib",  # Replace with your library name
    version="0.1.0",
    author="Saigowtham x23337818@student.ncirl.ie",
    author_email="x23337818@student.ncirl.ie",
    description="A library that returns current datetime with a booking success message",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Education',
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
