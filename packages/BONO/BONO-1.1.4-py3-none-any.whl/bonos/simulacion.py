# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:14:55 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Simulación de Escenarios

import numpy as np

def simular_tasas_inflacion(base_tasa, desviacion, num_escenarios=100):
    """
    Simula diferentes escenarios para tasas de interés basadas en una distribución normal.
    
    Args:
        base_tasa (float): Tasa de interés base (promedio esperado).
        desviacion (float): Desviación estándar de las tasas simuladas.
        num_escenarios (int): Número de escenarios a simular.
    
    Returns:
        np.array: Array con las tasas simuladas.
    """
    tasas_simuladas = np.random.normal(loc=base_tasa, scale=desviacion, size=num_escenarios)
    return tasas_simuladas

def simular_flujos_bono(flujos_originales, tasas_simuladas, plazos):
    """
    Calcula los valores presentes de los flujos de un bono bajo diferentes escenarios de tasas.
    
    Args:
        flujos_originales (list): Lista de flujos de efectivo originales del bono.
        tasas_simuladas (np.array): Array de tasas simuladas.
        plazos (list): Plazos en años correspondientes a cada flujo.
    
    Returns:
        list: Lista de valores presentes de los flujos bajo cada escenario.
    """
    escenarios_flujos = []
    for tasa in tasas_simuladas:
        flujos_descuento = [f / (1 + tasa)**t for f, t in zip(flujos_originales, plazos)]
        escenarios_flujos.append(flujos_descuento)
    return escenarios_flujos

#%%