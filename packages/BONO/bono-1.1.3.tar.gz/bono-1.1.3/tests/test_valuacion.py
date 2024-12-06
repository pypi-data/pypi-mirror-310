# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:25:57 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
#
'''
Este archivo contiene pruebas unitarias para las funciones de cálculo del precio de un bono que se encuentran en valuacion.py. Usaremos el módulo unittest.
'''
import unittest
from bonos.valuacion import precio_bono

class TestValuacion(unittest.TestCase):
    def test_precio_bono_anual(self):
        """
        Prueba del precio de un bono con pagos anuales.
        """
        valor_nominal = 1000
        tasa_cupon = 5  # 5% anual
        tasa_descuento = 3  # 3% anual
        periodos = 5  # 5 años
        frecuencia = 1  # Pago anual

        # El precio esperado se calcula de forma teórica
        precio_esperado = 1086.07
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

    def test_precio_bono_semestral(self):
        """
        Prueba del precio de un bono con pagos semestrales.
        """
        valor_nominal = 1000
        tasa_cupon = 6  # 6% anual
        tasa_descuento = 4  # 4% anual
        periodos = 10  # 10 años
        frecuencia = 2  # Pago semestral

        # El precio esperado se calcula de forma teórica
        precio_esperado = 1104.26
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

    def test_precio_bono_cero(self):
        """
        Prueba del precio de un bono cero cupón.
        """
        valor_nominal = 1000
        tasa_cupon = 0  # Sin cupones
        tasa_descuento = 5  # 5% anual
        periodos = 5  # 5 años
        frecuencia = 1  # Pago único al vencimiento

        # El precio esperado se calcula de forma teórica
        precio_esperado = 783.53
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

if __name__ == "__main__":
    unittest.main()
#%%