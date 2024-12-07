from setuptools import setup, find_packages

setup(
    name="x-sparta",
    version="1.0.0",
    author="Ghost",
    author_email="your.email@example.com",
    description="A secure downloader that downloads files based on passcode authentication.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",  # Dependency for downloading files
    ],
    entry_points={
        "console_scripts": [
            "secure-downloader=secure_downloader.downloader:download_file",  # Maps command to function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
