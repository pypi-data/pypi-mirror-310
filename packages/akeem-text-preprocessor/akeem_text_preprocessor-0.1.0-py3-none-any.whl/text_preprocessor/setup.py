from setuptools import setup, find_packages

setup(
    name="text_preprocessor",
    version="0.1.0",
    description="A comprehensive text preprocessing library.",
    author="Akeem Raji",
    packages=find_packages(),
    install_requires=["nltk", "beautifulsoup4"],
    include_package_data=True,
    package_data={
        'resources': ['*.txt', '*.json'],
    },
)