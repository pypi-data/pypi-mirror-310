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
    version="1.1.4",  # Versión inicial
    description="Librería para análisis y cálculos de bonos financieros",
    long_description=open("README.md").read(),  # Lee la descripción desde README.md
    long_description_content_type="text/markdown",  # Solo aparece una vez
    url="https://github.com/LuisHCalderon",  # URL de tu repositorio
    author="Luis Humberto Calderon Baldeón",
    author_email="luis.calderon.b@uni.pe",  
    license="MIT",  # Licencia
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',          # Para cálculos matemáticos
        'matplotlib>=3.5.0',      # Para visualización de datos
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Versión mínima de Python requerida
)
#%%