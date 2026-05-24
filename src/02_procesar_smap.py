#Importtar librerias
import earthaccess
import h5py
import numpy as np
import pandas as pd
from pathlib import Path
import pathlib   # nuevo import

# --- Determinar rutas absolutas ---
SCRIPT_DIR = pathlib.Path(__file__).parent.resolve()   # carpeta donde está este script (src/)
PROJECT_DIR = SCRIPT_DIR.parent                        # carpeta raíz del proyecto
DATA_DIR = PROJECT_DIR / "data" / "raw"                # datos crudos fuera de src
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"     # datos procesados fuera de src

earthaccess.login()

# --- Configuración ---
bbox = (-67.5, -24.5, -66.0, -23.5)  # cuenca San Antonio de los Cobres
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Buscar y descargar archivos recientes ---
results = earthaccess.search_data(
    short_name="SPL3SMP",
    version="009",
    bounding_box=bbox,
    temporal=("2024-04-01", "2025-04-30"),
    count=30
)

print(f"Descargando {len(results)} archivos...")
files = earthaccess.download(results, local_path=DATA_DIR)
print(f"Archivos descargados: {files}")

# --- Función para extraer humedad en nuestra cuenca ---
def extraer_humedad_cuenca(filepath, bbox):
    """
    Extrae el valor medio de humedad de suelo (soil_moisture)
    del producto SPL3SMP para el bounding box dado.
    """
    lon_min, lat_min, lon_max, lat_max = bbox

    with h5py.File(filepath, 'r') as f:
        # SPL3SMP tiene dos pasadas: AM y PM
        # Usamos AM que es más confiable para humedad de suelo
        grupo = f['Soil_Moisture_Retrieval_Data_AM']

        sm     = grupo['soil_moisture'][:]          # humedad de suelo
        lats   = grupo['latitude'][:]
        lons   = grupo['longitude'][:]
        flags  = grupo['retrieval_qual_flag'][:]     # control de calidad

        # Reemplazar valores inválidos (-9999.0) con NaN
        sm = np.where(sm == -9999.0, np.nan, sm)

        # Máscara: dentro del bounding box Y calidad OK (flag == 0)
        mascara = (
            (lats >= lat_min) & (lats <= lat_max) &
            (lons >= lon_min) & (lons <= lon_max) &
            (flags == 0)
        )

        valores = sm[mascara]
        fecha = filepath.stem.split('_')[4]  # extrae fecha del nombre

        if len(valores) == 0:
            print(f"  {fecha}: sin datos válidos en la cuenca")
            return None

        print(f"  {fecha}: {len(valores)} píxeles válidos | "
              f"humedad media = {np.nanmean(valores):.4f} m³/m³")

        return {
            'fecha': pd.to_datetime(fecha, format='%Y%m%d'),
            'sm_media': np.nanmean(valores),
            'sm_min':   np.nanmin(valores),
            'sm_max':   np.nanmax(valores),
            'n_pixeles': len(valores)
        }

# --- Procesar archivos descargados ---
registros = []
for f in sorted(DATA_DIR.glob("*.h5")):
    resultado = extraer_humedad_cuenca(f, bbox)
    if resultado:
        registros.append(resultado)

# --- Guardar resultado ---
if registros:
    df = pd.DataFrame(registros).sort_values('fecha')
    out = PROCESSED_DIR / "smap_cuenca.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"\nGuardado en {out}")
    print(df)
else:
    print("\nNo se encontraron datos válidos en la cuenca.")