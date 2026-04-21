# 📋 Requerimientos de Programación en Python
## Proyecto: Modelado y Simulación del Enfriamiento de Newton
### Caso aplicado: Enfriamiento de una taza de café

---

## 🗂️ Estructura general del archivo

El proyecto se entrega en **un solo archivo** llamado:

```
enfriamiento_newton.py
```

El archivo se organiza en **5 secciones secuenciales**, separadas por bloques de comentarios bien visibles. Sigue la misma lógica del ejemplo de referencia: primero importaciones, luego parámetros, luego secciones numeradas de menor a mayor complejidad.

---

## 📦 Sección 0 — Importaciones

Coloca todas las importaciones al inicio del archivo, antes de cualquier código.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint
```

> **¿Por qué estas librerías?**
> - `numpy`: operaciones matemáticas y arreglos de tiempo.
> - `matplotlib.pyplot`: graficar temperatura vs tiempo.
> - `matplotlib.animation`: crear la animación GIF.
> - `scipy.integrate.odeint`: resolver numéricamente la EDO.

---

## ⚙️ Sección 1 — Parámetros del modelo

Define todas las constantes y condiciones iniciales en un bloque agrupado, con comentarios que expliquen cada variable. Esto facilita cambiarlos para los escenarios del modelo predictivo.

```python
# --- Parámetros del modelo ---
T0    = 90.0   # Temperatura inicial del café (°C)
Ta    = 22.0   # Temperatura ambiente (°C)
k     = 0.07   # Constante de enfriamiento (1/min) — café en taza cerámica
t_fin = 60     # Tiempo total de simulación (minutos)

# Vector de tiempo (600 puntos de 0 a t_fin minutos)
t = np.linspace(0, t_fin, 600)
```

> **Nota:** El valor de `k` representa qué tan rápido se enfría el objeto. Para café en taza cerámica, un valor entre `0.05` y `0.10` es razonable. Este valor se ajusta en los escenarios predictivos.

---

## 📐 Sección 2 — Modelo matemático y solución numérica

### 2.1 Definir la EDO

La ecuación diferencial del Modelo de Enfriamiento de Newton es:

$$\frac{dT}{dt} = -k(T - T_a)$$

Tradúcela a una función Python de la siguiente manera:

```python
# --- Definición de la EDO ---
def modelo_enfriamiento(T, t, k, Ta):
    """
    EDO del Enfriamiento de Newton.
    dT/dt = -k * (T - Ta)
    
    Parámetros:
        T  : temperatura actual del objeto (°C)
        t  : tiempo actual (min) — requerido por odeint aunque no se use explícitamente
        k  : constante de enfriamiento (1/min)
        Ta : temperatura ambiente (°C)
    
    Retorna:
        dTdt : tasa de cambio de temperatura (°C/min)
    """
    dTdt = -k * (T - Ta)
    return dTdt
```

### 2.2 Resolver numéricamente con `odeint`

```python
# --- Solución numérica ---
T_sol = odeint(modelo_enfriamiento, T0, t, args=(k, Ta))
T_sol = T_sol.flatten()  # Convertir de columna a arreglo 1D
```

> `odeint` recibe:
> 1. La función de la EDO
> 2. La condición inicial `T0`
> 3. El vector de tiempo `t`
> 4. `args=(k, Ta)` — parámetros extra que necesita la función

### 2.3 Solución analítica (para comparación)

La solución exacta de la EDO es:

$$T(t) = T_a + (T_0 - T_a) \cdot e^{-kt}$$

Calcúlala en paralelo para validar que la solución numérica es correcta:

```python
# --- Solución analítica ---
T_analitica = Ta + (T0 - Ta) * np.exp(-k * t)
```

---

## 📊 Sección 3 — Gráfica principal: Temperatura vs Tiempo

Genera una gráfica que muestre ambas soluciones (numérica y analítica) sobre la misma figura.

```python
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

print("✔ Gráfica guardada: temperatura_vs_tiempo.png")
```

> **Outputs esperados:**
> - Archivo `temperatura_vs_tiempo.png`
> - Curva descendente exponencial en azul
> - Curva analítica en rojo punteado (debe coincidir casi perfectamente con la numérica)

---

## 🎞️ Sección 4 — Animación GIF

Crea una animación que muestre cómo la temperatura baja con el tiempo. El color del punto cambia de rojo (caliente) a azul (frío) para representar el enfriamiento visualmente.

### 4.1 Preparar la figura de animación

```python
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
```

### 4.2 Funciones de inicialización y actualización

```python
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
    """
    Actualiza cada frame de la animación.
    i : índice del arreglo T_sol correspondiente al frame actual
    """
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
```

### 4.3 Crear y exportar el GIF

```python
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

print("✔ Animación guardada: enfriamiento_cafe.gif")
```

> **Requisito extra:** tener `Pillow` instalado.
> ```bash
> pip install Pillow
> ```

---

## 🔮 Sección 5 — Modelo predictivo (caso café)

Esta sección responde preguntas concretas usando el modelo. Incluye tres análisis:

### 5.1 ¿Cuánto tarda el café en llegar a 60°C (temperatura ideal para beber)?

```python
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
```

### 5.2 Comparar 3 escenarios con distinta temperatura ambiente

```python
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

print("✔ Gráfica guardada: escenario_temperatura_ambiente.png")
```

### 5.3 Comparar 3 escenarios con distinta constante de enfriamiento

```python
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

print("✔ Gráfica guardada: escenario_constante_k.png")
```

---

## 📁 Archivos que debe generar el script al ejecutarse

| Archivo                            | Sección | Descripción                                      |
|------------------------------------|---------|--------------------------------------------------|
| `temperatura_vs_tiempo.png`        | 3       | Gráfica principal con solución numérica y analítica |
| `enfriamiento_cafe.gif`            | 4       | Animación del proceso de enfriamiento            |
| `escenario_temperatura_ambiente.png` | 5     | Comparativa con 3 temperaturas ambientes         |
| `escenario_constante_k.png`        | 5       | Comparativa con 3 valores de k                   |

---

## ✅ Checklist antes de entregar

- [ ] El archivo `.py` ejecuta completo **sin errores** de principio a fin
- [ ] Cada sección tiene un encabezado de comentario tipo `# --- Nombre de sección ---`
- [ ] Todas las funciones tienen docstring explicando parámetros y retorno
- [ ] Los 4 archivos de salida se generan correctamente
- [ ] El GIF muestra cambio de color del punto (rojo → azul)
- [ ] Los resultados del modelo predictivo se imprimen en consola con `print()`
- [ ] Las gráficas tienen título, etiquetas en ejes, leyenda y grid

---

## 🛠️ Dependencias necesarias

```bash
pip install numpy matplotlib scipy Pillow
```

| Librería      | Versión mínima recomendada | Uso en el proyecto                   |
|---------------|----------------------------|--------------------------------------|
| `numpy`       | 1.21+                      | Arreglos de tiempo, exponencial      |
| `matplotlib`  | 3.5+                       | Gráficas y animación                 |
| `scipy`       | 1.7+                       | Resolver la EDO con `odeint`         |
| `Pillow`      | 9.0+                       | Exportar el GIF                      |
