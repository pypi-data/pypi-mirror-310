# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:05:55 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Generación de Flujos de Caja
'''
Descripción
Los flujos de caja de un bono consisten en:

Pagos periódicos de cupones, que se calculan como la tasa de cupón multiplicada por el valor nominal.
El valor nominal del bono, que se paga al vencimiento.
El flujo de caja tiene en cuenta:

Frecuencia: Si el bono paga cupones anualmente, semestralmente, trimestralmente, etc.
Duración: Número de años hasta el vencimiento.
Tasa de cupón: La tasa anual expresada como porcentaje del valor nominal.
Valor nominal: El monto principal que se paga al vencimiento.

'''

def generar_flujos(valor_nominal, tasa_cupon, periodos, frecuencia=1):
    """
    Genera los flujos de caja de un bono.

    Args:
        valor_nominal (float): Valor nominal del bono.
        tasa_cupon (float): Tasa de cupón anual (en porcentaje).
        periodos (int): Número total de años hasta el vencimiento.
        frecuencia (int): Frecuencia de pago de cupones (1 = anual, 2 = semestral, etc.).

    Returns:
        list: Lista de flujos de caja, donde cada elemento representa un pago en un periodo.
    """
    tasa_cupon /= 100  # Convertir la tasa de cupón a decimal
    flujo_cupon = valor_nominal * tasa_cupon / frecuencia
    flujos = [flujo_cupon] * (periodos * frecuencia)  # Cupones periódicos
    flujos[-1] += valor_nominal  # Agregar el valor nominal al último flujo
    return flujos
#%%