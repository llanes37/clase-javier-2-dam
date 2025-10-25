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


a = 1
b = 2
c = 3
print(a < b < c) # True
print( a >= b > c) # False

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
