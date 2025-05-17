import pandas as pd
import matplotlib.pyplot as plt

# Lee los datos desde el archivo Excel
archivo = "MuestrasAplicandoFiltrado.xlsx"
hoja = "BD_ESTUDIO"

# Carga los datos
df = pd.read_excel(archivo, sheet_name=hoja)

# Selecciona y limpia las columnas relevantes
columnas = [
    'Sexo',
    'Grado',
    'Grupo',
    'Condicion_Experimental',
    'Participacion',
    'NivelLectura-Pretest'
]
df = df[columnas]
df.columns = [
    'Sexo',
    'Grado',
    'Grupo',
    'Condición Experimental',
    'Participación',
    'Nivel de Lectura (Pretest)'
]

# Paleta de colores diferentes para cada gráfica
colores = ["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974", "#64B5CD"]

# Títulos para cada gráfica
titulos = [
    "Frecuencia por Sexo",
    "Frecuencia por Grado",
    "Frecuencia por Grupo",
    "Frecuencia por Condición Experimental",
    "Frecuencia por Participación",
    "Frecuencia por Nivel de Lectura (Pretest)"
]

# Configura la figura: 2 filas x 3 columnas (más compacta)
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 6))
axes = axes.flatten()

for i, col in enumerate(df.columns):
    ax = axes[i]
    vc = df[col].value_counts().sort_index()
    bars = ax.bar(vc.index.astype(str), vc.values, color=colores[i], edgecolor='black', width=0.6)
    ax.set_title(titulos[i], fontsize=11)
    ax.set_xlabel('')
    ax.set_ylabel('Frecuencia', fontsize=10)
    ax.tick_params(axis='x', labelrotation=20, labelsize=9)
    ax.tick_params(axis='y', labelsize=9)
    ax.grid(axis='y', linestyle=':', alpha=0.5)
    # Etiquetas explícitas sobre cada barra
    for bar, cat, freq in zip(bars, vc.index, vc.values):
        label = f"{cat}: {freq}"
        ax.annotate(label,
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha='center', va='bottom', fontsize=9, fontweight='bold', rotation=0, xytext=(0,2), textcoords='offset points')

# Título general, más arriba
plt.suptitle(
    'Frecuencias de la Muestra Caso de Estudio Verónica',
    fontsize=16,
    y=1.07,  # Más arriba de lo normal
    fontweight='bold'
)
plt.tight_layout(rect=[0, 0.03, 1, 0.98])

# Guarda como SVG
plt.savefig("Distribucion_Frecuencias_Muestra.svg", format='svg', bbox_inches='tight')
plt.close()
print("¡SVG generado exitosamente como 'Distribucion_Frecuencias_Muestra.svg'!")
