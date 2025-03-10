import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageGrab
import pytesseract
import csv
import os
import time
from tqdm import tqdm

def procesar_screenshot(imagen):
    texto = pytesseract.image_to_string(imagen, lang='spa')
    print("Texto extraído:\n", texto)
    
    datos = {}
    # Procesar el texto extraido linea por línea
    for linea in texto.split('\n'):
        linea = linea.strip()
        print(f"Línea procesada: '{linea}'")
        
        if ':' in linea:  # Verificar si la línea tiene un ":"
            clave, valor = linea.split(':', 1) 
            clave = clave.strip() 
            valor = valor.strip()
            

            if not valor:
                print(f"Advertencia: Valor vacío detectado para '{clave}'")
                valor = "N/A"  #Asignar "N/A" si no hay valor
            
            # Almacenar solo las claves relevantes
            if clave in ['Origen génetico', 'Efecto', 'Sabor', 'Tipo de variedad', 'THC', 'CBD']:
                datos[clave] = valor
                print(f"Guardado: {clave} -> {valor}") 
        
        elif 'Tipo' in linea: 
            tipo_valores = linea.split(':', 1)
            if len(tipo_valores) > 1:
                datos['Tipo de variedad'] = tipo_valores[1].strip()
                print(f"Guardado: Tipo de variedad -> {tipo_valores[1].strip()}")

    print("Datos extraídos:", datos) 
    return datos

def procesar_imagen_portapapeles():
    img = ImageGrab.grabclipboard()
    if img is None:
        print("No se encontró ninguna imagen en el portapapeles.")
        return {}
    
    print("Procesando imagen...")
    for _ in tqdm(range(100), desc="Extrayendo información", leave=False):
        pass 
    
    datos = procesar_screenshot(img)
    return datos

def guardar_en_csv(datos_cepa):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    archivo_existe = os.path.exists('cepas.csv')
    
    print("Datos a guardar en CSV:", datos_cepa)
    
    #Extraemos la informacion por clave.
    with open('cepas.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not archivo_existe:
            writer.writerow(['Origen génetico', 'Efecto', 'Sabor', 'THC', 'CBD'])
        
        writer.writerow([
            datos_cepa.get('Origen génetico', 'N/A'),
            datos_cepa.get('Efecto', 'N/A'),
            datos_cepa.get('Sabor', 'N/A'),
            datos_cepa.get('THC', 'N/A'),
            datos_cepa.get('CBD', 'N/A')
        ])
    
    print("Datos guardados en cepas.csv a las", timestamp)

def subir_screenshot():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg"), ("Todos los archivos", "*.*")])
    if ruta_imagen:
        img = Image.open(ruta_imagen)
        especificaciones = procesar_screenshot(img)
        guardar_en_csv(especificaciones)
        messagebox.showinfo("Éxito", "La extracción se completó correctamente.")

def usar_portapapeles():
    especificaciones = procesar_imagen_portapapeles()
    if especificaciones:
        guardar_en_csv(especificaciones)
        messagebox.showinfo("Éxito", "La extracción se completó correctamente.")

root = tk.Tk()
root.title("Tabla a CSV")
root.geometry("300x200")

btn_subir = tk.Button(root, text="Subir Screenshot", command=subir_screenshot)
btn_subir.pack(expand=True, pady=10)

btn_portapapeles = tk.Button(root, text="Pegar imagen", command=usar_portapapeles)
btn_portapapeles.pack(expand=True, pady=10)

root.mainloop()