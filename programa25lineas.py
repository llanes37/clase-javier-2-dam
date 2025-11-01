
# * Carrito de la compra con descuentos por volumen
# TODO: Permitir al usuario añadir productos y calcular el total con descuentos
# Este programa simula un carrito de la compra donde puedes añadir productos, ver el carrito y calcular el total.
# Si compras más de 5 unidades de un producto, se aplica un descuento del 10% en ese producto.

# Lista para guardar los nombres de los productos
productos = []
# Lista para guardar los precios unitarios de cada producto
precios = []
# Lista para guardar la cantidad de cada producto
cantidades = []


# Porcentaje de descuento por volumen (10%) si compras más de 5 unidades de un producto
descuento_volumen = 0.10
# Porcentaje de IVA (21%) que se suma al total
iva = 0.21

# Función para mostrar el contenido actual del carrito

# Función para mostrar el contenido actual del carrito y el descuento aplicado si corresponde
def mostrar_carrito():
    print("\n# * Carrito actual:")
    for i, (prod, prec, cant) in enumerate(zip(productos, precios, cantidades), start=1):
        linea = f"{i}. {prod} - {cant} x {prec}€"
        if cant > 5:
            descuento = prec * cant * descuento_volumen
            linea += f" | Descuento aplicado: -{round(descuento,2)}€"
        print(linea)
    print()  # Línea en blanco para separar

# Función para calcular el total a pagar, aplicando descuentos si corresponde

# Función para calcular el total a pagar, aplicando descuentos si corresponde y sumando el IVA
def calcular_total():
    total_sin_iva = 0  # Variable para acumular el total sin IVA
    descuentos = []    # Lista para guardar los descuentos aplicados
    for i in range(len(productos)):
        subtotal = precios[i] * cantidades[i]
        descuento = 0
        if cantidades[i] > 5:
            descuento = subtotal * descuento_volumen
            subtotal -= descuento
        descuentos.append(descuento)
        total_sin_iva += subtotal
    total_con_iva = total_sin_iva * (1 + iva)
    return total_con_iva, descuentos, total_sin_iva

# Bucle principal del programa: muestra el menú y gestiona las opciones

# Función para imprimir el ticket detallado de la compra
def imprimir_ticket(descuentos, total_sin_iva, total_con_iva):
    print("\n================ TICKET DE COMPRA ================")
    for i, (prod, prec, cant, desc) in enumerate(zip(productos, precios, cantidades, descuentos), start=1):
        print(f"{i}. {prod}")
        print(f"   Precio unitario: {prec}€")
        print(f"   Cantidad: {cant}")
        subtotal = prec * cant
        print(f"   Subtotal: {round(subtotal,2)}€")
        if desc > 0:
            print(f"   Descuento aplicado: -{round(desc,2)}€")
        else:
            print(f"   Descuento aplicado: 0€")
        print(f"   Subtotal con descuento: {round(subtotal-desc,2)}€")
        print("----------------------------------------")
    print(f"Total sin IVA: {round(total_sin_iva,2)}€")
    print(f"IVA (21%): {round(total_sin_iva*iva,2)}€")
    print(f"TOTAL A PAGAR: {round(total_con_iva,2)}€")
    print("==================================================\n")

while True:
    print("\n# * Menú carrito de la compra")
    print("1) Añadir producto")
    print("2) Mostrar carrito")
    print("3) Calcular total y salir")
    opcion = input("Elige opción: ")  # El usuario elige qué hacer
    if opcion == "1":
        # Opción para añadir un producto al carrito
        nombre = input("Nombre del producto: ")
        try:
            # Pedimos el precio y la cantidad, y convertimos a los tipos adecuados
            precio = float(input("Precio unitario (€): "))
            cantidad = int(input("Cantidad: "))
            # Validación para evitar números negativos o cero
            if precio <= 0 or cantidad <= 0:
                print("! No se permiten valores negativos o cero. Intenta de nuevo.")
                continue
        except ValueError:
            # Si el usuario pone algo que no es número, mostramos error y volvemos al menú
            print("! Entrada no válida. Intenta de nuevo.")
            continue  # Salta a la siguiente iteración del bucle
        # Guardamos los datos en las listas correspondientes
        productos.append(nombre)
        precios.append(precio)
        cantidades.append(cantidad)
        print(f"Producto '{nombre}' añadido.")
    elif opcion == "2":
        # Opción para mostrar el carrito actual
        mostrar_carrito()
    elif opcion == "3":
        # Opción para calcular el total y salir del programa
        mostrar_carrito()  # Mostramos el carrito antes de calcular
        total_con_iva, descuentos, total_sin_iva = calcular_total()  # Calculamos el total con descuentos y IVA
        imprimir_ticket(descuentos, total_sin_iva, total_con_iva)  # Mostramos el ticket detallado
        break  # Sale del bucle principal y termina el programa
    else:
        # Si la opción no es válida, avisamos y volvemos a pedir
        print("! Opción no válida.")
        continue
# * Fin del programa
# Este programa termina cuando el usuario elige la opción 3.