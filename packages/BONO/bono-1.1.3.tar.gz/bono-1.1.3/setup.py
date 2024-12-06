# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:16:25 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
#

from setuptools import setup, find_packages

setup(
    name="BONO",  # Nombre del paquete
    version="1.1.3",  # Versión inicial
    description="Librería para análisis y cálculos de bonos financieros",
    long_description=open("README.md").read(),  # Lee la descripción desde README.md
    long_description_content_type="text/markdown",
    url="https://github.com/LuisHCalderon",  # URL de tu repositorio
    author="Luis Humberto Calderon Baldeón",
    author_email="luis.calderon.b@uni.pe",  
    license="MIT",  # Licencia (por ejemplo, MIT)
    packages=find_packages(),  # Encuentra automáticamente los paquetes en tu proyecto
    install_requires=[
        "numpy>=1.21.0",  # Dependencias necesarias
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires='>=3.7',  # Versión mínima de Python requerida
)
#%%