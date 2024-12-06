# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:17:55 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Comparación y Selección de Bonos
# Analiza y elige el mejor bono según ciertos criterios.

def comparar_bonos(bonos, tasas_descuento):
    """
    Compara múltiples bonos y selecciona el mejor basado en el Valor Presente Neto (VPN).
    
    Args:
        bonos (list): Lista de bonos, donde cada bono es un diccionario {'flujos': [...], 'plazos': [...]}
        tasas_descuento (float): Tasa de descuento aplicada a todos los bonos.
    
    Returns:
        dict: Bono con el mayor VPN.
    """
    resultados = []
    for bono in bonos:
        flujos = bono['flujos']
        plazos = bono['plazos']
        vpn = sum([f / (1 + tasas_descuento)**t for f, t in zip(flujos, plazos)])
        resultados.append({'bono': bono, 'vpn': vpn})
    
    # Seleccionar el bono con el mayor VPN
    mejor_bono = max(resultados, key=lambda x: x['vpn'])
    return mejor_bono

#%%