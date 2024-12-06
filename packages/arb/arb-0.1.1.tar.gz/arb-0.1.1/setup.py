from setuptools import setup, find_packages

setup(
    name="arb",
    version="0.1.1",
    packages=find_packages(),
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
