# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:27:41 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
#
'''
Este archivo contiene pruebas unitarias para las funciones de duración de Macaulay y, si decides implementarla, convexidad. Usaremos también el módulo unittest.
'''
import unittest
from bonos.sensibilidad import duracion_macaulay  # Importar la función que estamos probando

class TestSensibilidad(unittest.TestCase):

    def test_duracion_macaulay_anual(self):
        """
        Prueba de la duración de Macaulay para un bono con pagos anuales.
        """
        valor_nominal = 1000
        tasa_cupon = 5  # 5% anual
        tasa_descuento = 3  # 3% anual
        periodos = 5  # 5 años
        frecuencia = 1  # Pago anual

        # La duración esperada se calcula de forma teórica
        duracion_esperada = 4.43
        duracion_calculada = duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(duracion_calculada, duracion_esperada, places=2)

    def test_duracion_macaulay_semestral(self):
        """
        Prueba de la duración de Macaulay para un bono con pagos semestrales.
        """
        valor_nominal = 1000
        tasa_cupon = 6  # 6% anual
        tasa_descuento = 4  # 4% anual
        periodos = 10  # 10 años
        frecuencia = 2  # Pago semestral

        # La duración esperada se calcula de forma teórica
        duracion_esperada = 8.33
        duracion_calculada = duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(duracion_calculada, duracion_esperada, places=2)

    def test_duracion_macaulay_sin_cupones(self):
        """
        Prueba de la duración de Macaulay para un bono sin cupones (bono cero).
        """
        valor_nominal = 1000
        tasa_cupon = 0  # Sin cupones
        tasa_descuento = 5  # 5% anual
        periodos = 10  # 10 años
        frecuencia = 1  # Pago único al vencimiento

        # Para un bono cero cupón, la duración de Macaulay es igual a los años al vencimiento
        duracion_esperada = 10
        duracion_calculada = duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(duracion_calculada, duracion_esperada, places=2)

if __name__ == "__main__":
    unittest.main()
#%%