import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/smap_cuenca.csv", parse_dates=["fecha"])

# Baseline histórico: promedio y std de abril 2024
baseline = df[df["fecha"].dt.year == 2024]["sm_media"]
baseline_mean = baseline.mean()
baseline_std  = baseline.std()

print(f"Baseline abril 2024 → media: {baseline_mean:.4f} | std: {baseline_std:.4f}")

# Anomalía estandarizada (Z-score)
df["anomalia"] = (df["sm_media"] - baseline_mean) / baseline_std

# IEH: normalizado entre 0 y 1
# Z negativo = suelo más seco que el promedio = mayor estrés
# Invertimos para que IEH alto = mayor estrés
df["ieh"] = 1 - (df["anomalia"] - df["anomalia"].min()) / \
                (df["anomalia"].max() - df["anomalia"].min())

# Clasificación de alerta
def clasificar(ieh):
    if ieh >= 0.7:   return "🔴 CRÍTICO"
    elif ieh >= 0.4: return "🟡 MODERADO"
    else:            return "🟢 NORMAL"

df["alerta"] = df["ieh"].apply(clasificar)

df.to_csv("data/processed/smap_ieh.csv", index=False)
print("\nÍndice de Estrés Hídrico calculado:")
print(df[["fecha", "sm_media", "anomalia", "ieh", "alerta"]].to_string())