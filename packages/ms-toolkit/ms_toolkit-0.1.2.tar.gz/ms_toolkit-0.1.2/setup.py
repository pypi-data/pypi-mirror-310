from setuptools import setup, find_packages
from os import path

# Aqui estamos pegando o caminho da pasta onde o setup.py está localizado
here = path.abspath(path.dirname(__file__))

# Abre o README.md na mesma pasta do setup.py
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ms_toolkit",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
    ],
    description="Pacote para manipulação, limpeza e visualização de dados.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Garantir que é markdown
    author="Mamadu Sama",
    author_email="mamadusama19@gmail.com",
    url="https://github.com/mamadusama/ms_toolkit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.6',
)
