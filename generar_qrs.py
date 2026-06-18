import pandas as pd
import qrcode
import os
import re

# CONFIGURACIÓN

# Nombre de tu archivo Excel
archivo_excel = "Asesores.xlsx"

# Nombre de la hoja de Excel
hoja = "Hoja1"

# Carpeta donde se guardarán los QR
carpeta_salida = "qrs"
os.makedirs(carpeta_salida, exist_ok=True)


def limpiar_nombre_archivo(nombre):
    """
    Limpia el nombre para que sea válido como nombre de archivo.
    Ejemplo:
    'Juan Pérez S.A.' -> 'Juan_Perez_SA'
    """
    nombre = str(nombre).strip()
    nombre = re.sub(r"[^\w\s-]", "", nombre)
    nombre = re.sub(r"\s+", "_", nombre)
    return nombre


def limpiar_numero(numero):
    """
    Convierte el número de teléfono a texto limpio.
    Ejemplo:
    938312347.0 -> 938312347
    '+51 938 312 347' -> 51938312347
    """
    numero_texto = str(numero).strip()

    # Si Excel lo leyó como decimal, ejemplo: 987123465.0
    if numero_texto.endswith(".0"):
        numero_texto = numero_texto[:-2]

    # Dejar solo números
    numero_texto = re.sub(r"\D", "", numero_texto)

    return numero_texto


# ==============================
# LEER EXCEL
# ==============================

df = pd.read_excel(archivo_excel, sheet_name=hoja)

# Validar columnas
if "Nombre" not in df.columns or "Teléfono" not in df.columns:
    raise ValueError("El Excel debe tener las columnas: Nombre y Teléfono")


# ==============================
# GENERAR QRS
# ==============================

for index, fila in df.iterrows():
    nombre = fila["Nombre"]
    numero = fila["Teléfono"]

    if pd.isna(nombre) or pd.isna(numero):
        print(f"Fila {index + 2} ignorada porque tiene datos vacíos")
        continue

    nombre_limpio = limpiar_nombre_archivo(nombre)
    numero_texto = limpiar_numero(numero)

    if numero_texto == "":
        print(f"Fila {index + 2} ignorada porque el teléfono no es válido")
        continue

    # Si el número ya empieza con 51, no le volvemos a agregar 51
    if numero_texto.startswith("51"):
        numero_whatsapp = numero_texto
    else:
        numero_whatsapp = f"51{numero_texto}"

    # Enlace de WhatsApp que irá dentro del QR
    contenido_qr = f"https://wa.me/{numero_whatsapp}"

    # Crear QR
    qr = qrcode.make(contenido_qr)

    # Guardar QR con el nombre asociado
    ruta_salida = os.path.join(carpeta_salida, f"{nombre_limpio}.png")
    qr.save(ruta_salida)

    print(f"QR generado: {ruta_salida} -> {contenido_qr}")


print("Proceso terminado.")