from setuptools import setup, find_packages

setup(
    name="sua_biblioteca",
    version="0.1.0",
    description="Uma biblioteca simples para operações matemáticas básicas.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Seu Nome",
    author_email="seuemail@exemplo.com",
    url="https://github.com/seu_usuario/sua_biblioteca",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
