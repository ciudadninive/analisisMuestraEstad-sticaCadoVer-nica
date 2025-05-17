import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Lee los datos desde el archivo Excel
archivo = "MuestrasAplicandoFiltrado.xlsx"
hoja = "BD_ESTUDIO"

df = pd.read_excel(archivo, sheet_name=hoja)
df.columns = [c.strip() for c in df.columns]

df = df.rename(columns={
    'Sexo': 'Sexo',
    'Condicion_Experimental': 'Condición Experimental',
    'NivelLectura-Pretest': 'Nivel Lectura Pretest',
    'Puntaje_Pretest': 'Puntaje Pretest',
    'Puntaje_Postest': 'Puntaje Postest'
})

for col in ['Puntaje Pretest', 'Puntaje Postest']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['Puntaje Pretest', 'Puntaje Postest', 'Sexo', 'Nivel Lectura Pretest', 'Condición Experimental'])

colores = ["#4C72B0", "#C44E52"]
momentos = ['Puntaje Pretest', 'Puntaje Postest']

# Etiquetas de mediana dentro de cada caja
def add_median_labels(ax, data, x, hue, y):
    medians = data.groupby([x, hue])[y].median().reset_index()
    n_hue = len(data[hue].unique())
    for i, artist in enumerate(ax.artists):
        box = artist
        box_x = box.get_x() + box.get_width() / 2
        cats = [t.get_text() for t in ax.get_xticklabels()]
        cat = cats[i // n_hue]
        moment = data[hue].unique()[i % n_hue]
        median_val = medians[(medians[x] == cat) & (medians[hue] == moment)][y].values
        if len(median_val) > 0:
            ax.text(box_x, median_val[0], f"{median_val[0]:.1f}", ha='center', va='center',
                    fontsize=9, color='white' if box.get_facecolor()[0] < 0.5 else 'black',
                    fontweight='bold', bbox=dict(facecolor=box.get_facecolor(), edgecolor='none', alpha=0.7, boxstyle='round,pad=0.15'))

# Etiquetas resumen en la parte central inferior, cada una en un renglón diferente, sin sobreposición
def add_bottom_center_labels(ax, data, hue, colores, medida="Mediana", y_offset=0.07, line_sep=0.055):
    momentos = ['Puntaje Pretest', 'Puntaje Postest']
    resumen = []
    for idx, color in zip(momentos, colores):
        vals = data[data[hue]==idx]['Puntaje']
        if len(vals) > 0 and not np.all(np.isnan(vals)):
            valor = np.nanmedian(vals)
            resumen.append((idx, valor, color))
        else:
            resumen.append((idx, None, color))
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x = (xlim[0] + xlim[1]) / 2

    # Calcula espacio vertical para la gráfica 3 (más alto para más espacio)
    if hasattr(ax, 'is_grande') and ax.is_grande:
        y_offset = 0.12
        line_sep = 0.07

    y = ylim[0] + (ylim[1]-ylim[0]) * y_offset

    # Línea 1: Mediana
    ax.text(x, y, f"{medida}", ha='center', va='bottom', fontsize=12, fontweight='bold',
            color='black', bbox=dict(facecolor='white', edgecolor='gray', alpha=0.85, boxstyle='round,pad=0.2'))

    # Línea 2: (renglón libre)
    y_line = y + ((ylim[1]-ylim[0])*line_sep)

    # Línea 3: Puntaje Pretest
    if resumen[0][1] is not None:
        label = f"{resumen[0][0]}: {resumen[0][1]:.1f}"
    else:
        label = f"{resumen[0][0]}: N/A"
    ax.text(x, y_line, label, ha='center', va='bottom', fontsize=12, fontweight='bold', color=colores[0],
            bbox=dict(facecolor='none', edgecolor='none', alpha=0))

    # Línea 4: Puntaje Postest
    y_line2 = y_line + ((ylim[1]-ylim[0])*line_sep)
    if resumen[1][1] is not None:
        label = f"{resumen[1][0]}: {resumen[1][1]:.1f}"
    else:
        label = f"{resumen[1][0]}: N/A"
    ax.text(x, y_line2, label, ha='center', va='bottom', fontsize=12, fontweight='bold', color=colores[1],
            bbox=dict(facecolor='none', edgecolor='none', alpha=0))

fig = plt.figure(figsize=(13, 7))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.7])

# 1. Boxplot por Sexo (arriba izquierda)
ax1 = fig.add_subplot(gs[0, 0])
data1 = pd.melt(df, id_vars=['Sexo'], value_vars=momentos, var_name='Momento', value_name='Puntaje')
sns.boxplot(data=data1, x='Sexo', y='Puntaje', hue='Momento', palette=colores, ax=ax1, width=0.6, fliersize=2)
add_median_labels(ax1, data1, 'Sexo', 'Momento', 'Puntaje')
add_bottom_center_labels(ax1, data1, 'Momento', colores, medida="Mediana", y_offset=0.07, line_sep=0.055)
ax1.set_title('Puntaje Pretest y Postest por Sexo', fontsize=11)
ax1.set_xlabel('Sexo')
ax1.set_ylabel('Puntaje')
ax1.legend_.remove()

# 2. Boxplot por Nivel de Lectura Pretest (arriba derecha)
ax2 = fig.add_subplot(gs[0, 1])
data2 = pd.melt(df, id_vars=['Nivel Lectura Pretest'], value_vars=momentos, var_name='Momento', value_name='Puntaje')
sns.boxplot(data=data2, x='Nivel Lectura Pretest', y='Puntaje', hue='Momento', palette=colores, ax=ax2, width=0.6, fliersize=2)
add_median_labels(ax2, data2, 'Nivel Lectura Pretest', 'Momento', 'Puntaje')
add_bottom_center_labels(ax2, data2, 'Momento', colores, medida="Mediana", y_offset=0.07, line_sep=0.055)
ax2.set_title('Puntaje Pretest y Postest por Nivel de Lectura (Pretest)', fontsize=11)
ax2.set_xlabel('Nivel de Lectura (Pretest)')
ax2.set_ylabel('Puntaje')
ax2.legend_.remove()

# 3. Boxplot por Condición Experimental (abajo, centrado, más alto)
ax3 = fig.add_subplot(gs[1, :])
ax3.is_grande = True  # Marca este eje como el más grande para usar más espacio vertical
data3 = pd.melt(df, id_vars=['Condición Experimental'], value_vars=momentos, var_name='Momento', value_name='Puntaje')
all_cats = sorted(df['Condición Experimental'].unique())
all_moments = momentos
for cat in all_cats:
    for moment in all_moments:
        if not ((data3['Condición Experimental'] == cat) & (data3['Momento'] == moment)).any():
            data3 = pd.concat([data3, pd.DataFrame({'Condición Experimental':[cat], 'Momento':[moment], 'Puntaje':[np.nan]})], ignore_index=True)
sns.boxplot(data=data3, x='Condición Experimental', y='Puntaje', hue='Momento', palette=colores, ax=ax3, width=0.6, fliersize=2)
add_median_labels(ax3, data3, 'Condición Experimental', 'Momento', 'Puntaje')
add_bottom_center_labels(ax3, data3, 'Momento', colores, medida="Mediana", y_offset=0.12, line_sep=0.07)
ax3.set_title('Puntaje Pretest y Postest por Condición Experimental', fontsize=11)
ax3.set_xlabel('Condición Experimental')
ax3.set_ylabel('Puntaje')
ax3.legend_.remove()

plt.suptitle('Diagramas de Caja: Comparación de Puntajes Pretest y Postest', fontsize=15, y=1.02, fontweight='bold')
plt.tight_layout(rect=[0, 0.08, 1, 0.98])
plt.savefig("Boxplots_Puntajes_Distribuidos.svg", format='svg', bbox_inches='tight')
plt.close()
print("¡SVG generado exitosamente como 'Boxplots_Puntajes_Distribuidos.svg'!")
