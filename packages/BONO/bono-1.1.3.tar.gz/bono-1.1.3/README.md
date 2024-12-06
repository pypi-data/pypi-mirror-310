
### Bond Library
A Python library for performing calculations and analyses related to financial bonds. Ideal for financial analysts, finance students, and developers interested in financial engineering.

#### Summary of Examples:
* Basic bond valuation (coupon and zero-coupon bonds).
* Calculating bond sensitivity (Macaulay duration).
* Yield to Maturity (YTM) calculation.
* Generating cash flows for bonds.
* Portfolio analysis (total value and weighted average duration).
* Yield curve analysis.

### 1. Bond Valuation
Calculate the price of bonds, including coupon bonds and zero-coupon bonds.

**Example: Valuing a bond**

```python
from bonos.valuacion import precio_bono
```
*#Inputs: Face value (nominal value), coupon rate, discount rate, periods, payment frequency*
```python
bond_price = precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=5, frecuencia=1)
print(f"The bond price is: {bond_price}")
```

**Example: Valuing a zero-coupon bond**

```python
from bonos.valuacion import precio_bono
```

*#Zero-coupon bond: coupon rate = 0*
```python
zero_coupon_price = precio_bono(valor_nominal=1000, tasa_cupon=0, tasa_descuento=4, periodos=10, frecuencia=1)
print(f"The zero-coupon bond price is: {zero_coupon_price}")
```

### 2. Bond Sensitivity
Calculate the Macaulay Duration, a measure of a bond’s sensitivity to interest rate changes.

**Example: Calculating Macaulay Duration**

```python
from bonos.sensibilidad import duracion_macaulay
```

*#Inputs: Face value, coupon rate, discount rate, periods, payment frequency*
```python
duration = duracion_macaulay(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=5, frecuencia=1)
print(f"The Macaulay duration is: {duration}")
```
**Example: Duration of a zero-coupon bond**
```python
from bonos.sensibilidad import duracion_macaulay
```
*#Zero-coupon bond: coupon rate = 0*
```python
zero_coupon_duration = duracion_macaulay(valor_nominal=1000, tasa_cupon=0, tasa_descuento=4, periodos=10, frecuencia=1)
print(f"The duration of the zero-coupon bond is: {zero_coupon_duration}")
```

### 3. Yield to Maturity (YTM)
Calculate the Yield to Maturity (YTM), which represents the bond's expected annual return if held until maturity.

**Example: Calculating YTM**
```python
from bonos.tasas import rendimiento_vencimiento
```
*#Inputs: Bond price, face value, coupon rate, periods, payment frequency*
```python
ytm = rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1)
print(f"The yield to maturity (YTM) is: {ytm}%")
```

**Example: YTM with semi-annual payments**
```python
from bonos.tasas import rendimiento_vencimiento
```
*#Semi-annual payments: frequency = 2*
```python
ytm_semi_annual = rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=2)
print(f"The semi-annual yield to maturity (YTM) is: {ytm_semi_annual}%")
```

### 4. Cash Flow Generation
Generate the cash flows of a bond, including periodic coupon payments and the redemption of the face value.

**Example: Generating cash flows**
```python
from bonos.flujos import generar_flujos
```
*#Inputs: Face value, coupon rate, periods, payment frequency*
```python
cash_flows = generar_flujos(valor_nominal=1000, tasa_cupon=5, periodos=5, frecuencia=2)
print(f"Cash flows: {cash_flows}")
```
**Example: Cash flows for a zero-coupon bond**
```python
from bonos.flujos import generar_flujos
```
*#Zero-coupon bond: coupon rate = 0*
```python
zero_coupon_flows = generar_flujos(valor_nominal=1000, tasa_cupon=0, periodos=10, frecuencia=1)
print(f"Cash flows for zero-coupon bond: {zero_coupon_flows}")
```

### 5. Advanced Example, Bond Portfolio Analysis
Combine the library's features to analyze a portfolio of bonds. For instance, calculate the total portfolio value and its weighted average duration.

**Example: Portfolio Analysis**
```python
from bonos.valuacion import precio_bono
from bonos.sensibilidad import duracion_macaulay
```
*#Define portfolio bonds*
```python
bonds = [
    {"valor_nominal": 1000, "tasa_cupon": 5, "tasa_descuento": 3, "periodos": 5, "frecuencia": 1},
    {"valor_nominal": 2000, "tasa_cupon": 4, "tasa_descuento": 3.5, "periodos": 10, "frecuencia": 2},
    {"valor_nominal": 1500, "tasa_cupon": 6, "tasa_descuento": 4, "periodos": 7, "frecuencia": 1},
]
```
*#Calculate the price and duration for each bond*
```python
portfolio_value = 0
weighted_durations = 0
for bond in bonds:
    # Calculate bond price
    price = precio_bono(
        valor_nominal=bond["valor_nominal"],
        tasa_cupon=bond["tasa_cupon"],
        tasa_descuento=bond["tasa_descuento"],
        periodos=bond["periodos"],
        frecuencia=bond["frecuencia"]
    )
    # Calculate Macaulay duration
    duration = duracion_macaulay(
        valor_nominal=bond["valor_nominal"],
        tasa_cupon=bond["tasa_cupon"],
        tasa_descuento=bond["tasa_descuento"],
        periodos=bond["periodos"],
        frecuencia=bond["frecuencia"]
    )
    # Update portfolio totals
    portfolio_value += price
    weighted_durations += price * duration
```
*#Calculate weighted average duration*
```python
weighted_average_duration = weighted_durations / portfolio_value

print(f"Total portfolio value: {portfolio_value}")
print(f"Weighted average duration: {weighted_average_duration}")
```

### 6. Advanced Example, Bond Yield Curve Analysis
You can use the library to analyze the yield curve of bonds with different maturities, calculating their YTMs and plotting the curve.

**Example: Yield Curve Analysis**
```python
from bonos.tasas import rendimiento_vencimiento
import matplotlib.pyplot as plt
```
*#Define a series of bonds with different maturities and prices*
```python
bonds = [
    {"precio_bono": 980, "valor_nominal": 1000, "tasa_cupon": 3, "periodos": 2, "frecuencia": 1},
    {"precio_bono": 950, "valor_nominal": 1000, "tasa_cupon": 4, "periodos": 5, "frecuencia": 1},
    {"precio_bono": 920, "valor_nominal": 1000, "tasa_cupon": 5, "periodos": 10, "frecuencia": 1},
    {"precio_bono": 890, "valor_nominal": 1000, "tasa_cupon": 6, "periodos": 20, "frecuencia": 1},
]
```
*#Calculate YTM for each bond and store maturities and YTMs*
```python
maturities = []
ytms = []
for bond in bonds:
    ytm = rendimiento_vencimiento(
        precio_bono=bond["precio_bono"],
        valor_nominal=bond["valor_nominal"],
        tasa_cupon=bond["tasa_cupon"],
        periodos=bond["periodos"],
        frecuencia=bond["frecuencia"]
    )
    maturities.append(bond["periodos"])
    ytms.append(ytm)
```
*#Plot the yield curve*
```python
plt.plot(maturities, ytms, marker='o')
plt.title("Bond Yield Curve")
plt.xlabel("Maturity (Years)")
plt.ylabel("Yield to Maturity (YTM)")
plt.grid()
plt.show()
```

#### License
This project is licensed under the MIT License.<p>
```python
Luis Humberto Calderon B.
UNIVERSIDAD NACIONAL DE INGENIERIA
Lima-Peru, 2024
```