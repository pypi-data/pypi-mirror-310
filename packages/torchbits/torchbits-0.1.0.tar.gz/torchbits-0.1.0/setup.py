from setuptools import setup, find_packages

setup(
    name="torchbits",                       # Package name
    version="0.1.0",                         # Package version
    author="Chima Emmanuel",
    author_email="chimaifeanyi62@gmail.com",
    description="A lightweight deep signal processing library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/torchbits/torchbits",  # Project URL (GitHub or other)
    packages=find_packages(),                # Automatically find subpackages
    install_requires=[                       # Dependencies
        "numpy",   # if needed
    ],
    classifiers=[                            # Metadata about the package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
