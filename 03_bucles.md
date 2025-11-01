
# Ejemplo Completo con Bucles y Ejercicios en Python

Este archivo contiene ejemplos completos y ejercicios prácticos sobre cómo utilizar bucles en Python en un contexto de administración de sistemas.

---

## Sección 1: Bucle `for` Básico

Los bucles `for` permiten iterar sobre un rango o una colección de elementos, como listas. Son ideales cuando conocemos el número de veces que queremos repetir una operación.

### Código de ejemplo:
```python
for servidor in range(1, 6):
    print(f"Comprobando disponibilidad del servidor {servidor}...")
```

---

## Sección 2: Bucle `for` con Listas

Podemos usar los bucles `for` para iterar sobre elementos de una lista. Este ejemplo simula la comprobación del estado de servicios en un servidor.

### Código de ejemplo:
```python
servicios = ["SSH", "Apache", "MySQL", "FTP", "Firewall"]

for servicio in servicios:
    print(f"Comprobando estado del servicio: {servicio}")
```

---

## Sección 3: Bucle `for` con Índice usando `enumerate()`

A veces necesitamos tanto el índice como el valor al iterar sobre una lista. Con `enumerate()`, obtenemos el índice y el valor simultáneamente.

### Código de ejemplo:
```python
for indice, servicio in enumerate(servicios):
    print(f"Servicio {indice + 1}: {servicio}")
```

---

## Sección 4: Bucle `while`

El bucle `while` se utiliza cuando no sabemos cuántas veces se debe repetir el bucle. Continúa ejecutándose mientras una condición sea verdadera.

### Código de ejemplo:
```python
logs = ["Inicio del sistema", "Conexión SSH establecida", "Actualización exitosa", "Error: Base de datos desconectada"]

i = 0
while i < len(logs):
    log = logs[i]
    print(f"Monitoreo de logs: {log}")
    if "Error" in log:
        print("¡Se ha detectado un error en el sistema! Revisar inmediatamente.")
        break
    i += 1
```

---

## Sección 5: Bucle `while` con una Condición Externa

Este ejemplo simula la monitorización de la carga del CPU de un servidor hasta que llegue a un nivel aceptable.

### Código de ejemplo:
```python
carga_cpu = 95

while carga_cpu > 75:
    print(f"Carga del CPU: {carga_cpu}% - ¡Alerta! Carga alta.")
    carga_cpu -= 5

print(f"Carga del CPU bajo control: {carga_cpu}%. Sistema estable.")
```

---

## Sección 6: Ejemplo Avanzado: Gestión de Usuarios Conectados

Este ejemplo utiliza un bucle `for` para iterar sobre una lista de usuarios y realizar diferentes acciones según su estado.

### Código de ejemplo:
```python
usuarios = [
    {"nombre": "Ana", "conectado": True},
    {"nombre": "Luis", "conectado": False},
    {"nombre": "Pedro", "conectado": True},
    {"nombre": "Marta", "conectado": False},
]

for usuario in usuarios:
    if usuario["conectado"]:
        print(f"Usuario {usuario['nombre']} está conectado. Enviando notificación de mantenimiento.")
    else:
        print(f"Usuario {usuario['nombre']} no está conectado. Omitiendo.")
```

---

## Sección Final: Autoevaluación

### Tareas:
1. Crea una lista que almacene 3 direcciones IP de servidores.
2. Usa un bucle `for` para realizar una "verificación" en cada servidor.
3. Crea una variable que represente la carga inicial del CPU de un servidor.
4. Utiliza un bucle `while` para simular la reducción gradual de la carga del CPU hasta un nivel aceptable (75%).
5. Imprime el resultado final cuando la carga del CPU sea segura.

### Código de ejemplo:
```python
servidores = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]

for servidor in servidores:
    print(f"Verificando estado del servidor {servidor}...")

carga_cpu = 90

while carga_cpu > 75:
    print(f"Carga actual del CPU: {carga_cpu}% - ¡Alerta! Reduciendo carga.")
    carga_cpu -= 5

print(f"Carga del CPU bajo control: {carga_cpu}%. Sistema estable.")
```

---

Este archivo cubre los fundamentos de los bucles en Python con ejemplos prácticos y ejercicios aplicados a la administración de sistemas.
