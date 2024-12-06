from setuptools import setup, find_packages

setup(
    name="sklearnplot",
    version="0.1.0",
    description="A description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my_package",  # Repo URL
    packages=find_packages(),
    install_requires=[
        # List dependencies, e.g., "numpy>=1.19.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
