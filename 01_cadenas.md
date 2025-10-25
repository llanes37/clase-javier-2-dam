
# Cadenas en Python

Las cadenas de caracteres son muy útiles en Python. Ellas están formadas por una secuencia de caracteres y se usan para representar texto en el código. Por ejemplo:

---

## Sección 1: Cadenas de caracteres


### Código de ejemplo:
```python
"¡Hola, Mundo!"
'¡Hola, Mundo!'
"45678"
"mi-correo@email.com"
"#MeEncantaPython"
```

---

## Sección 2: Comillas dentro de cadenas de caracteres

Si definimos una cadena de caracteres con comillas dobles "", entonces podemos usar comillas simples dentro de la cadena de caracteres. Por ejemplo:

### Código de ejemplo:
```python
print("Mi asignatura favorita es 'Fundamentos de programación'")
print('Mi asignatura favorita es "Fundamentos de programación"')
```

---

## Sección 3: Indexación de cadenas de caracteres

Podemos usar índices para acceder a los caracteres de una cadena de caracteres en nuestro programa. Un índice es un número entero que representa una posición específica en la cadena de caracteres. Cada índice está asociado al carácter ubicado en esa posición. Por ejemplo, este es un diagrama de la cadena de caracteres "Hola":

### Código de ejemplo:
```python
# Cadena:    H o l a 
# Índices:   0 1 2 3
cadena = "Hola"
print(cadena[0])
print(cadena[1])
print(cadena[2])
print(cadena[3])
# print(cadena[4])   este código produciría error ya que no existe el índice 4
```
También podemos usar índices negativos para acceder a estos caracteres de derecha a izquierda:
### Índeces negativos:
```python
# Cadena:     H  o  l  a 
# Índices:   -4 -3 -2 -1
cadena = "Hola"
print(cadena[-1]) # Dato:comúnmente usamos el índice -1 para acceder al último carácter de una cadena de caracteres.
print(cadena[-2])
print(cadena[-3])
print(cadena[-4])
```
---

## Sección 4: Truncado o rebanado de cadenas de caracteres

En Python podemos obtener una rebana de una cadena de caracteres (un subconjunto de sus caracteres) de esta forma:

### Crear subconjuntos de las cadenas de caracteres:
```python
# variable_con_cadena[inicio:fin:paso]
```
inicio: es el índice del primer carácter que será incluido en la rebanada. Por defecto, su valor es 0, así que la rebanada iniciaría desde el primer carácter de la cadena.

fin: es el índice del último carácter en la rebanada (este carácter no será incluido). Por defecto, es el último carácter de la cadena (si omitimos este valor, el último carácter también será incluido).

paso: epresenta cuánto se le sumará al índice actual para alcanzar el índice del próximo carácter de la rebanada. Básicamente determina si se van a "saltar" caracteres antes de incluir el próximo carácter.

Para usar el valor por defecto de paso (1) debemos especificar solo dos valores (argumentos). Esto incluirá todos los caracteres entre los índices de inicio y fin (sin incluir este último carácter):
### Ejemplos de truncado de cadenas:
```python
cadena = "cadenaDeTexto"
print(cadena[2:8]) 
print(cadena[2:8:1]) 
print(cadena[0:4])
print(cadena[0:12:2]) 
print(cadena[0:20]) # aunque nos pasemos de indice en el fin el código sigue funcionando
```
---

## Sección 5: Métodos de cadenas de caracteres

Las cadenas de caracteres también tienen métodos, los cuales nos permiten realizar funcionalidad común que ya fue implementada en Python por los creadores del lenguaje, así que podemos usarlos en nuestros programas directamente. Son muy útiles. Esta es la sintaxis general para llamar a un método en Python:

### Métodos más importantes de cadenas de texto:
```python
# cadena.metodo(argumentos)
cadena = 'cadenaDeTexto'

# Capitalize: devuelve una copia del string con su primer carácter en mayúsculas y el resto en minúsculas.
print(cadena.capitalize())

# Count: devolverá el recuento de un elemento determinado en la lista que le pasemos por argumento.
print(cadena.count('e'))

# Find: para encontrar el índice de la primera ocurrencia de una subcadena de la cadena dada. 
print(cadena.find('e'))

# Lower: devuelve una copia de la cadena en minúsculas.
print(cadena.lower())

# Upper: devuelve una copia de la cadena en mayúsculas.
print(cadena.upper())

# Replace: devuelve una copia del string tras reemplazar las apariciones del primer argumeto por el segundo.
print(cadena.replace("e", "i"))

# Split: devuelve una lista de subcadenas cuyo separador será el caracter que le pasemos por argumento.
cadena = 'Esto es una cadena de texto'
lista_palabras = cadena.split(" ")
print(lista_palabras)
# La funcion len(lista) devuelve el nmero de elementos de una lista.
print("La cadena de texto tiene:", len(lista_palabras), "palabras.")
```

---

## Sección Final: Autoevaluación

### Tareas:
Una persona normal, lee una media de 2 palabras por segundo. Sin embargo, un locutor de radio, es capaz de leer un 30% más rápido. Teniendo en cuenta estos datos, realizar un programa en lenguaje Python, que realice lo siguiente:
1. Solicitar al usuario que inserte un texto por consola (cadena de texto).
2. Calcular las palabras escritas por el usuario y el tiempo que tardaría en leerlas una persona normal. En caso de que el tiempo sea superior a 30 segundos, mostrar un mensaje con consola.
3. Los resultados se mostrarán con el siguiente formato (ejemplo):

    Escribiste 14 palabras, y tardarías 7.0 segundos en leerlo.

    ¡Menudo testamento! (solo en caso de que el tiempo sea superior a 30 segundos)

    El locutor de radio, lo leería en 4.9 segundos.

4. Nótese que los datos decimales, se muestran con un solo decimal.


### Código de ejemplo:
```python
cadena = input("Introduzca el texto a analizar:")
lista_palabras = cadena.split(" ")
tiempo = len(lista_palabras)/2
print(f"Escribiste {len(lista_palabras)} palabras, y tardarías {tiempo} segundos en leerlo.")
if tiempo > 30:
    print("¡Menudo testamento!")
print(f"El locutor de radio, lo leería en {round((tiempo*0.7),1)} segundos.")
```

---


