# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:21:55 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
#
import unittest
from bonos.visualizacion import graficar_flujos, graficar_tasas_simuladas
import matplotlib.pyplot as plt

class TestVisualizacion(unittest.TestCase):
    def test_graficar_flujos(self):
        flujos = [100, 100, 1100]
        plazos = [1, 2, 3]
        try:
            graficar_flujos(flujos, plazos)
        except Exception as e:
            self.fail(f"graficar_flujos lanzó una excepción: {e}")

    def test_graficar_tasas_simuladas(self):
        tasas_simuladas = [0.04, 0.05, 0.06, 0.07, 0.04]
        try:
            graficar_tasas_simuladas(tasas_simuladas)
        except Exception as e:
            self.fail(f"graficar_tasas_simuladas lanzó una excepción: {e}")

if __name__ == '__main__':
    unittest.main()
#%%
