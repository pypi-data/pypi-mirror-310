from setuptools import setup, find_packages

setup(
    name="akeem-text-preprocessor",
    version="0.1.0",
    description="A comprehensive text preprocessing library.",
    author="Your Name",
    packages=find_packages(),
    install_requires=["nltk", "beautifulsoup4"],
    include_package_data=True,
    package_data={
        'resources': ['*.txt', '*.json'],
    },
)