# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 22:22:53 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
#Pruebas para las funciones de comparación de bonos y selección del mejor bono.

import unittest
from bonos.optimizacion import comparar_bonos

class TestOptimizacion(unittest.TestCase):
    def setUp(self):
        # Configuramos algunos bonos ficticios para la prueba
        self.bonos = [
            {'flujos': [100, 100, 1100], 'plazos': [1, 2, 3]},  # Bono 1
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono 2
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono 3
        ]
        self.tasa_descuento = 0.05  # 5%

    def test_comparar_bonos(self):
        # Llamamos a la función para comparar los bonos
        mejor_bono = comparar_bonos(self.bonos, self.tasa_descuento)
        
        # Verificamos que el bono con el mayor Valor Presente Neto es el Bono 3
        self.assertEqual(mejor_bono['bono'], self.bonos[2])  # Verificar que seleccionó el bono correcto
        self.assertAlmostEqual(mejor_bono['vpn'], 1464.11, places=2)  # Verificar el VPN del mejor bono

if __name__ == '__main__':
    unittest.main()
#%%