import os
import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

# Get version from environment variable or fallback to a default value
version = os.getenv("PACKAGE_VERSION", "0.0.1")  # Default to '0.0.1' if not provided

setuptools.setup(
    name="notebook-orchestration-and-execution-manager",
    version=version,  # Use the dynamic version from the environment variable
    author="Jorge Cardona",
    description="A tool for orchestrating and executing Jupyter notebooks, enabling seamless parameter passing between notebooks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JorgeCardona/notebook-orchestration-and-execution-manager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'papermill',
        'IPython'
    ],
)