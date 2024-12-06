# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:08:07 2024

@author: Luis Humberto Calderon Baldeón
"""
#%%
#
'''
El archivo __init__.py inicializa el paquete y permite importar módulos o funciones directamente desde la carpeta bonos.
ejemplo: from bonos import precio_bono, duracion_macaulay
'''

# Importar las funciones clave de los módulos
from .valuacion import precio_bono
from .sensibilidad import duracion_macaulay
from .tasas import rendimiento_vencimiento
from .flujos import generar_flujos

# Especificar qué funciones estarán disponibles al importar el paquete
__all__ = [
    "precio_bono",
    "duracion_macaulay",
    "rendimiento_vencimiento",
    "generar_flujos",
]

#%%