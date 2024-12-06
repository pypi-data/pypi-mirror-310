from setuptools import setup, find_packages

setup(
    name="codrone-simulator",  # Replace with your project name
    version="0.2.7",  # Replace with your initial version
    author="10boticsDev",  # Replace with your name
    author_email="mark.protusada@10botics.com",  # Replace with your email
    description="A Python package for simulating drone operations and learning drone programming in a virtual environment.",  # Short description
    long_description=open("README.md").read(),  # Use README.md for long description
    long_description_content_type="text/markdown",  # Specify format of README
    project_urls={  # Custom project links
        "GitHub Repository": "https://github.com/10botics/codrone-simulator-sdk-python",
        "Drone Simulator Github": "https://github.com/10botics/codrone-simulator",
    },
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",  # Use a generic classifier for non-standard licenses
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version requirement
    install_requires=[
        # List your dependencies here, e.g., "numpy>=1.19"
    ],
    license="CC-BY-ND-4.0",  # Specify the license here
)