import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Retail Analytics Engine", layout="wide", page_icon="🛒")

st.title("🛒 Retail Analytics Engine")
st.markdown("Motor de auditoría operativa y diagnóstico financiero interactivo.")

# ==========================================
# 1. PANEL DE ENTRADA DE DATOS (SIDEBAR)
# ==========================================
st.sidebar.header("⚙️ Parámetros de Auditoría")

sector = st.sidebar.selectbox(
    "Sector del Negocio:",
    ("General", "Moda", "Alimentacion", "Tecnologia")
)

periodo_dias = st.sidebar.number_input("Periodo Analizado (Días):", min_value=1, value=30)
ventas = st.sidebar.number_input("Ventas Brutas Totales (€):", min_value=0.0, value=50000.0, step=100.0)
cogs = st.sidebar.number_input("Coste Total Mercancía (COGS) (€):", min_value=0.0, value=20000.0, step=100.0)
unidades = st.sidebar.number_input("Unidades Totales Vendidas:", min_value=0, value=1500)
transacciones = st.sidebar.number_input("Número de Transacciones (Tickets):", min_value=0, value=800)
inventario = st.sidebar.number_input("Valor Medio Inventario (€):", min_value=0.0, value=15000.0, step=100.0)
superficie = st.sidebar.number_input("Superficie Comercial (m²) - Optativo:", min_value=0.0, value=100.0)

# Botón de ejecución
calcular = st.sidebar.button("Generar Cuadro de Mando", use_container_width=True)

# ==========================================
# 2. MOTOR MATEMÁTICO Y LÓGICA DE NEGOCIO
# ==========================================
if calcular or ventas > 0: # Se ejecuta al pulsar el botón o por defecto si hay datos
    
    # Normalización de cálculos base
    upt = unidades / transacciones if transacciones > 0 else 0
    aov = ventas / transacciones if transacciones > 0 else 0
    coste_por_ticket = cogs / transacciones if transacciones > 0 else 0
    beneficio_bruto = ventas - cogs
    margen_pct = (beneficio_bruto / ventas) * 100 if ventas > 0 else 0
    
    # Integración del parámetro tiempo
    dsi = (inventario / cogs) * periodo_dias if cogs > 0 else 0
    
    # Cálculos optativos
    v_m2 = ventas / superficie if superficie > 0 else 0
    sts = inventario / ventas if ventas > 0 else 0

    # Índice de Eficiencia Retail (IER)
    ier = (upt * margen_pct) / (dsi / 10) if dsi > 0 else 0

    # Umbrales Heurísticos Dinámicos
    umbral_dsi_critico = 45
    umbral_upt_optimo = 1.5

    if sector == "Alimentacion":
        umbral_dsi_critico = 15
        umbral_upt_optimo = 3.0
    elif sector == "Tecnologia":
        umbral_dsi_critico = 60
        umbral_upt_optimo = 1.2

    # Generación de alertas
    alerta_upt = "✅ ÓPTIMO" if upt >= umbral_upt_optimo else "⚠️ REVISAR VENTA CRUZADA"
    alerta_dsi = "✅ ROTACIÓN SANA" if dsi <= umbral_dsi_critico else "🚨 STOCK ESTANCADO"

    # ==========================================
    # 3. INTERFAZ Y VISUALIZACIÓN DE DATOS (DASHBOARD)
    # ==========================================
    
    st.markdown("---")
    st.subheader(f"📊 Análisis Operativo: Sector {sector} ({periodo_dias} días)")
    
    # Tarjeta destacada IER
    st.info(f"**Índice de Eficiencia Retail (IER): {ier:.2f}** \n*Métrica sintética que cruza Rentabilidad, Profundidad de Venta y Rotación temporal.*")

    # Fila 1: Métricas Vitales
    st.markdown("#### Métricas Vitales")
    col1, col2, col3 = st.columns(3)
    col1.metric("UPT (Unidades x Ticket)", f"{upt:.2f} uds", delta=alerta_upt, delta_color="normal" if upt >= umbral_upt_optimo else "inverse")
    col2.metric("Margen Bruto Promedio", f"{margen_pct:.2f} %")
    col3.metric("DSI (Días de Rotación Real)", f"{dsi:.1f} días", delta=alerta_dsi, delta_color="normal" if dsi <= umbral_dsi_critico else "inverse")

    # Fila 2: Métricas Optativas
    st.markdown("#### Métricas Secundarias")
    col4, col5, col6 = st.columns(3)
    col4.metric("AOV (Ingreso Medio)", f"{aov:.2f} €")
    col5.metric("Eficiencia de Espacio", f"{v_m2:.2f} €/m²")
    col6.metric("Stock-to-Sales Ratio", f"{sts:.2f}")

    st.markdown("---")
    
    # Fila 3: Gráficos con Plotly
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("<h5 style='text-align: center;'>Estructura de Ingresos vs Costes</h5>", unsafe_allow_html=True)
        fig_donut = px.pie(
            values=[beneficio_bruto, cogs], 
            names=['Margen Bruto (€)', 'Coste Producto COGS (€)'],
            hole=0.5,
            color_discrete_sequence=['#27ae60', '#e74c3c']
        )
        fig_donut.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_chart2:
        st.markdown("<h5 style='text-align: center;'>Rendimiento del Ticket (AOV)</h5>", unsafe_allow_html=True)
        fig_bar = go.Figure(data=[
            go.Bar(name='Ingreso Medio (AOV)', x=['Ticket'], y=[aov], marker_color='#2980b9'),
            go.Bar(name='Coste Medio por Ticket', x=['Ticket'], y=[coste_por_ticket], marker_color='#95a5a6')
        ])
        fig_bar.update_layout(barmode='group', margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("👈 Configura los parámetros en el menú lateral y pulsa 'Generar Cuadro de Mando'.")
