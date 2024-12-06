# setup.py
from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fridaylabs",
    version="0.2.1",  # Incremented version to reflect updates
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",  # Specify version to ensure compatibility
    ],
    author="FridayLabs",
    author_email="fridaylabs@fridaylabs.ai",
    description="A Python client library to interact with the FridayLabs AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ImJustRicky/fridaylabs-package",
    project_urls={
        "Documentation": "https://github.com/ImJustRicky/fridaylabs-package#readme",
        "Source": "https://github.com/ImJustRicky/fridaylabs-package",
        # Add other relevant URLs if any
    },
    classifiers=[
        "Development Status :: 4 - Beta",  # Adjust status as appropriate
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",  # Specify versions you support
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="fridaylabs ai api client",
    python_requires='>=3.7',  # Updated to reflect current Python versions
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
)
