from setuptools import setup, find_packages

# Read requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="mpesa_sdk",
    version="0.1.0",
    author="Grivine Bala",
    author_email="grivine@mail.com",
    description="This is an sdk providing convenient access to the Safaricom MPESA Daraja API for applications written in Python3.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/balagrivine/mpesa-sdk",
    packages=find_packages(),
    install_requires=requirements,  # Use requirements from requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
