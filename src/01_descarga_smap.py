# Importar librerias
import earthaccess
import xarray as xr
from pathlib import Path

# Autenticación automática desde .netrc
earthaccess.login()

# Bounding box cuenca San Antonio de los Cobres
# (lon_min, lat_min, lon_max, lat_max)
bbox = (-67.5, -24.5, -66.0, -23.5)

# Buscar datos SMAP SPL3SMP últimos 30 días
results = earthaccess.search_data(
    short_name="SPL3SMP",
    version="009",
    bounding_box=bbox,
    temporal=("2025-04-01", "2025-05-22"),
    count=10
)

print(f"Archivos encontrados: {len(results)}")
for r in results:
    print(r)