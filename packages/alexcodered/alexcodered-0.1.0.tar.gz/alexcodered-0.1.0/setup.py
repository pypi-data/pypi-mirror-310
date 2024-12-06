from setuptools import setup,find_packages
setup(
    name='alexcodered',     # package name
    version='0.1.0',        # Version
    description='A Sample Python module',
    author='Alex Thankachan',
    author_email='alexthankachan95@outlook.com',
    packages=find_packages(),       # Automatically find modules      
    install_requiries=[],           # Dependencies(if any)
    python_requiries='>=3.6',       # Supported Python versions
)