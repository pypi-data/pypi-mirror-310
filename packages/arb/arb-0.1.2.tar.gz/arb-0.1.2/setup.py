from setuptools import setup, find_packages
import os

def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()
    
setup(
    name="arb",
    version="0.1.2",
    packages=find_packages(),
    long_description=read_readme(),  # Include the README content here
    long_description_content_type='text/markdown',
    install_requires=[
        "ccxt",
        "colorama==0.4.6",
        "requests==2.31.0",
        "pytz==2023.3",
    ],
    entry_points={
        "console_scripts": [
            "arb=arb.run:main",  # Optional CLI
        ],
    },
)
