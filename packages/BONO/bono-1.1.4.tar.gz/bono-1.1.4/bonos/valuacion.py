# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 18:57:40 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Precio de un bono con cupones
'''
El precio de un bono se calcula como la suma del valor presente de los pagos de cupones y el valor presente del valor nominal.
'''
def precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia=1):
    """
    Calcula el precio de un bono con cupones.

    Args:
        valor_nominal (float): Valor nominal del bono.
        tasa_cupon (float): Tasa de cupón anual (en porcentaje).
        tasa_descuento (float): Tasa de descuento anual (en porcentaje).
        periodos (int): Número total de períodos hasta el vencimiento.
        frecuencia (int): Frecuencia de pago de cupones (1 = anual, 2 = semestral, etc.).

    Returns:
        float: Precio del bono.
    """
    tasa_cupon /= 100
    tasa_descuento /= 100
    flujo_cupon = valor_nominal * tasa_cupon / frecuencia
    precio = sum(flujo_cupon / (1 + tasa_descuento / frecuencia) ** t for t in range(1, periodos * frecuencia + 1))
    precio += valor_nominal / (1 + tasa_descuento / frecuencia) ** (periodos * frecuencia)
    return precio
#%%