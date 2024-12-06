from setuptools import setup, find_packages

setup(
    name="exposor",
    version="1.0.0",
    description="Exposor - Unified query system for search engines",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Abdulla Abdullayev",
    author_email="abu@abuyv.com",
    url="https://github.com/abuyv/exposor",  # Project URL (GitHub or other)
    packages=find_packages(),  # Automatically find all sub-packages
    include_package_data=True,  # Include non-code files (via MANIFEST.in)
    install_requires=[
        "requests",  # Add dependencies here
        "pyyaml",
        "python-dotenv",
        "setuptools"
    ],
    entry_points={
        "console_scripts": [
            "exposor=exposor:main",  # Maps the CLI command `exposor` to `main()` in exposor.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security"
    ],
    python_requires=">=3.8",  # Minimum Python version
)
