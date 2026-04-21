import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint

# --- Parámetros del modelo ---
T0    = 90.0   # Temperatura inicial del café (°C)
Ta    = 22.0   # Temperatura ambiente (°C)
k     = 0.07   # Constante de enfriamiento (1/min) — café en taza cerámica
t_fin = 60     # Tiempo total de simulación (minutos)

# Vector de tiempo (600 puntos de 0 a t_fin minutos)
t = np.linspace(0, t_fin, 600)

# --- Definición de la EDO ---
def modelo_enfriamiento(T, t, k, Ta):

    dTdt = -k * (T - Ta)
    return dTdt

# --- Solución numérica ---
T_sol = odeint(modelo_enfriamiento, T0, t, args=(k, Ta))
T_sol = T_sol.flatten()  # Convertir de columna a arreglo 1D

# --- Solución analítica ---
T_analitica = Ta + (T0 - Ta) * np.exp(-k * t)

# --- Gráfica: Temperatura vs Tiempo ---
plt.figure(figsize=(10, 5))

plt.plot(t, T_sol,       color='steelblue',  linewidth=2,
         label='Solución numérica (odeint)')
plt.plot(t, T_analitica, color='tomato',      linewidth=1.5,
         linestyle='--', label='Solución analítica')

# Línea de temperatura ambiente
plt.axhline(y=Ta, color='gray', linestyle=':', linewidth=1.2,
            label=f'Temperatura ambiente ({Ta}°C)')

# Anotación: temperatura ideal para beber café
plt.axhline(y=60, color='orange', linestyle='-.', linewidth=1,
            label='Temperatura ideal café (60°C)')

plt.title('Enfriamiento de Newton — Taza de Café', fontsize=14)
plt.xlabel('Tiempo (minutos)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('temperatura_vs_tiempo.png', dpi=150)
plt.show()
plt.close()

print("Gráfica guardada: temperatura_vs_tiempo.png")

# --- Animación GIF del enfriamiento ---
fig_anim, ax_anim = plt.subplots(figsize=(8, 5))

ax_anim.set_xlim(0, t_fin)
ax_anim.set_ylim(Ta - 5, T0 + 5)
ax_anim.set_title('Simulación de Enfriamiento — Café', fontsize=13)
ax_anim.set_xlabel('Tiempo (minutos)')
ax_anim.set_ylabel('Temperatura (°C)')
ax_anim.axhline(y=Ta, color='gray', linestyle=':', linewidth=1,
                label=f'T ambiente = {Ta}°C')
ax_anim.legend(loc='upper right')
ax_anim.grid(True, alpha=0.3)

# Elementos que se actualizarán en cada frame
linea_anim, = ax_anim.plot([], [], color='steelblue', linewidth=2)
punto_anim, = ax_anim.plot([], [], 'o', markersize=10)
texto_temp  = ax_anim.text(0.65, 0.85, '', transform=ax_anim.transAxes,
                            fontsize=12, color='black')

# Número de frames (usa 1 de cada 6 puntos para que no sea muy lento)
frames_idx = range(0, len(t), 6)
frames_list = list(frames_idx)

def init_anim():
    """Reinicia la animación al estado vacío."""
    linea_anim.set_data([], [])
    punto_anim.set_data([], [])
    texto_temp.set_text('')
    return linea_anim, punto_anim, texto_temp

def actualizar_frame(i):
    # Dibujar la curva hasta el punto i
    linea_anim.set_data(t[:i], T_sol[:i])

    # Punto móvil en el frente de la curva
    punto_anim.set_data([t[i]], [T_sol[i]])

    # Color del punto: gradiente rojo → azul según temperatura
    ratio = (T_sol[i] - Ta) / (T0 - Ta)   # 1.0 = caliente, 0.0 = frío
    color_punto = (ratio, 0.1, 1 - ratio)  # (R, G, B)
    punto_anim.set_color(color_punto)

    # Texto con temperatura actual
    texto_temp.set_text(f'T = {T_sol[i]:.1f} °C\nt = {t[i]:.1f} min')

    return linea_anim, punto_anim, texto_temp

anim = animation.FuncAnimation(
    fig_anim,
    actualizar_frame,
    frames=frames_list,
    init_func=init_anim,
    interval=60,      # milisegundos entre frames
    blit=True
)

# Exportar como GIF (requiere Pillow instalado: pip install Pillow)
anim.save('enfriamiento_cafe.gif', writer='pillow', fps=18)
plt.close()

print("Animación guardada: enfriamiento_cafe.gif")

# --- Modelo predictivo: Enfriamiento de café ---
print("\n===== MODELO PREDICTIVO: CAFÉ =====")

T_objetivo = 60.0  # °C — temperatura ideal para beber

# Buscar el tiempo donde T cruza T_objetivo
idx_objetivo = np.argmax(T_sol <= T_objetivo)

if idx_objetivo > 0:
    t_objetivo = t[idx_objetivo]
    print(f"El café alcanza {T_objetivo}°C en aproximadamente {t_objetivo:.1f} minutos.")
else:
    print("El café nunca alcanza la temperatura objetivo en el rango simulado.")

# --- Escenario A: Comparar distintas temperaturas ambiente ---
ambientes = [10, 22, 35]      # °C: día frío, normal, día caluroso
colores   = ['royalblue', 'forestgreen', 'tomato']
etiquetas = ['Ta = 10°C (día frío)', 'Ta = 22°C (normal)', 'Ta = 35°C (caluroso)']

plt.figure(figsize=(10, 5))

for Ta_i, color_i, etiqueta_i in zip(ambientes, colores, etiquetas):
    T_i = odeint(modelo_enfriamiento, T0, t, args=(k, Ta_i)).flatten()
    plt.plot(t, T_i, color=color_i, linewidth=2, label=etiqueta_i)

plt.axhline(y=60, color='orange', linestyle='--', linewidth=1,
            label='Temperatura ideal (60°C)')
plt.title('Escenario A: Impacto de la Temperatura Ambiente', fontsize=13)
plt.xlabel('Tiempo (minutos)')
plt.ylabel('Temperatura del café (°C)')
plt.legend()
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('escenario_temperatura_ambiente.png', dpi=150)
plt.close()

print("Gráfica guardada: escenario_temperatura_ambiente.png")

# --- Escenario B: Comparar distintas constantes de enfriamiento ---
constantes = [0.03, 0.07, 0.15]   # taza térmica, cerámica, vaso delgado
colores_k  = ['purple', 'steelblue', 'darkorange']
etiquetas_k = ['k=0.03 (taza térmica)', 'k=0.07 (taza cerámica)', 'k=0.15 (vaso delgado)']

plt.figure(figsize=(10, 5))

for k_i, color_i, etiqueta_i in zip(constantes, colores_k, etiquetas_k):
    T_i = odeint(modelo_enfriamiento, T0, t, args=(k_i, Ta)).flatten()
    plt.plot(t, T_i, color=color_i, linewidth=2, label=etiqueta_i)

plt.axhline(y=60, color='orange', linestyle='--', linewidth=1,
            label='Temperatura ideal (60°C)')
plt.title('Escenario B: Impacto de la Constante de Enfriamiento', fontsize=13)
plt.xlabel('Tiempo (minutos)')
plt.ylabel('Temperatura del café (°C)')
plt.legend()
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('escenario_constante_k.png', dpi=150)
plt.close()

print("Gráfica guardada: escenario_constante_k.png")
