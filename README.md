# Modelado y Simulación del Enfriamiento de Newton
### Caso aplicado: Enfriamiento de una taza de café

---

## Resumen

El presente trabajo tiene como propósito modelar, simular y analizar el proceso de enfriamiento de un objeto en función del tiempo, utilizando la **Ley de Enfriamiento de Newton** como fundamento matemático. Esta ley establece que la tasa de cambio de temperatura de un cuerpo es directamente proporcional a la diferencia entre la temperatura del objeto y la del medio circundante, lo que conduce a la siguiente ecuación diferencial ordinaria:

$$\frac{dT}{dt} = -k(T - T_a)$$

cuya solución analítica describe un **decaimiento exponencial** de la temperatura a lo largo del tiempo.

Como caso de aplicación, se modela el enfriamiento de una taza de café en un ambiente a temperatura constante, estimando el tiempo necesario para que el café alcance una temperatura adecuada de consumo bajo distintos escenarios.

Para la implementación computacional se emplearon las siguientes bibliotecas de Python:

- **NumPy** — manejo de arreglos y operaciones matemáticas
- **SciPy** — resolución numérica de la ecuación diferencial
- **Matplotlib** — generación de gráficas y animaciones del proceso

Los resultados obtenidos muestran consistencia con el comportamiento exponencial predicho por el modelo teórico, validando su aplicabilidad en contextos cotidianos e ingenieriles.

---

## Objetivos de la actividad

- ✓ Modelar matemáticamente un fenómeno térmico mediante EDO
- ✓ Implementar soluciones numéricas en Python
- ✓ Generar visualizaciones dinámicas del proceso de enfriamiento
- ✓ Desarrollar un modelo predictivo aplicado a la vida cotidiana

---

## Autoras

| Nombre | Correo institucional |
|---|---|
| Emilia Gómez Utrilla | 243700@ids.upchiapas.edu.mx |
| Nadia Guerra Cuessy | 243751@ids.upchiapas.edu.mx |
| Emma Reyes Preciado | 243765@ids.upchiapas.edu.mx |

---

## Requisitos

Antes de ejecutar el programa, asegúrate de tener **Python 3.8 o superior** instalado. Luego instala las dependencias necesarias con el siguiente comando:

```bash
pip install numpy matplotlib scipy Pillow
```

| Librería | Versión mínima recomendada |
|---|---|
| numpy | 1.21+ |
| matplotlib | 3.5+ |
| scipy | 1.7+ |
| Pillow | 9.0+ |

---

## Cómo ejecutar el programa

1. Descarga o clona este repositorio en tu computadora.

2. Abre una terminal (cmd, PowerShell o terminal de tu sistema operativo) en la carpeta donde se encuentra el archivo.

3. Instala las dependencias (si aún no lo has hecho):

```bash
pip install numpy matplotlib scipy Pillow
```

4. Ejecuta el script:

```bash
python enfriamiento_newton.py
```

5. Durante la ejecución, el programa mostrará una ventana con la gráfica principal. **Ciérrala** para que el programa continúe generando los demás archivos.

---

## Archivos generados

Al terminar la ejecución, el script produce automáticamente los siguientes archivos en la misma carpeta:

| Archivo | Descripción |
|---|---|
| `temperatura_vs_tiempo.png` | Gráfica principal con la solución numérica y analítica |
| `enfriamiento_cafe.gif` | Animación del proceso de enfriamiento |
| `escenario_temperatura_ambiente.png` | Comparativa con 3 temperaturas ambientes distintas |
| `escenario_constante_k.png` | Comparativa con 3 valores de la constante de enfriamiento |

Además, en la consola se imprime el tiempo estimado en que el café alcanza **60°C**, la temperatura ideal para consumirlo.

---

## Estructura del código

El archivo `enfriamiento_newton.py` está organizado en **5 secciones secuenciales**:

| Sección | Descripción |
|---|---|
| 0 — Importaciones | Carga de bibliotecas necesarias |
| 1 — Parámetros del modelo | Definición de constantes y condiciones iniciales |
| 2 — Modelo matemático | Definición de la EDO y su solución numérica y analítica |
| 3 — Gráfica principal | Visualización de temperatura vs. tiempo |
| 4 — Animación GIF | Simulación animada del enfriamiento con cambio de color |
| 5 — Modelo predictivo | Análisis de escenarios y estimación de tiempos |
