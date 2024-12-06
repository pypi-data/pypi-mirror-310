# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:16:59 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Gráficos y Visualización

import matplotlib.pyplot as plt

def graficar_flujos(flujos, plazos):
    """
    Genera un gráfico de barras para visualizar los flujos de efectivo del bono.
    
    Args:
        flujos (list): Lista de flujos de efectivo.
        plazos (list): Lista de plazos correspondientes.
    """
    plt.bar(plazos, flujos, color='skyblue', edgecolor='black')
    plt.xlabel('Plazos (años)')
    plt.ylabel('Flujos de Efectivo')
    plt.title('Flujos de Efectivo del Bono')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def graficar_tasas_simuladas(tasas_simuladas):
    """
    Genera un histograma de las tasas simuladas.
    
    Args:
        tasas_simuladas (np.array): Array de tasas simuladas.
    """
    plt.hist(tasas_simuladas, bins=20, color='lightgreen', edgecolor='black')
    plt.xlabel('Tasas de Interés')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Tasas Simuladas')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

#%%
