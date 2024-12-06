from setuptools import setup, find_packages

setup(
    name="ms_toolkit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
    ],
    description="Pacote para manipulação, limpeza e visualização de dados.",
    author="Mamadu Sama",
    author_email="mamadusama19@gmail.com",
    url="https://github.com/mamadusama/ms_toolkit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
