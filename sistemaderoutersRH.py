import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================
st.set_page_config(
    page_title="OptiNetwork | Router Infrastructure",
    page_icon="🌐",
    layout="wide"
)

# =========================================================
# ESTILO CSS PERSONALIZADO
# =========================================================
st.markdown("""
<style>
    /* Fondo y fuentes */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Títulos y Headers */
    h1, h2, h3, .stMarkdown {
        color: #2dd4bf !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedores de métricas */
    [data-testid="stMetricValue"] {
        color: #2dd4bf !important;
        font-size: 36px !important;
    }
    
    /* Botones */
    div.stButton > button {
        background-color: #2dd4bf;
        color: #0f172a;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #5eead4;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(45, 212, 191, 0.4);
    }
    
    /* Dataframes con estilo oscuro */
    [data-testid="stDataFrame"] {
        background-color: #1e293b;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR - CONFIGURACIÓN
# =========================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067451.png", width=80)
    st.title("Network Config")
    st.markdown("---")
    
    st.subheader("Beneficio por Tipo")
    u1 = st.number_input("Usuarios Router T1", value=20)
    u2 = st.number_input("Usuarios Router T2", value=50)
    u3 = st.number_input("Usuarios Router T3", value=90)
    u4 = st.number_input("Usuarios Router T4", value=150)
    
    st.markdown("---")
    st.info("Este modelo utiliza Programación Lineal Entera Mixta (MILP) para maximizar la capacidad de usuarios.")

# =========================================================
# HEADER PRINCIPAL
# =========================================================
st.title("🌐 Optimización de Infraestructura de Routers")
st.markdown("##### Estrategia de escalado basada en algoritmos de optimización matemática")

# Pestañas para organizar la UI
tab_data, tab_const, tab_solve = st.tabs(["📊 Datos de Entrada", "🛡️ Restricciones", "🚀 Resolución"])

variables = ["Routers Tipo 1", "Routers Tipo 2", "Routers Tipo 3", "Routers Tipo 4"]
restricciones = [
    "Energía (W)", "Ancho de Banda (Gb)", "Stock Equipos", 
    "Disipación (BTU)", "Personal Manto.", "Cobertura (m2)", "Dependencia"
]

# PESTAÑA 1: DATOS
with tab_data:
    st.subheader("Matriz de Coeficientes Técnicos")
    A_inicial = pd.DataFrame(
        [
            [6, 12, 25, 40], [5, 10, 20, 45], [1, 2, 3, 5],
            [2, 4, 15, 20], [3, 5, 8, 12], [400, 1200, 3000, 7000], [1, 0, 0, -2]
        ],
        columns=variables, index=restricciones
    )
    A_df = st.data_editor(A_inicial, use_container_width=True)

# PESTAÑA 2: RESTRICCIONES
with tab_const:
    st.subheader("Definición de Límites Operativos")
    limites_df = pd.DataFrame({
        "Límite Mín": [1, 1, 1, 1, 1, 1, 1],
        "Límite Máx": [500, 300, 40, 120, 80, 750000, np.inf]
    }, index=restricciones)
    limites_editados = st.data_editor(limites_df, use_container_width=True)

# PESTAÑA 3: RESOLUCIÓN
with tab_solve:
    c = [-u1, -u2, -u3, -u4]  # Maximizar es minimizar el negativo
    
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        btn_solve = st.button("EJECUTAR OPTIMIZACIÓN")
    
    if btn_solve:
        with st.spinner("Calculando solución óptima..."):
            try:
                # Preparar datos
                A = A_df.values
                bl = limites_editados["Límite Mín"].values
                bu = limites_editados["Límite Máx"].values
                constraints = LinearConstraint(A, bl, bu)
                bounds = Bounds([0]*4, [np.inf]*4)
                integrality = [1, 1, 1, 1]  # Forzamos variables enteras
                
                # Solver
                res = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)
                
                if res.success:
                    st.success("🎯 Solución óptima encontrada exitosamente")
                    
                    # Dashboard de resultados
                    res_col1, res_col2 = st.columns([1, 2])
                    
                    with res_col1:
                        st.metric("Beneficio (Usuarios)", int(-res.fun))
                        
                        df_res = pd.DataFrame({
                            "Router": variables,
                            "Cantidad": res.x
                        })
                        st.table(df_res)
                    
                    with res_col2:
                        # Gráfico Plotly
                        fig = px.bar(df_res, x="Router", y="Cantidad", 
                                     title="Distribución Óptima de Equipos",
                                     color_discrete_sequence=['#2dd4bf'])
                        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font_color="#f8fafc"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"Error: {res.message}")
            except Exception as e:
                st.error(f"Error técnico: {e}")
