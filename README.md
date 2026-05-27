# AquaGuard NOA
## Sistema satelital de predicción de estrés hídrico y riesgo territorial en cuencas mineras del NOA

> **Hackathon:** Desafío Argentina al Espacio — ConstelAR Space  
> **Desafío:** Comando Galáctico — Economía, Derecho y Políticas Espaciales  
>  **Equipo:** SatLab
> **Sede:** Salta Capital  
> **Fecha:** 23 y 24 de mayo de 2026  
> **Autor:** Abraham Tartalos  

---

## Índice

1. [Problema y contexto territorial](#1-problema-y-contexto-territorial)
2. [Propuesta de solución](#2-propuesta-de-solución)
3. [Datos utilizados y justificación](#3-datos-utilizados-y-justificación)
4. [Arquitectura del sistema](#4-arquitectura-del-sistema)
5. [Desarrollo técnico — Log de avance](#5-desarrollo-técnico--log-de-avance)
6. [Modelo de impacto económico](#6-modelo-de-impacto-económico)
7. [Resultados y visualizaciones](#7-resultados-y-visualizaciones)
8. [Limitaciones y trabajo futuro](#8-limitaciones-y-trabajo-futuro)
9. [Referencias](#9-referencias)
10. [Cómo ejecutar el proyecto](#10-cómo-ejecutar-el-proyecto)

---

## 1. Problema y contexto territorial

### 1.1 El agua en el NOA: un recurso bajo presión

El Noroeste Argentino (NOA), y Salta en particular, concentra una paradoja crítica: es una región con enorme riqueza mineral estratégica (litio, boratos, cobre, sal) y al mismo tiempo una de las zonas con mayor escasez y vulnerabilidad hídrica del país. Las cuencas que nacen en la Puna salteña, por encima de los 3.500 msnm, no son solo fuentes de agua para comunidades de altura. Son el origen del sistema hídrico que irriga el Valle de Lerma, la región agrícola más productiva de Salta, a más de 200 kilómetros de distancia.

Esta dependencia hidrológica entre altura y valle es poco visible, poco monitoreada, y casi completamente ignorada en la toma de decisiones sobre concesiones mineras.

### 1.2 Área de estudio: cuenca alta del río San Antonio de los Cobres

El área de estudio primaria de AquaGuard NOA es la **cuenca alta del río San Antonio de los Cobres**, ubicada en el departamento Los Andes, Salta, a una altitud promedio de 3.800 msnm.

Esta cuenca fue seleccionada por la intersección de tres condiciones únicas:

- **Actividad minera activa y documentada:** la zona concentra explotaciones de boratos (Tincalayu), sal y minerales industriales, con presencia de operaciones que utilizan agua en procesos extractivos y de procesamiento.
- **Comunidades puneñas con dependencia hídrica directa:** la localidad de San Antonio de los Cobres (aproximadamente 5.000 habitantes según INDEC 2022) y comunidades kollas y atacameñas aledañas dependen de fuentes de agua superficial y subterránea cuya disponibilidad no cuenta con monitoreo continuo.
- **Conexión hidrológica con el Valle de Lerma:** el río San Antonio de los Cobres tributa al sistema del Pasaje-Juramento, que constituye la principal fuente de agua de riego de la agricultura salteña aguas abajo. Un evento de estrés hídrico o contaminación en la cuenca alta tiene efectos económicos medibles a 200 km de distancia.

### 1.3 El problema concreto que AquaGuard NOA resuelve

Hoy, no existe ningún sistema integrado y continuo que monitoree el estado hídrico de estas cuencas de altura en relación con la actividad minera. Las consecuencias son:

- **Para las comunidades:** no tienen datos objetivos para negociar o disputar el uso del agua frente a operadores mineros. La asimetría de información es total.
- **Para los gobiernos provinciales y municipales:** toman decisiones sobre concesiones y permisos ambientales sin una línea de base hídrica satelital confiable.
- **Para los agricultores del Valle de Lerma:** no pueden anticipar períodos de estrés hídrico originados en la cuenca alta, lo que les impide tomar decisiones preventivas de siembra, riego o cosecha.
- **Para las empresas mineras:** la ausencia de monitoreo continuo las expone a riesgos legales y reputacionales ante cualquier evento hídrico, sin evidencia objetiva de su impacto real.

### 1.4 Por qué los satélites son la solución correcta

Las cuencas de la Puna salteña son inaccesibles durante gran parte del año. La infraestructura de estaciones meteorológicas e hidrológicas en la región es escasa y discontinua. El monitoreo in situ tradicional es costoso, lento, y geográficamente incompleto.

Los satélites con capacidad de observación radar, como **SAOCOM** (desarrollado por Argentina), pueden observar la superficie terrestre independientemente de las condiciones climáticas, de noche y a través de nubes. Esta característica es especialmente valiosa en la Puna, donde la cobertura nubosa durante la temporada de lluvias (diciembre-marzo) impide el monitoreo óptico convencional.

Argentina ya tiene esa capacidad. AquaGuard NOA propone usarla.

---

## 2. Propuesta de solución

### 2.1 Concepto general

AquaGuard NOA es un **sistema satelital de predicción de estrés hídrico y riesgo territorial** que integra múltiples fuentes de datos espaciales para generar alertas tempranas, índices de vulnerabilidad y proyecciones de impacto económico en cuencas mineras del NOA argentino.

El sistema no es un visor de imágenes satelitales. Es una **herramienta de decisión**: transforma datos crudos de satélite en información accionable para gobiernos, comunidades, productores y operadores mineros.

### 2.2 Funcionamiento en tres capas

**Capa 1 — Observación continua**

El sistema ingiere de forma periódica datos de humedad de suelo (SMAP, SAOCOM), cobertura hídrica superficial (Sentinel-2), y variables climáticas (precipitación ERA5, temperatura). Estos datos se procesan y normalizan sobre la cuenca de estudio.

**Capa 2 — Modelado predictivo**

Sobre la serie temporal de variables observadas, el sistema calcula:

- **Índice de Estrés Hídrico (IEH):** anomalía de humedad de suelo respecto al baseline histórico del mismo período estacional, combinada con el índice NDWI de cobertura hídrica superficial. Valor normalizado entre 0 y 1, donde valores cercanos a 1 indican estrés severo.
- **Índice de Riesgo Territorial (IRT):** combinación del IEH con la capa de actividad minera georreferenciada y la capa de vulnerabilidad social (proximidad de comunidades a fuentes de agua bajo estrés).
- **Predicción a 7 días:** modelo LightGBM entrenado sobre series históricas de SMAP para anticipar la evolución del IEH en el corto plazo.

**Capa 3 — Interfaz de decisión**

Dashboard interactivo en Streamlit con cinco módulos:

| Módulo | Contenido |
|---|---|
| Mapa de riesgo | Visualización geoespacial del IEH e IRT sobre la cuenca, con zonas de alerta verde/amarillo/rojo |
| Serie temporal | Evolución histórica del índice con marcadores de eventos de estrés identificados |
| Simulador económico | Cálculo del valor económico en riesgo según cultivos, superficie irrigada y precio de mercado |
| Vulnerabilidad social | Mapa de comunidades en zona de influencia con datos demográficos INDEC |
| Metodología | Descripción de fuentes de datos, pipeline de procesamiento y limitaciones del sistema |

### 2.3 Usuarios y casos de uso

| Usuario | Cómo usa AquaGuard NOA |
|---|---|
| Secretaría de Ambiente de Salta | Monitoreo continuo de cuencas bajo presión minera; base objetiva para evaluaciones de impacto ambiental |
| Municipio de San Antonio de los Cobres | Alertas tempranas de estrés hídrico para gestión local del agua |
| Comunidades kollas y atacameñas | Acceso a datos objetivos sobre el estado del agua en su territorio |
| Cooperativas agrícolas del Valle de Lerma | Anticipación de períodos de baja disponibilidad hídrica para decisiones de siembra y riego |
| Empresas mineras (compliance ambiental) | Evidencia continua y objetiva del estado hídrico de la cuenca para reportes ESG y EIA |
| CONICET / UNSa (investigación) | Dataset continuo de variables hídricas para estudios de cambio climático y gestión de cuencas |
| Empresas mineras (Lithium Americas, Ganfeng — Cauchari-Olaroz) | Cumplimiento ESG y EIA con evidencia satelital continua |

### 2.4 Propuesta de valor diferencial

AquaGuard NOA no compite con sistemas existentes porque en Argentina no existe ningún sistema equivalente para cuencas mineras de altura. Su diferencial es:

- **Integración de fuentes:** combina radar SAR argentino (SAOCOM) con datos globales (SMAP, Sentinel-2, ERA5) en un pipeline unificado orientado a una problemática territorial específica.
- **Orientación a decisión:** no entrega imágenes, entrega índices accionables con umbrales de alerta calibrados.
- **Anclaje económico:** cuantifica el impacto de los eventos hídricos en términos de pérdida productiva aguas abajo, haciendo visible una externalidad que hoy es invisible.
- **Soberanía tecnológica:** el núcleo del sistema está basado en capacidad espacial argentina (SAOCOM/CONAE) procesada con herramientas de código abierto, sin dependencia de plataformas privadas extranjeras.

---

## 3. Datos utilizados y justificación

### 3.1 Fuentes de datos primarias

#### SAOCOM (CONAE — Argentina)
- **Producto:** Humedad de suelo superficial y en profundidad (hasta 50 cm) derivada de radar SAR banda L
- **Resolución espacial:** ~10-100 m según producto
- **Cobertura temporal:** desde 2018, con revisitas frecuentes sobre Argentina
- **Justificación:** Es el sensor con mayor penetración en el suelo disponible sobre la región. La banda L permite estimar humedad incluso bajo vegetación escasa, condición característica de la Puna. Además, su origen argentino es estratégico para la narrativa de soberanía de datos.
- **Portal de acceso:** https://saocom.invap.com.ar

#### NASA SMAP (Soil Moisture Active Passive)
- **Producto:** SPL3SMP — SMAP L3 Radiometer Global Daily 36 km
- **Resolución espacial:** 36 km (escala regional)
- **Cobertura temporal:** desde abril 2015, cobertura global diaria
- **Justificación:** Permite construir una serie histórica larga y consistente de humedad de suelo a escala regional. Es el dato base para calcular anomalías estacionales y entrenar el modelo predictivo. Su resolución más gruesa se complementa con SAOCOM para el detalle local.
En la implementación actual, SAOCOM opera como fuente de diseño arquitectural. Los datos operativos provienen de SMAP como proxy de alta disponibilidad.
- **Portal de acceso:** https://nsidc.org/data/spl3smp | Descarga programática: librería `earthaccess`

#### Sentinel-2 (ESA — Copernicus)
- **Bandas utilizadas:** B03 (verde), B08 (NIR), B11 (SWIR)
- **Resolución espacial:** 10-20 m
- **Cobertura temporal:** cada 5 días con dos satélites combinados
- **Justificación:** Permite calcular NDWI (Normalized Difference Water Index) para detectar y monitorear cuerpos de agua superficiales en la cuenca. Complementa los datos de humedad de suelo con información sobre agua superficial visible.
- **Portal de acceso:** https://browser.dataspace.copernicus.eu

#### ERA5 (ECMWF — Copernicus Climate Data Store)
- **Variables:** precipitación total, temperatura a 2m, evapotranspiración potencial
- **Resolución espacial:** ~31 km
- **Cobertura temporal:** desde 1940, actualización mensual con rezago de 5 días
- **Justificación:** Proporciona el contexto climático para contextualizar las anomalías de humedad detectadas por SMAP y SAOCOM. Permite distinguir estrés hídrico por déficit de precipitación de estrés hídrico por extracción o alteración antrópica.
- **Portal de acceso:** https://cds.climate.copernicus.eu | Descarga programática: librería `cdsapi`

### 3.2 Fuentes de datos secundarias

| Fuente | Datos | Uso en el sistema |
|---|---|---|
| INDEC — Censo 2022 | Población, comunidades, NBI por departamento | Capa de vulnerabilidad social |
| INDEC — Producción agropecuaria | Superficie cultivada, rendimientos, precios por cultivo en Salta | Modelo de impacto económico |
| INTA | Coeficientes de reducción de rendimiento por estrés hídrico por cultivo | Cálculo de pérdida productiva |
| IGN Argentina | Shapefile de cuencas hidrográficas, ríos, límites administrativos | Recorte espacial del área de estudio |
| Secretaría de Minería de Salta | Concesiones mineras georreferenciadas | Capa de actividad minera |
| SAGyP | Estimaciones agrícolas del Valle de Lerma | Validación del modelo económico |

### 3.3 Justificación de la combinación de fuentes

La decisión de combinar estas fuentes responde a una lógica de complementariedad:

- **SMAP** aporta consistencia histórica y cobertura diaria, pero a resolución gruesa.
- **SAOCOM** aporta resolución local y capacidad de penetración bajo nubes, pero con menor frecuencia de revisita.
- **Sentinel-2** aporta detalle visual de agua superficial, pero no funciona bajo nubes.
- **ERA5** aporta contexto climático para separar señal antrópica de señal climática natural.

Ninguna de estas fuentes sola responde la pregunta central del sistema. La fusión de las cuatro sí lo hace.

---

## 4. Arquitectura del sistema

> El sistema se organiza en tres capas funcionales:

**Capa 1 — Observación continua**
Descarga automática de datos SMAP (SPL3SMP v009) mediante la 
librería earthaccess de NASA. Los archivos HDF5 se recortan 
al bounding box de la cuenca (-67.5, -24.5, -66.0, -23.5) 
y se procesan con h5py. SAOCOM y Sentinel-2 están integrados 
en la arquitectura como fuentes de Fase 2.

**Capa 2 — Modelado**
Cálculo del Índice de Estrés Hídrico (IEH) como anomalía 
Z-score de humedad de suelo respecto al baseline histórico 
estacional, normalizada entre 0 (normal) y 1 (crítico). 
Clasificación en tres niveles: NORMAL (<0.4), MODERADO 
(0.4-0.7), CRÍTICO (>0.7). Predicción a 7 días con 
LightGBM prevista en Fase 2.

**Capa 3 — Interfaz de decisión**
Dashboard Streamlit con cuatro módulos: serie temporal del 
IEH, mapa de cuenca, simulador de impacto económico, y 
metodología. Deployable en Streamlit Community Cloud.

El diagrama de arquitectura completo está disponible en 
el archivo FigJam del proyecto.

---

## 5. Desarrollo técnico — Log de avance

| Hora | Acción | Estado |
|---|---|---|
| 22/05 22:00 | Definición del problema y área de estudio | ✅ |
| 22/05 23:00 | Setup entorno conda, resolución conflictos DLL Windows | ✅ |
| 22/05 23:30 | Configuración credenciales NASA Earthdata | ✅ |
| 23/05 20:00 | Pipeline descarga SMAP (01_descarga_smap.py) | ✅ |
| 23/05 21:00 | Extracción humedad por cuenca (02_procesar_smap.py) | ✅ |
| 23/05 21:30 | Cálculo IEH y clasificación (03_calcular_ieh.py) | ✅ |
| 24/05 09:30 | Dashboard Streamlit 4 tabs (dashboard/app.py) | ✅ |
| 24/05 11:00 | Diagrama de arquitectura en FigJam | ✅ |
| 24/05 12:00 | Video de presentación 90 segundos |   |

### Log
| Hora | Acción | Estado |
|---|---|---|
| | | |

---

## 6. Modelo de impacto económico

### Cadena de impacto
Estrés hídrico en cuenca alta → reducción de caudal 
disponible → déficit de riego en Valle de Lerma → 
reducción de rendimiento agrícola → pérdida económica 
cuantificable.

### Parámetros del modelo
- Superficie irrigada en riesgo: 15.000 hectáreas (Valle de Lerma, fuente SAGyP)
- Cultivo de referencia: tabaco (principal cultivo comercial salteño)
- Rendimiento promedio: 2,5 ton/ha (fuente INTA)
- Precio de mercado: USD 850/ton (fuente INDEC)
- Reducción de rendimiento por estrés hídrico severo: 25% (fuente INTA)

### Cálculo
Pérdida potencial por evento:
15.000 ha × 2,5 ton/ha × 25% × USD 850/ton = **USD 7.968.750**

Pérdida evitable con alerta temprana (40%):
**USD 3.187.500 por evento**

### Costo estimado del sistema vs. beneficio
Costo operativo anual estimado del sistema: USD 50.000
ROI: 63x en un solo evento severo evitado.

### Fuentes
INDEC Producción Agropecuaria | INTA NOA | SAGyP 
estimaciones Valle de Lerma 2024.

---

## 7. Resultados y visualizaciones

### Datos procesados
- Período: abril 2024 — abril 2025
- Registros válidos obtenidos: 12 observaciones
- Cobertura: ~40% de días con datos válidos 
  (normal para resolución 36km en cuenca pequeña)

### Valores del IEH calculados
- IEH mínimo registrado: 0.00 (15/04/2024 — evento 
  de humedad elevada, probable precipitación o nevada)
- IEH máximo registrado: 1.00 (25/04/2024 — suelo 
  en condición más seca del período)
- IEH última medición (02/04/2025): 0.69 — MODERADO

### Interpretación
El período analizado muestra condición de estrés hídrico 
crónico en la cuenca (IEH promedio >0.8), con un único 
evento de humedad elevada en abril 2024 que contrasta 
con la tendencia general de aridez. Esto es consistente 
con las características climáticas de la Puna salteña 
en otoño.

### Dashboard
Disponible en: dashboard/app.py
Ejecutar con: streamlit run dashboard/app.py

---

## 8. Limitaciones y trabajo futuro

### Expansión prevista: Fase 2 — Salar de Cauchari-Olaroz

AquaGuard NOA está diseñado desde su arquitectura para escalar a otras cuencas del NOA. La expansión prioritaria identificada es el **Salar de Cauchari-Olaroz**, ubicado en el departamento de Los Andes, Salta, donde operan actualmente proyectos de extracción de litio de escala internacional (Lithium Americas y Ganfeng Lithium).

La hidrología de los salares de altura presenta mayor complejidad que la cuenca del río San Antonio de los Cobres, ya que involucra acuíferos subterráneos de salmuera cuya dinámica no es completamente capturada por SMAP en su configuración estándar. Esta complejidad técnica adicional justifica que Cauchari-Olaroz sea una segunda fase y no el caso de estudio inicial.

Sin embargo, el impacto potencial de esta expansión es significativamente mayor, dado el volumen de inversión extranjera directa en la zona y las obligaciones de monitoreo ambiental que los operadores deben cumplir para acceder a mercados internacionales de financiamiento ESG.

---

## 9. Referencias

### Referencias preliminares

- CONAE (2023). *Misión SAOCOM: productos y aplicaciones*. https://saocom.invap.com.ar
- Entekhabi, D. et al. (2010). The Soil Moisture Active Passive (SMAP) Mission. *Proceedings of the IEEE*, 98(5), 704-716.
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. *FAccT 2019*.
- INDEC (2022). *Censo Nacional de Población, Hogares y Viviendas 2022*. https://www.indec.gob.ar
- INTA (2020). *Impacto del estrés hídrico en cultivos del NOA argentino*.
- Secretaría de Minería de Salta (2024). *Mapa de concesiones mineras provincia de Salta*.

---

## 10. Cómo ejecutar el proyecto

### Requisitos
- Miniconda instalado
- Cuenta en NASA Earthdata: https://urs.earthdata.nasa.gov

### Instalación
```bash
conda create -n aquaguard python=3.11 -c conda-forge -y
conda activate aquaguard
conda install -c conda-forge lightgbm xarray h5py h5netcdf netCDF4 geopandas earthaccess streamlit plotly pandas numpy scikit-learn shap psutil pyproj folium -y
```

### Credenciales NASA
```bash
python -c "import earthaccess; earthaccess.login(strategy='interactive', persist=True)"
```

### Pipeline completo
```bash
python src/01_descarga_smap.py
python src/02_procesar_smap.py
python src/03_calcular_ieh.py
```

### Dashboard
```bash
streamlit run dashboard/app.py
```
---

*Documento creado el 23 de mayo de 2026*
 
*Próxima actualización: Junio*
