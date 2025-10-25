


## Sección 1: Condicionales Básicos

Las condiciones en Python permiten tomar decisiones en base a una expresión que puede ser verdadera o falsa. En este ejemplo, simulamos la planificación de actividades según el clima.

### Código de ejemplo:
```python
clima = input("¿Cómo está el clima? (soleado/lluvioso): ").lower()
# Variable predefinida
clima_predefinido = "lluvioso"

if clima == "soleado":
    print("Puedes salir a pasear.")
else:
    print("Mejor quédate en casa.")
```

---

## Sección 2: Condiciones Múltiples con `elif`

El `elif` permite evaluar más opciones cuando la primera condición no se cumple. En este ejemplo, decidimos qué transporte usar según la distancia.

### Código de ejemplo:
```python
distancia = int(input("Introduce la distancia al destino (km): "))
# Variable predefinida
distancia_predefinida = 8

if distancia < 2:
    print("Puedes caminar.")
elif distancia <= 10:
    print("Usa una bicicleta.")
else:
    print("Toma un coche o transporte público.")
```

---

## Sección 3: Condiciones Anidadas

Las condiciones anidadas evalúan una condición dentro de otra. Este ejemplo ayuda a decidir si se necesita una chaqueta dependiendo del clima y la temperatura.

### Código de ejemplo:
```python
clima = input("¿Cómo está el clima? (soleado/lluvioso): ").lower()
temperatura = int(input("¿Cuál es la temperatura (°C)?: "))
# Variables predefinidas
clima_predefinido = "lluvioso"
temperatura_predefinida = 12

if clima == "lluvioso":
    if temperatura < 15:
        print("Lleva una chaqueta y un paraguas.")
    else:
        print("Solo necesitas un paraguas.")
else:
    print("Disfruta del sol.")
```

---

## Sección 4: Operadores de Comparación y Lógicos

Combinamos operadores de comparación (`>`, `<`, `>=`, `<=`) y lógicos (`and`, `or`) para tomar decisiones más complejas. En este ejemplo, decidimos si es seguro salir.

### Código de ejemplo:
```python
clima = input("¿Cómo está el clima? (soleado/lluvioso): ").lower()
temperatura = int(input("¿Cuál es la temperatura (°C)?: "))
# Variables predefinidas
clima_predefinido = "soleado"
temperatura_predefinida = 25

if clima == "soleado" and temperatura > 20:
    print("Es un buen día para salir.")
elif clima == "lluvioso" or temperatura < 10:
    print("Mejor quédate en casa.")
else:
    print("Sal si te sientes cómodo.")
```

---

## Sección 5: Evaluación Combinada

Evaluamos múltiples factores para decidir si asistir a un evento al aire libre.

### Código de ejemplo:
```python
clima = input("¿Cómo está el clima? (soleado/lluvioso): ").lower()
temperatura = int(input("¿Cuál es la temperatura (°C)?: "))
horario = input("¿El evento es de día o de noche?: ").lower()
# Variables predefinidas
clima_predefinido = "soleado"
temperatura_predefinida = 18
horario_predefinido = "día"

if clima == "soleado" and temperatura > 15 and horario == "día":
    print("Asiste al evento.")
else:
    print("Considera quedarte en casa.")
```

---

## Sección Final: Autoevaluación

### Tareas:
1. Solicita al usuario que introduzca una actividad planeada.
2. Pide el clima y la temperatura del día.
3. Verifica si las condiciones son adecuadas para realizar la actividad.
4. Muestra una recomendación basada en las condiciones.

### Código de ejemplo:
```python
actividad = input("¿Qué actividad planeas realizar?: ")
clima = input("¿Cómo está el clima? (soleado/lluvioso): ").lower()
temperatura = int(input("¿Cuál es la temperatura (°C)?: "))

print(f"Actividad: {actividad}")
print(f"Clima: {clima}")
print(f"Temperatura: {temperatura}°C")

if clima == "soleado" and temperatura > 20:
    print("Es un buen momento para realizar la actividad.")
else:
    print("Tal vez debas esperar mejores condiciones.")
```

---

Este archivo cubre los fundamentos de los condicionales en Python con ejemplos prácticos aplicados a situaciones cotidianas.
