#dependencias
import os
import shutil
import glob
from pathlib import Path

ruta_c = 'data'

#funciones
def capturar_shapefile():
    origen_dir = os.path.expanduser('~/Downloads/RedVial/')
    destino_dir = Path(ruta_c) / "RedVial"
    nombre_capa = 'RedVial'

    if not os.path.exists(destino_dir):
        os.makedirs(destino_dir)

    # Buscar todos los archivos que empiezan con el nombre_capa
    archivos_a_copiar = glob.glob(os.path.join(origen_dir, f"{nombre_capa}.*"))

    if archivos_a_copiar:
        for archivo in archivos_a_copiar:
            shutil.copy(archivo, destino_dir)
            print(f"Copiado: {os.path.basename(archivo)}")
        print("Capa Shapefile actualizada correctamente.")
    else:
        print(f"No se encontraron archivos para {nombre_capa} en el origen.")

def capturar_csv(nombre_archivo):
    origen = Path.home() / "Downloads" / nombre_archivo
    destino_carpeta = Path(ruta_c)
    destino_archivo = destino_carpeta / nombre_archivo

    destino_carpeta.mkdir(parents=True, exist_ok=True)

    if origen.exists():
        shutil.copy2(origen, destino_archivo)
        print(f"Archivo {origen.name} copiado a {destino_carpeta}/")
        print("Datos actualizados correctamente.")
    else:
        print(f"Error: No se encontró el archivo en {origen}")

#main
if __name__ == "__main__":
    capturar_shapefile()
    capturar_csv("miercoles_rm.csv")
    capturar_csv("DatosSII_Completos.csv")