# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:01:10 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Cálculo de la duración de Macaulay
'''
La Duración de Macaulay es una medida de la sensibilidad del precio de un bono a los cambios en las tasas de interés. Representa el tiempo promedio ponderado en el que se reciben los flujos de efectivo del bono. La fórmula para calcularla es:

[
\text{Duración de Macaulay} = \frac{\sum_{t=1}^{N} \left( \frac{t \cdot CF_t}{(1 + r)^t} \right)}{\sum_{t=1}^{N} \left( \frac{CF_t}{(1 + r)^t} \right)}
]

Donde:

( CF_t ): Flujo de efectivo en el periodo ( t ) (incluye cupones y el valor nominal al final).
( r ): Tasa de descuento por periodo.
( N ): Número total de periodos.
'''

def duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia=1):
    """
    Calcula la duración de Macaulay de un bono.

    Args:
        valor_nominal (float): Valor nominal del bono.
        tasa_cupon (float): Tasa de cupón anual (en porcentaje).
        tasa_descuento (float): Tasa de descuento anual (en porcentaje).
        periodos (int): Número total de años hasta el vencimiento.
        frecuencia (int): Frecuencia de pago de cupones (1 = anual, 2 = semestral, etc.).

    Returns:
        float: Duración de Macaulay del bono.
    """
    tasa_cupon /= 100
    tasa_descuento /= 100
    flujo_cupon = valor_nominal * tasa_cupon / frecuencia
    periodos_totales = periodos * frecuencia
    tasa_periodo = tasa_descuento / frecuencia

    # Calcular los flujos de efectivo descontados y sus pesos temporales
    flujos_descuentados = [
        (t, flujo_cupon / (1 + tasa_periodo) ** t) for t in range(1, periodos_totales + 1)
    ]
    flujos_descuentados.append((periodos_totales, valor_nominal / (1 + tasa_periodo) ** periodos_totales))

    # Numerador: Suma de tiempos ponderados por los flujos descontados
    numerador = sum(t * flujo for t, flujo in flujos_descuentados)

    # Denominador: Suma total de los flujos descontados
    denominador = sum(flujo for _, flujo in flujos_descuentados)

    # Calcular la duración de Macaulay
    duracion = numerador / denominador

    return duracion
#%%