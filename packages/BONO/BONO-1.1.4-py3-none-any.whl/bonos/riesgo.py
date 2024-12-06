# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:13:21 2024

@author: Luis Humberto Calderon Baldeón
"""
#%%

# Cálculo de Duración y Convexidad

def calcular_duracion(flujos, tasas, plazos):
    """
    Calcula la duración de un bono.
    
    Args:
        flujos (list): Lista de flujos de efectivo.
        tasas (float): Tasa de descuento.
        plazos (list): Plazos en años para cada flujo.

    Returns:
        float: Duración del bono.
    """
    valor_presente = sum([f / (1 + tasas)**t for f, t in zip(flujos, plazos)])
    duracion = sum([(t * f) / (1 + tasas)**t for f, t in zip(flujos, plazos)]) / valor_presente
    return duracion

def calcular_convexidad(flujos, tasas, plazos):
    """
    Calcula la convexidad de un bono.
    
    Args:
        flujos (list): Lista de flujos de efectivo.
        tasas (float): Tasa de descuento.
        plazos (list): Plazos en años para cada flujo.

    Returns:
        float: Convexidad del bono.
    """
    valor_presente = sum([f / (1 + tasas)**t for f, t in zip(flujos, plazos)])
    convexidad = sum([(t * (t + 1) * f) / (1 + tasas)**(t + 2) for f, t in zip(flujos, plazos)]) / valor_presente
    return convexidad
#%%