# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:20:07 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Pruebas para las funciones de cálculo de duración y convexidad.

import unittest
from bonos.riesgo import calcular_duracion, calcular_convexidad

class TestRiesgo(unittest.TestCase):
    def setUp(self):
        self.flujos = [100, 100, 1100]  # Flujos de efectivo
        self.tasas = 0.05              # Tasa de descuento (5%)
        self.plazos = [1, 2, 3]        # Plazos en años

    def test_calcular_duracion(self):
        duracion = calcular_duracion(self.flujos, self.tasas, self.plazos)
        self.assertAlmostEqual(duracion, 2.76, places=2)  # Comparando con un valor esperado

    def test_calcular_convexidad(self):
        convexidad = calcular_convexidad(self.flujos, self.tasas, self.plazos)
        self.assertAlmostEqual(convexidad, 8.25, places=2)  # Comparando con un valor esperado

if __name__ == '__main__':
    unittest.main()
#%%