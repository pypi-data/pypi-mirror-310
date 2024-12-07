from setuptools import setup, find_packages

setup(
    name="arka_python",
    version="0.1",
    description="A Python package to interact with the Arka blockchain network",
    author="Python",
    author_email="chandini@vitwit.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
    ],
    python_requires=">=3.6",
)
