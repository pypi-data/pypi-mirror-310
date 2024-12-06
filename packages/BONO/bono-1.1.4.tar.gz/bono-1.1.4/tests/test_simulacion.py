# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:21:08 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%

#Pruebas para las funciones de simulación de tasas y flujos.
import unittest
import numpy as np
from bonos.simulacion import simular_tasas_inflacion, simular_flujos_bono

class TestSimulacion(unittest.TestCase):
    def test_simular_tasas_inflacion(self):
        tasas_simuladas = simular_tasas_inflacion(base_tasa=0.05, desviacion=0.01, num_escenarios=1000)
        self.assertEqual(len(tasas_simuladas), 1000)  # Asegura que se generan 1000 escenarios
        self.assertAlmostEqual(np.mean(tasas_simuladas), 0.05, delta=0.01)  # Promedio cerca de la tasa base

    def test_simular_flujos_bono(self):
        flujos = [100, 100, 1100]
        plazos = [1, 2, 3]
        tasas_simuladas = [0.04, 0.05, 0.06]
        escenarios = simular_flujos_bono(flujos, tasas_simuladas, plazos)
        self.assertEqual(len(escenarios), 3)  # Tres escenarios generados
        self.assertAlmostEqual(escenarios[0][2], 937.87, places=2)  # Valor presente del flujo final bajo 4%

if __name__ == '__main__':
    unittest.main()

#%%