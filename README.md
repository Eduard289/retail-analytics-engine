# 🛒 Retail Analytics Engine: Motor Analítico Asíncrono en FastAPI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.0+-009688.svg)](https://fastapi.tiangolo.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-3.0+-FF6384.svg)](https://www.chartjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un microservicio de alto rendimiento diseñado para la auditoría operativa y el diagnóstico financiero de infraestructuras comerciales (Retail). Construido sobre **FastAPI**, el sistema aplica una arquitectura *Stateless* (Zero-Disk) para ingerir datos transaccionales brutos y devolver un análisis volumétrico en tiempo real, garantizando absoluta privacidad al no persistir información en bases de datos.

Este motor no solo calcula métricas estándar, sino que implementa **umbrales heurísticos dinámicos** que adaptan las alertas de riesgo (exceso de stock o falta de venta cruzada) según la vertical específica del negocio (Moda, Alimentación, Tecnología, etc.).

---

## ⚙️ Arquitectura del Sistema

El ecosistema opera bajo un paradigma de inyección de plantillas HTML desde el servidor con manipulación del DOM delegada al cliente, optimizando así la carga de procesamiento del VPS:

1. **Backend (FastAPI & Uvicorn):** Gestión de enrutamiento asíncrono (`async def`). Utiliza la validación estricta de tipos mediante la dependencia `Form(...)` de Starlette para sanitizar los inputs antes del cálculo matemático.
2. **Motor de Inferencia (Python):** Procesamiento algebraico de variables de negocio (Ventas, COGS, Tráfico, Inventario) normalizadas bajo un parámetro de control temporal (`periodo_dias`).
3. **Frontend Dinámico (HTML5 + CSS3):** Interfaz inyectada directamente en la respuesta HTTP (`HTMLResponse`), eliminando la necesidad de motores de plantillas pesados (como Jinja2) para reducir la latencia de respuesta (TTFB).
4. **Capa de Visualización (Chart.js):** Renderizado de gráficos vectoriales en el lado del cliente (Client-Side Rendering) a partir de variables inyectadas estáticamente por el backend.

---

## 🧮 Motor Matemático y Lógica de Negocio

El núcleo de la aplicación ejecuta el cálculo en tiempo real de **KPIs críticos (Key Performance Indicators)**. Destaca la formulación propia del **IER (Índice de Eficiencia Retail)**, una métrica multidimensional que cruza la rentabilidad, la profundidad de venta y la rotación.

### 1. Variables Dinámicas de Interacción
- `UPT` (Unidades por Ticket): $Unidades / Transacciones$
- `AOV` (Average Order Value): $Ventas Brutas / Transacciones$
- `Margen Bruto`: $((Ventas - COGS) / Ventas) \times 100$
- `DSI` (Days Sales of Inventory): $(Inventario / COGS) \times Periodo_{dias}$

### 2. Algoritmo del Índice de Eficiencia Retail (IER)
El IER es una métrica sintética diseñada para evaluar el grado de "salud operativa" del punto de venta o e-commerce. La fórmula premia altos márgenes y alta venta cruzada (UPT), mientras que penaliza severamente la obsolescencia del stock (DSI):

ier = (upt * margen_pct) / (dsi / 10) if dsi > 0 else 0

### 3. Umbrales de Riesgo Heurístico (Sectoriales)
El script aplica lógica de control de flujo para modificar los umbrales de alerta en función de la naturaleza del producto, controlando la volatilidad del inventario:
- **Alimentación (Alta Rotación):** Alerta DSI crítica si > 15 días. UPT óptimo > 3.0.
- **Tecnología (Baja Rotación / Alto Ticket):** Alerta DSI crítica si > 60 días. UPT óptimo > 1.2.
- **Moda / General:** Alerta DSI crítica si > 45 días. UPT óptimo > 1.5.

---

## 🚀 Despliegue e Instalación

Gracias a su enfoque monolítico ligero, la aplicación puede desplegarse en cualquier contenedor Docker, VPS o entorno local en segundos.

### Requisitos Previos
- Python 3.9 o superior.
- Gestor de paquetes `pip`.

### Instalación en Entorno Virtual (Recomendado)

# 1. Clonar el repositorio
git clone https://github.com/TuUsuario/retail-analytics-engine.git
cd retail-analytics-engine

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias core
pip install fastapi uvicorn

### Ejecución del Servidor ASGI

Levanta el servidor Uvicorn en modo producción o desarrollo local:

uvicorn MetricasKPIs:app --host 0.0.0.0 --port 8000 --reload

La interfaz de auditoría estará disponible de forma asíncrona en `http://localhost:8000`.

---

## 🛡️ Seguridad y Privacidad (Zero-Disk)

Esta herramienta está construida respetando estrictamente el paradigma **Zero-Disk Processing**. 
Toda la manipulación de variables financieras, cálculos de costes de mercancía (COGS) y ratios de conversión ocurre exclusivamente en la **memoria RAM volátil (RAM Processing)** durante el ciclo de vida de la petición POST. Una vez renderizado y enviado el HTML al cliente, las variables son destruidas por el *Garbage Collector* de Python, haciendo imposible la filtración de datos corporativos a través del servidor.

---
*Desarrollado y mantenido por **Jose Luis Asenjo**.*
