# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 19:03:32 2024

@author: Luis Humberto Calderon Baldeón
"""

#%%
# Cálculo del Rendimiento al Vencimiento (YTM)
'''
El YTM (Yield to Maturity) es la tasa de descuento que iguala el precio actual de un bono con el valor presente de todos sus flujos de efectivo futuros (cupones y valor nominal). Matemáticamente, se resuelve de la siguiente manera:

[
P = \sum_{t=1}^{N} \frac{CF_t}{(1 + YTM)^t}
]

Donde:

( P ): Precio actual del bono.
( CF_t ): Flujo de efectivo en el periodo ( t ) (incluye cupones y el valor nominal al vencimiento).
( YTM ): Rendimiento al vencimiento (lo que queremos calcular).
( N ): Número total de periodos.
Como esta ecuación no se puede resolver de forma analítica, se utiliza un método numérico como Newton-Raphson para calcular el ( YTM ).
'''

def rendimiento_vencimiento(precio_bono, valor_nominal, tasa_cupon, periodos, frecuencia=1, guess=0.05, tol=1e-6, max_iter=1000):
    """
    Calcula el Rendimiento al Vencimiento (YTM) de un bono usando el método de Newton-Raphson.

    Args:
        precio_bono (float): Precio actual del bono.
        valor_nominal (float): Valor nominal del bono.
        tasa_cupon (float): Tasa de cupón anual (en porcentaje).
        periodos (int): Número total de años hasta el vencimiento.
        frecuencia (int): Frecuencia de pago de cupones (1 = anual, 2 = semestral, etc.).
        guess (float): Suposición inicial para el YTM (por defecto 5% o 0.05).
        tol (float): Tolerancia para la convergencia.
        max_iter (int): Número máximo de iteraciones.

    Returns:
        float: Rendimiento al vencimiento (YTM) en porcentaje.

    Raises:
        ValueError: Si el método no converge.
    """
    tasa_cupon /= 100
    flujo_cupon = valor_nominal * tasa_cupon / frecuencia
    periodos_totales = periodos * frecuencia
    ytm = guess

    for _ in range(max_iter):
        # Calcular el precio estimado del bono usando la suposición actual del YTM
        precio_estimado = sum(
            flujo_cupon / (1 + ytm / frecuencia) ** t for t in range(1, periodos_totales + 1)
        )
        precio_estimado += valor_nominal / (1 + ytm / frecuencia) ** periodos_totales

        # Calcular la derivada (necesaria para el método de Newton-Raphson)
        precio_derivado = sum(
            -t * flujo_cupon / frecuencia / (1 + ytm / frecuencia) ** (t + 1)
            for t in range(1, periodos_totales + 1)
        )
        precio_derivado += -periodos_totales * valor_nominal / frecuencia / (1 + ytm / frecuencia) ** (periodos_totales + 1)

        # Actualizar el YTM utilizando el método de Newton-Raphson
        ytm_nuevo = ytm - (precio_estimado - precio_bono) / precio_derivado

        # Verificar convergencia
        if abs(ytm_nuevo - ytm) < tol:
            return ytm_nuevo * 100  # Convertir a porcentaje

        ytm = ytm_nuevo

    # Si no converge, lanzar un error
    raise ValueError("El cálculo del YTM no convergió después de {} iteraciones".format(max_iter))
#%%
