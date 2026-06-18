from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Retail Analytics Engine - Jose Luis Asenjo")

# HTML base para el formulario de entrada con el nuevo parámetro de tiempo
FORM_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Auditoría Retail - Diseñado por Jose Luis Asenjo</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 40px; }
        .container { max-width: 800px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; font-size: 28px; border-bottom: 2px solid #ecf0f1; padding-bottom: 15px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
        label { font-weight: bold; color: #34495e; display: block; margin-top: 10px; font-size: 14px; }
        input, select { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccd1d9; border-radius: 4px; box-sizing: border-box; }
        .optativo { font-size: 11px; background: #e2e8f0; padding: 2px 5px; border-radius: 3px; color: #64748b; margin-left: 5px; }
        button { width: 100%; padding: 15px; margin-top: 30px; background-color: #2980b9; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #3498db; }
        .footer { text-align: center; margin-top: 40px; font-size: 12px; color: #7f8c8d; font-weight: bold; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>KPIs Avanzado Analítica Retail Universal</h1>
        <form action="/calcular" method="post">
            <div class="grid">
                <div>
                    <label>Sector del Negocio:</label>
                    <select name="sector">
                        <option value="General">Retail General</option>
                        <option value="Moda">Moda / Textil</option>
                        <option value="Alimentacion">Alimentación / Supermercado</option>
                        <option value="Tecnologia">Tecnología / Electrónica</option>
                    </select>

                    <label>Periodo Analizado (Días):</label>
                    <input type="number" name="periodo_dias" value="30" min="1" required>

                    <label>Ventas Brutas Totales (€):</label>
                    <input type="number" step="0.01" name="ventas" required>
                    
                    <label>Coste Total de Mercancía (COGS) (€):</label>
                    <input type="number" step="0.01" name="cogs" required>
                </div>
                <div>
                    <label>Unidades Totales Vendidas:</label>
                    <input type="number" name="unidades" required>

                    <label>Número de Transacciones (Tickets):</label>
                    <input type="number" name="transacciones" required>
                    
                    <label>Valor Medio del Inventario (€):</label>
                    <input type="number" step="0.01" name="inventario" required>
                    
                    <label>Superficie Comercial (m²): <span class="optativo">OPTATIVO</span></label>
                    <input type="number" step="0.01" name="superficie" value="0">
                </div>
            </div>
            <button type="submit">Generar Cuadro de Mando</button>
        </form>
        <div class="footer">Diseñado por Jose Luis Asenjo</div>
    </div>
</body>
</html>
"""

# HTML base para los resultados con Chart.js
RESULTS_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resultados - Diseñado por Jose Luis Asenjo</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }
        h2 { color: #34495e; font-size: 18px; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
        
        .grid-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
        .card { background: #f8f9fa; padding: 20px; border-radius: 6px; border-left: 5px solid #2980b9; }
        .card-title { font-size: 12px; color: #7f8c8d; text-transform: uppercase; font-weight: bold; }
        .card-value { font-size: 24px; font-weight: bold; color: #2c3e50; margin-top: 5px; }
        .card-alert { font-size: 12px; font-weight: bold; margin-top: 8px; }
        
        .iet-card { background: #2c3e50; color: white; padding: 25px; border-radius: 8px; text-align: center; margin-top: 20px; }
        .iet-value { font-size: 40px; font-weight: bold; color: #f1c40f; }
        
        .charts-container { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 40px; }
        .chart-box { background: white; padding: 15px; border: 1px solid #ecf0f1; border-radius: 6px; }
        
        a.btn { display: block; text-align: center; margin-top: 40px; padding: 15px; background-color: #95a5a6; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; }
        a.btn:hover { background-color: #7f8c8d; }
        .footer { text-align: center; margin-top: 40px; font-size: 12px; color: #7f8c8d; font-weight: bold; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Análisis Operativo: Sector __SECTOR__ (__DIAS__ días)</h1>
        
        <div class="iet-card">
            <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Índice de Eficiencia Retail (IER)</div>
            <div class="iet-value">__IER__</div>
            <div style="font-size: 13px; margin-top: 5px; color: #bdc3c7;">Métrica global: Cruza Margen, Venta Cruzada y Rotación Temporal</div>
        </div>

        <h2>Métricas Obligatorias (Vitales)</h2>
        <div class="grid-cards">
            <div class="card" style="border-left-color: __COLOR_UPT__;">
                <div class="card-title">UPT (Unidades x Ticket)</div>
                <div class="card-value">__UPT__ uds</div>
                <div class="card-alert" style="color: __COLOR_UPT__;">__ALERTA_UPT__</div>
            </div>
            <div class="card">
                <div class="card-title">Margen Bruto Promedio</div>
                <div class="card-value">__MARGEN__ %</div>
            </div>
            <div class="card" style="border-left-color: __COLOR_DSI__;">
                <div class="card-title">DSI (Días de Rotación Real)</div>
                <div class="card-value">__DSI__ días</div>
                <div class="card-alert" style="color: __COLOR_DSI__;">__ALERTA_DSI__</div>
            </div>
        </div>

        <h2>Métricas Optativas (Secundarias)</h2>
        <div class="grid-cards">
            <div class="card" style="border-left-color: #95a5a6;">
                <div class="card-title">Eficiencia de Espacio Proyectada</div>
                <div class="card-value">__V_M2__ €/m²</div>
            </div>
            <div class="card" style="border-left-color: #95a5a6;">
                <div class="card-title">Stock-to-Sales Ratio</div>
                <div class="card-value">__STS__</div>
            </div>
        </div>

        <div class="charts-container">
            <div class="chart-box">
                <h3 style="text-align:center; font-size:14px; color:#34495e;">Estructura de Ingresos vs Costes</h3>
                <canvas id="chartMargen"></canvas>
            </div>
            <div class="chart-box">
                <h3 style="text-align:center; font-size:14px; color:#34495e;">Rendimiento del Ticket (AOV)</h3>
                <canvas id="chartTicket"></canvas>
            </div>
        </div>

        <a href="/" class="btn">← Realizar Nueva Auditoría</a>
        <div class="footer">DISEÑADO POR JOSE LUIS ASENJO</div>
    </div>

    <script>
        const ctxMargen = document.getElementById('chartMargen').getContext('2d');
        new Chart(ctxMargen, {
            type: 'doughnut',
            data: {
                labels: ['Margen Bruto (€)', 'Coste Producto (€)'],
                datasets: [{
                    data: [__BENEFICIO_EUR__, __COGS_EUR__],
                    backgroundColor: ['#27ae60', '#e74c3c'],
                    borderWidth: 1
                }]
            },
            options: { responsive: true }
        });

        const ctxTicket = document.getElementById('chartTicket').getContext('2d');
        new Chart(ctxTicket, {
            type: 'bar',
            data: {
                labels: ['Valor del Ticket'],
                datasets: [
                    {
                        label: 'Ingreso Medio (AOV)',
                        data: [__AOV__],
                        backgroundColor: '#2980b9'
                    },
                    {
                        label: 'Coste Medio por Ticket',
                        data: [__COSTE_TICKET__],
                        backgroundColor: '#95a5a6'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=FORM_HTML)

@app.post("/calcular", response_class=HTMLResponse)
async def calcular(
    sector: str = Form(...),
    periodo_dias: int = Form(...),
    ventas: float = Form(...),
    cogs: float = Form(...),
    unidades: int = Form(...),
    transacciones: int = Form(...),
    inventario: float = Form(...),
    superficie: float = Form(0)
):
    # 1. Cálculos Base Normalizados por el parámetro Tiempo
    upt = unidades / transacciones if transacciones > 0 else 0
    aov = ventas / transacciones if transacciones > 0 else 0
    coste_por_ticket = cogs / transacciones if transacciones > 0 else 0
    beneficio_bruto = ventas - cogs
    margen_pct = (beneficio_bruto / ventas) * 100 if ventas > 0 else 0
    
    # Integración matemática del parámetro tiempo
    dsi = (inventario / cogs) * periodo_dias if cogs > 0 else 0

    # 2. Cálculos Optativos
    v_m2 = ventas / superficie if superficie > 0 else 0
    sts = inventario / ventas if ventas > 0 else 0

    # 3. Índice de Eficiencia Retail (IER) normalizado
    ier = (upt * margen_pct) / (dsi / 10) if dsi > 0 else 0

    # 4. Umbrales de Alertas Dinámicas por Sector (expresados siempre en días de cobertura de stock)
    umbral_dsi_critico = 45
    umbral_upt_optimo = 1.5

    if sector == "Alimentacion":
        umbral_dsi_critico = 15
        umbral_upt_optimo = 3.0
    elif sector == "Tecnologia":
        umbral_dsi_critico = 60
        umbral_upt_optimo = 1.2

    color_upt = "#27ae60" if upt >= umbral_upt_optimo else "#e74c3c"
    alerta_upt = "OPTIMO" if upt >= umbral_upt_optimo else "REVISAR VENTA CRUZADA"
    
    color_dsi = "#27ae60" if dsi <= umbral_dsi_critico else "#e74c3c"
    alerta_dsi = "ROTACION SANA" if dsi <= umbral_dsi_critico else "STOCK ESTANCADO"

    # 5. Inyección limpia de variables en la interfaz
    html_final = RESULTS_HTML
    html_final = html_final.replace("__SECTOR__", sector)
    html_final = html_final.replace("__DIAS__", str(periodo_dias))
    html_final = html_final.replace("__IER__", f"{ier:.2f}")
    html_final = html_final.replace("__UPT__", f"{upt:.2f}")
    html_final = html_final.replace("__MARGEN__", f"{margen_pct:.2f}")
    html_final = html_final.replace("__DSI__", f"{dsi:.1f}")
    html_final = html_final.replace("__V_M2__", f"{v_m2:.2f}")
    html_final = html_final.replace("__STS__", f"{sts:.2f}")
    
    html_final = html_final.replace("__COLOR_UPT__", color_upt)
    html_final = html_final.replace("__ALERTA_UPT__", alerta_upt)
    html_final = html_final.replace("__COLOR_DSI__", color_dsi)
    html_final = html_final.replace("__ALERTA_DSI__", alerta_dsi)
    
    html_final = html_final.replace("__BENEFICIO_EUR__", f"{beneficio_bruto:.2f}")
    html_final = html_final.replace("__COGS_EUR__", f"{cogs:.2f}")
    html_final = html_final.replace("__AOV__", f"{aov:.2f}")
    html_final = html_final.replace("__COSTE_TICKET__", f"{coste_por_ticket:.2f}")

    return HTMLResponse(content=html_final)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)