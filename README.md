# 🛒 Retail Analytics Engine: Analítica Avanzada en Streamlit

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una aplicación SaaS orientada a la auditoría operativa y el diagnóstico financiero de infraestructuras comerciales (Retail). Construida sobre **Streamlit**, el sistema procesa datos transaccionales brutos en memoria (arquitectura Zero-Disk) para devolver un análisis volumétrico interactivo en tiempo real.

Este motor implementa **umbrales heurísticos dinámicos** que adaptan las alertas de riesgo (exceso de stock o falta de venta cruzada) según la vertical específica del negocio (Moda, Alimentación, Tecnología, etc.).

---

## 🧮 Motor Matemático y Lógica de Negocio

El núcleo de la aplicación ejecuta el cálculo en tiempo real de **KPIs críticos**. Destaca la formulación propia del **IER (Índice de Eficiencia Retail)**, una métrica multidimensional que cruza la rentabilidad, la profundidad de venta y la rotación.

### 1. Variables Dinámicas de Interacción
- `UPT` (Unidades por Ticket): Unidades / Transacciones
- `AOV` (Average Order Value): Ventas Brutas / Transacciones
- `Margen Bruto`: ((Ventas - COGS) / Ventas) * 100
- `DSI` (Days Sales of Inventory): (Inventario / COGS) * Periodo_dias

### 2. Algoritmo del Índice de Eficiencia Retail (IER)
El IER es una métrica sintética diseñada para evaluar el grado de "salud operativa" del punto de venta o e-commerce. La fórmula premia altos márgenes y alta venta cruzada (UPT), mientras que penaliza severamente la obsolescencia del stock (DSI):

ier = (upt * margen_pct) / (dsi / 10) if dsi > 0 else 0

### 3. Umbrales de Riesgo Heurístico (Sectoriales)
El script aplica lógica de control de flujo para modificar los umbrales de alerta en función de la naturaleza del producto, controlando la volatilidad del inventario:
- **Alimentación (Alta Rotación):** Alerta DSI crítica si > 15 días. UPT óptimo > 3.0.
- **Tecnología (Baja Rotación / Alto Ticket):** Alerta DSI crítica si > 60 días. UPT óptimo > 1.2.
- **Moda / General:** Alerta DSI crítica si > 45 días. UPT óptimo > 1.5.

---

## 🚀 Despliegue en Streamlit Community Cloud

Esta aplicación está optimizada para desplegarse nativamente en la plataforma de Streamlit.

1. Sube este código (`app.py`) y el archivo `requirements.txt` a un repositorio público de GitHub.
2. Inicia sesión en [share.streamlit.io](https://share.streamlit.io).
3. Selecciona "New app", conecta el repositorio y define `app.py` como el Main file path.
4. Haz clic en "Deploy".

---
*Desarrollado y diseñado analíticamente por **Jose Luis Asenjo**.*
