import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AquaGuard NOA",
    page_icon="💧",
    layout="wide"
)

# Cargar datos
df = pd.read_csv("data/processed/smap_ieh.csv", parse_dates=["fecha"])

# Header
st.title("💧 AquaGuard NOA")
st.markdown("**Sistema satelital de predicción de estrés hídrico — Cuenca San Antonio de los Cobres, Salta**")
st.divider()

# Métricas principales
ultimo = df.iloc[-1]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Última medición", ultimo["fecha"].strftime("%d/%m/%Y"))
col2.metric("Humedad de suelo", f"{ultimo['sm_media']:.4f} m³/m³")
col3.metric("IEH actual", f"{ultimo['ieh']:.2f}")
col4.metric("Estado", ultimo["alerta"])

st.divider()

# Tabs reorganizados por jerarquía analítica
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Mapa de Cuenca",
    "📈 Serie Temporal",
    "👥 Impacto Socioeconómico",
    "ℹ️ Metodología"
])

# --- Tab 1: Serie temporal ---
with tab1:
    st.subheader("Evolución del Índice de Estrés Hídrico (IEH)")

    fig = go.Figure()

    # Línea IEH
    fig.add_trace(go.Scatter(
        x=df["fecha"], y=df["ieh"],
        mode="lines+markers",
        name="IEH",
        line=dict(color="#e74c3c", width=2),
        marker=dict(size=8)
    ))

    # Umbrales
    fig.add_hline(y=0.7, line_dash="dash", line_color="red",
                  annotation_text="Umbral crítico (0.7)")
    fig.add_hline(y=0.4, line_dash="dash", line_color="orange",
                  annotation_text="Umbral moderado (0.4)")

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="IEH (0=normal, 1=crítico)",
        yaxis=dict(range=[0, 1.1]),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tabla de datos")
    st.dataframe(
        df[["fecha", "sm_media", "ieh", "alerta"]].rename(columns={
            "fecha": "Fecha",
            "sm_media": "Humedad suelo (m³/m³)",
            "ieh": "IEH",
            "alerta": "Estado"
        }),
        use_container_width=True
    )

# --- Tab 2: Mapa ---
with tab2:
    st.subheader("Cuenca Alta del Río San Antonio de los Cobres")

    # Mapa centrado en la cuenca
    mapa_df = pd.DataFrame({
        "lat": [-24.0],
        "lon": [-66.8],
        "nombre": ["San Antonio de los Cobres"],
        "ieh": [ultimo["ieh"]],
        "estado": [ultimo["alerta"]]
    })

    fig_mapa = px.scatter_mapbox(
        mapa_df,
        lat="lat", lon="lon",
        hover_name="nombre",
        hover_data={"ieh": True, "estado": True, "lat": False, "lon": False},
        color="ieh",
        color_continuous_scale=["green", "yellow", "red"],
        range_color=[0, 1],
        size=[20],
        zoom=7,
        height=500,
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig_mapa, use_container_width=True)

    st.info("""
    **Área de estudio:** Cuenca alta del río San Antonio de los Cobres  
    **Departamento:** Los Andes, Salta  
    **Altitud media:** ~3.800 msnm  
    **Actividad minera:** Explotación de boratos (Tincalayu) y sal  
    **Conexión hídrica:** Tributaria del sistema Pasaje-Juramento → Valle de Lerma
    """)

# --- Tab 3: Impacto económico ---
with tab3:
    st.subheader("Simulador de Impacto Económico")
    st.markdown("Estimación de pérdidas productivas en el Valle de Lerma ante eventos de estrés hídrico en la cuenca alta.")

    col1, col2 = st.columns(2)
    with col1:
        hectareas = st.slider(
            "Hectáreas irrigadas en riesgo", 1000, 50000, 15000, 1000)
        reduccion = st.slider(
            "Reducción de rendimiento por estrés hídrico (%)", 10, 50, 25, 5)
    with col2:
        cultivo = st.selectbox(
            "Cultivo principal",
            ["Tabaco", "Hortalizas", "Caña de azúcar", "Soja"]
        )
        precios = {
            "Tabaco": 850,
            "Hortalizas": 320,
            "Caña de azúcar": 180,
            "Soja": 290
        }
        rendimientos = {
            "Tabaco": 2.5,
            "Hortalizas": 15.0,
            "Caña de azúcar": 60.0,
            "Soja": 3.2
        }
        precio = precios[cultivo]
        rendimiento = rendimientos[cultivo]

    perdida = hectareas * rendimiento * (reduccion / 100) * precio
    ahorro_sistema = perdida * 0.40  # 40% evitable con alerta temprana

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Pérdida potencial por evento", f"USD {perdida:,.0f}")
    c2.metric("Pérdida evitable con alerta temprana (40%)", f"USD {ahorro_sistema:,.0f}")
    c3.metric("ROI del sistema de monitoreo", f"{int(ahorro_sistema/50000)}x")

    st.caption("""
    **Fuentes:** INDEC Producción Agropecuaria | INTA coeficientes de estrés hídrico por cultivo | SAGyP estimaciones Valle de Lerma  
    **Supuesto:** El 40% de pérdidas es evitable con 7 días de anticipación para decisiones de riego y cosecha.
    """)

# --- Tab 4: Metodología ---
with tab4:
    st.subheader("Metodología y fuentes de datos")

    st.markdown("""
    ### Fuentes de datos
    | Fuente | Producto | Uso |
    |---|---|---|
    | NASA SMAP | SPL3SMP v009 | Humedad de suelo diaria |
    | SAOCOM (CONAE) | SMC banda L | Validación local (Fase 2) |
    | Sentinel-2 (ESA) | B03/B08/B11 | NDWI cobertura hídrica (Fase 2) |
    | ERA5 (ECMWF) | Precipitación/Temp | Contexto climático (Fase 2) |

    ### Cálculo del IEH
    El **Índice de Estrés Hídrico (IEH)** se calcula como una anomalía estandarizada
    de humedad de suelo respecto al baseline histórico del mismo período estacional,
    normalizada entre 0 (condición normal) y 1 (estrés crítico).

    ### Limitaciones actuales
    - Resolución SMAP: 36 km (escala regional, no local)
    - Baseline histórico limitado a datos disponibles (sistema diseñado para series más largas)
    - Integración Sentinel-2 y ERA5 en desarrollo (Fase 2)

    ### Expansión prevista: Fase 2
    Salar de Cauchari-Olaroz (proyecto litio Allkem/Posco) — mayor complejidad
    hidrológica subterránea, impacto económico potencialmente más alto.
    """)

    st.info("**Proyecto desarrollado en el marco del Desafío Argentina al Espacio 2026 — ConstelAR Space**")