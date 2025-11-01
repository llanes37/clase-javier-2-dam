# * Programa: generadorprecio.py
# * Descripción: Programa interactivo que solicita productos y precios, aplica un
# * descuento del 15% por producto cuando el subtotal de ese producto supera 50€
# * y genera un ticket con desgloses por producto y totales.

def sumar(a, b):
    """Devuelve la suma de a y b."""
    return a + b


def aplicar_descuento(total, dto_pct):
    """Aplica un descuento porcentual (dto_pct) sobre total y devuelve (total_desc, descuento)."""
    descuento = total * dto_pct / 100
    return total - descuento, descuento


def es_par(n):
    """Devuelve True si n es par."""
    try:
        return int(n) % 2 == 0
    except Exception:
        return False


def pedir_productos():
    """Pide al usuario los productos (nombre, precio, cantidad).
    Pulsa ENTER en el nombre para terminar.
    Devuelve una lista de tuplas: (nombre, precio, cantidad, subtotal, descuento, total_producto)
    """
    productos = []
    DTO_POR_PRODUCTO = 15  # porcentaje

    while True:
        nombre = input("Nombre del producto (ENTER para terminar): ").strip()
        if nombre == "":
            break
        try:
            precio = float(input("Precio unitario (€): ").strip())
            if precio < 0:
                print("El precio no puede ser negativo. Intenta de nuevo.")
                continue
        except Exception:
            print("Precio no válido. Intenta de nuevo.")
            continue
        try:
            cantidad = int(input("Cantidad: ").strip())
            if cantidad <= 0:
                print("La cantidad debe ser un entero positivo. Intenta de nuevo.")
                continue
        except Exception:
            print("Cantidad no válida. Intenta de nuevo.")
            continue

        subtotal = precio * cantidad
        # Aplica descuento del 15% si el subtotal del producto supera 50€
        if subtotal > 50:
            total_producto, descuento = aplicar_descuento(subtotal, DTO_POR_PRODUCTO)
        else:
            total_producto, descuento = subtotal, 0.0

        productos.append((nombre, precio, cantidad, round(subtotal, 2), round(descuento, 2), round(total_producto, 2)))
        print(f"Añadido: {nombre} | {cantidad} x {precio:.2f}€ → subtotal {subtotal:.2f}€, descuento {descuento:.2f}€")

    return productos


def generar_ticket(productos):
    """Imprime el ticket completo con desglose por producto y totales."""
    print("\n================== TICKET DE COMPRA ==================")
    total_bruto = 0.0
    total_descuentos = 0.0
    total_neto = 0.0

    for i, (nombre, precio, cantidad, subtotal, descuento, total_producto) in enumerate(productos, start=1):
        print(f"{i}. {nombre}")
        print(f"   Precio unitario: {precio:.2f}€")
        print(f"   Cantidad: {cantidad}")
        print(f"   Subtotal: {subtotal:.2f}€")
        print(f"   Descuento aplicado: {descuento:.2f}€")
        print(f"   Total producto: {total_producto:.2f}€")
        print("----------------------------------------------------")
        total_bruto += subtotal
        total_descuentos += descuento
        total_neto += total_producto

    print(f"TOTAL BRUTO: {total_bruto:.2f}€")
    print(f"TOTAL DESCUENTOS: -{total_descuentos:.2f}€")
    print(f"TOTAL A PAGAR: {total_neto:.2f}€")
    print("====================================================\n")


if __name__ == "__main__":
    print("Generador de precios - Añade productos para generar el ticket")
    productos = pedir_productos()
    if not productos:
        print("No se han añadido productos. Saliendo.")
    else:
        generar_ticket(productos)
