# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:11:59 2024

@author: Luis Humberto Calderon Baldeón
"""
#%%
# Pruebas para las funciones en tasas.py (rendimiento al vencimiento):

import unittest
from bonos.tasas import rendimiento_vencimiento

class TestTasas(unittest.TestCase):
    def test_rendimiento_vencimiento(self):
        # Prueba con un bono de 10 años con pagos anuales
        ytm = rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1)
        self.assertAlmostEqual(ytm, 5.57, places=2)

        # Prueba con un bono de 5 años con pagos semestrales
        ytm = rendimiento_vencimiento(precio_bono=980, valor_nominal=1000, tasa_cupon=4, periodos=5, frecuencia=2)
        self.assertAlmostEqual(ytm, 4.30, places=2)

if __name__ == "__main__":
    unittest.main()
    
#%%