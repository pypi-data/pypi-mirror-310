from setuptools import setup, find_packages

setup(
    name="easytuio",
    version="0.1.0",
    description="A Python library for handling TUIO messages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/easytuio",
    packages=find_packages(),
    install_requires=["python-osc"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
