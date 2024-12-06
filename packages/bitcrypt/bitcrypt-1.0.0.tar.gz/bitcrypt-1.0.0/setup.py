from setuptools import setup, find_packages

# Read the content of README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bitcrypt",
    version="1.0.0",
    description="A library for bit-level encryption and decryption with Base64 encoding.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AndrewCo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "bitcrypt=bitcrypt.__main__:main",
        ],
    },
    include_package_data=True,
)
