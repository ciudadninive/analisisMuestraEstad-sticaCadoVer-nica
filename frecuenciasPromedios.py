import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lee los datos desde el archivo Excel
archivo = "MuestrasAplicandoFiltrado.xlsx"
hoja = "BD_ESTUDIO"

# Carga los datos
df = pd.read_excel(archivo, sheet_name=hoja)
df.columns = [c.strip() for c in df.columns]

# Detecta los nombres correctos de las columnas numéricas
col_prom = [c for c in df.columns if 'promedio' in c.lower()][0]
col_pre = [c for c in df.columns if 'pretest' in c.lower()][0]
col_post = [c for c in df.columns if 'postest' in c.lower()][0]

# Selecciona y convierte a numérico, forzando errores a NaN
df_num = df[[col_prom, col_pre, col_post]].copy()
df_num.columns = ['Promedio', 'Puntaje Pretest', 'Puntaje Postest']
for col in df_num.columns:
    df_num[col] = pd.to_numeric(df_num[col], errors='coerce')
df_num = df_num.dropna()

# Paleta de colores diferentes
colores = ["#4C72B0", "#55A868", "#C44E52"]
titulos = [
    "Histograma de Promedio General",
    "Histograma de Puntaje Pretest",
    "Histograma de Puntaje Postest"
]
ejes_x = [
    "Promedio",
    "Puntaje Pretest",
    "Puntaje Postest"
]

# Configura la figura: 2 filas, 2 columnas (la última gráfica centrada)
fig, axes = plt.subplots(2, 2, figsize=(13, 8), gridspec_kw={'height_ratios': [1, 1]})
axes = axes.flatten()

# Primer renglón: dos gráficas
for i in range(2):
    ax = axes[i]
    data = df_num.iloc[:, i]
    counts, bins, patches = ax.hist(data, bins='auto', color=colores[i], edgecolor='black', alpha=0.85)
    ax.set_title(titulos[i], fontsize=13)
    ax.set_xlabel(ejes_x[i], fontsize=11)
    ax.set_ylabel('Frecuencia', fontsize=11)
    ax.grid(axis='y', linestyle=':', alpha=0.5)
    # Etiquetas explícitas sobre cada barra
    for count, left, right in zip(counts, bins[:-1], bins[1:]):
        if count > 0:
            label = f"{left:.1f}–{right:.1f}\n{int(count)}"
            y_pos = count * 0.5 if count > 1 else count + 0.5
            ax.annotate(label,
                        (left + (right - left)/2, y_pos),
                        ha='center', va='center', fontsize=9, fontweight='bold', rotation=0)
    # Media y mediana
    media = data.mean()
    mediana = data.median()
    ax.axvline(media, color='red', linestyle='--', linewidth=1, label=f'Media: {media:.2f}')
    ax.axvline(mediana, color='green', linestyle=':', linewidth=1, label=f'Mediana: {mediana:.2f}')
    ax.legend(fontsize=9)

# Segundo renglón: la tercera gráfica centrada
ax = axes[2]
data = df_num.iloc[:, 2]
counts, bins, patches = ax.hist(data, bins='auto', color=colores[2], edgecolor='black', alpha=0.85)
ax.set_title(titulos[2], fontsize=13)
ax.set_xlabel(ejes_x[2], fontsize=11)
ax.set_ylabel('Frecuencia', fontsize=11)
ax.grid(axis='y', linestyle=':', alpha=0.5)
for count, left, right in zip(counts, bins[:-1], bins[1:]):
    if count > 0:
        label = f"{left:.1f}–{right:.1f}\n{int(count)}"
        y_pos = count * 0.5 if count > 1 else count + 0.5
        ax.annotate(label,
                    (left + (right - left)/2, y_pos),
                    ha='center', va='center', fontsize=9, fontweight='bold', rotation=0)
media = data.mean()
mediana = data.median()
ax.axvline(media, color='red', linestyle='--', linewidth=1, label=f'Media: {media:.2f}')
ax.axvline(mediana, color='green', linestyle=':', linewidth=1, label=f'Mediana: {mediana:.2f}')
ax.legend(fontsize=9)

# Elimina el último eje (inferior derecha) y centra la gráfica inferior
fig.delaxes(axes[3])
plt.subplots_adjust(hspace=0.35)
plt.suptitle('Histogramas de Variables Numéricas - Caso de Estudio Verónica', fontsize=16, y=0.98, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Guarda como SVG
plt.savefig("Histogramas_Variables_Numericas.svg", format='svg', bbox_inches='tight')
plt.close()
print("¡SVG generado exitosamente como 'Histogramas_Variables_Numericas.svg'!")
