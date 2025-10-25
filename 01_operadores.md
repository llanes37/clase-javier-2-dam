
# Operadores en Python

Ahora que sabes cómo trabajar con los tipos de datos básicos en Python y con las estructuras de datos integradas, comencemos a ver los operadores en Python. Los operadores son esenciales para realizar operaciones y para formar expresiones.

---

## Sección 1: Operadores aritméticos en Python

Estos operadores son:

### Código de ejemplo:
```python
# Suma
print(2+2) # 4
# Resta
print(10-2-5) # 3
# Multiplicación
print(8*3) # 24
# División
print(30/6) # 5.0 la división siempre devuelve un float
# Módulo, resto o residuo
print(21%5) # 1 
# División Entera
print(21//5) # 4 devuelve un int
# Potencia
print(2**3) # 8
```

---

## Sección 2: Operadores de comparación

Estos operadores son:

Mayor que: >

Mayor o igual que: >=

Menor que: <

Menor o igual que: <=

Igual a: ==

No igual a: !=

Estos operadores de comparación crean expresiones que evalúan a True o False. Aquí tenemos algunos ejemplos:

### Código de ejemplo:
```python
# Mayor que
print(5 > 6) # False
# Menor que
print(5 < 6) # True
# Mayor o igual que
print(8 >= 6) # True
# Menor o igual que
print(5 <= 3) # False
# Igual a
print(5 == 5) # True
# No igual a, o distinto  
print(5 != 5) # False
# Si evaluamos cadenas, lo hará por orden alfabético
print("Antonio" > "Zacarías") # False
print("Pepe" < "Pepa") # False
# Tambien variables
num1 = 4
num2 = 6
print(num1 <= num2) # True
```

---

## Sección 3: Encadenar operadores de comparación

En Python, podemos encadenar los operadores de comparación para realizar más de una comparación de forma más concisa.

Por ejemplo, esta expresión verifica si a es menor que b y si b es menor que c:

### Código de ejemplo:
```python
a = 1
b = 2
c = 3
print(a < b < c) # True
print( a >= b > c) # False
```

---

## Sección 4: Operadores lógicos

En Python tenemos tres operadores lógicos: and, or, y not. Cada uno de estos operadores tiene su propia tabla de verdad y son esenciales para trabajar con condicionales.

### Ejemplo AND, OR y NOT:
```python
# El operador and:
print(True and True) # True
print(True and False) # False
print(False and True) # False
print(False and False) # False
# El operador or:
print(True or True) # True
print(True or False) # True
print(False or True) # True
print(False or False) # False
# El operador not:
print(not True) # False
print(not False) # True
```
Estos operadores son usados para formar expresiones más complejas que combinan diferentes operaciones, valores y variables.

---

## Sección 5: Operadores de asignación

Estos operadores son usados para asignar un valor a una variable.

Ellos son: =, +=, -=, *=, %=, /=, //=, **=

El operador = asigna el valor a una variable.
Los otros operadores realizan una operación con el valor actual de la variable y el valor del lado derecho de la sentencia de asignación y asignan el resultado a la misma variable.
Por ejemplo:

### Ejemplos de asignación:
```python
# Operador de asignación =
x = 6 # x vale 6
print(x)
# Operador de asignación +=
x += 15 # ahora x vale 21 (15+6)
print(x)
# Operador de asignación -=
x -= 2 # ahora x vale 19 (21-2)
print(x)
# Operador de asignación *=
x *= 2 # ahora x vale 38 (19*2)
print(x)
# Operador de asignación %=
x %= 3 # ahora x vale 2 (es el resto de 38/3)
print(x)
# Operador de asignación /=
x=30
x /= 2 # ahora x vale 15.0 (30/2)
print(x)
# Operador de asignación //=
x //= 2 # ahora x vale 7.0 (2/2)
print(x)
# Operador de asignación **=
x **= 2 # ahora x vale 49.0 (7.0 al cuadrado)
print(x)

```

---

## Sección Final: Autoevaluación

### Tareas:
Escribe un programa en Python que realice las siguientes tareas:

<u>Entrada de Datos:</u>

1. Solicita al usuario que ingrese dos números enteros.
2. Solicita al usuario que ingrese una cadena de texto.

<u>Operaciones y Comparaciones:</u>

3. Determina si los dos números son iguales(almacena en una varable boolean para poder mostrar luego).
4. Determina si el primer número es mayor que el segundo.
5. Determina si la longitud de la cadena de texto es mayor o igual a 3 y menor que 10.
6. Calcula el resultado de sumar, restar, multiplicar y dividir los dos números.

<u>Salida de Resultados:</u>

7. Muestra los resultados de las comparaciones y operaciones en la consola.


### Código de ejemplo:
```python
# Solicitar entrada de datos
numero1 = int(input("Ingresa el primer número: "))
numero2 = int(input("Ingresa el segundo número: "))
cadena = input("Ingresa una cadena de texto: ")

# Comparaciones
son_iguales = numero1 == numero2
es_mayor = numero1 > numero2
longitud_valida = 3 <= len(cadena) < 10

# Operaciones
suma = numero1 + numero2
resta = numero1 - numero2
multiplicacion = numero1 * numero2
division = numero1 / numero2 if numero2 != 0 else "Indefinido (división por cero)"

# Mostrar resultados
print(f"¿Los números son iguales? {son_iguales}")
print(f"¿El primer número es mayor que el segundo? {es_mayor}")
print(f"¿La longitud de la cadena es válida (3-9)? {longitud_valida}")
print(f"Suma: {suma}")
print(f"Resta: {resta}")
print(f"Multiplicación: {multiplicacion}")
print(f"División: {division}")
```

---


