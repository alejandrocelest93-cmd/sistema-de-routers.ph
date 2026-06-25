import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILO PREMIUM
# =========================================================
st.set_page_config(
    page_title="RouterOptima | UI",
    page_icon="⚡",
    layout="wide"
)

# Inyección de CSS Avanzado para Diseño de Tarjetas y Degradados
st.markdown("""
<style>
    /* Fondo principal con degradado sutil */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Estilo para los títulos principales */
    h1 {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #1E293B !important;
        font-weight: 600 !important;
    }

    /* Tarjetas contenedoras de información */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent;
    }
    
    .card-dashboard {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
    }

    /* Botón de acción principal personalizado */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MENÚ LATERAL (CONFIGURACIÓN DE VARIABLES)
# =========================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/router.png", width=80)
    st.title("Configuración")
    st.markdown("Ajuste la capacidad de usuarios por cada tipo de infraestructura.")
    
    st.subheader("👥 Capacidad de Usuarios")
    u1 = st.number_input("Router Tipo 1", value=20, step=5)
    u2 = st.number_input("Router Tipo 2", value=50, step=5)
    u3 = st.number_input("Router Tipo 3", value=90, step=5)
    u4 = st.number_input("Router Tipo 4", value=150, step=5)
    
    c = [-u1, -u2, -u3, -u4]

# =========================================================
# CUERPO PRINCIPAL
# =========================================================
st.title("⚡ Optimización de Infraestructura de Routers")
st.markdown("### Modelo de programación entera mixta para despliegue tecnológico eficiente.")
st.markdown("---")

# Estructura de Datos Base
variables = ["Routers Tipo 1", "Routers Tipo 2", "Routers Tipo 3", "Routers Tipo 4"]
restricciones = [
    "⚡ Energía (W)", 
    "🌐 Ancho de Banda (Gbps)", 
    "📦 Disponibilidad Equipos", 
    "🔥 Disipación Térmica", 
    "🛠️ Personal Mantenimiento", 
    "🗺️ Cobertura (m²)", 
    "🔗 Dependencia Mínima"
]

# Tabs para organizar la configuración matemática de forma limpia
tab1, tab2 = st.tabs(["📊 Matriz de Coeficientes", "⚙️ Tipos de Variable y Límites"])

with tab1:
    st.markdown("<div class='card-dashboard'>", unsafe_allow_html=True)
    st.write("Modifique los pesos de consumo de recursos de cada equipo:")
    A_inicial = pd.DataFrame([
        [6, 12, 25, 40],
        [5, 10, 20, 45],
        [1, 2, 3, 5],
        [2, 4, 15, 20],
        [3, 5, 8, 12],
        [400, 1200, 3000, 7000],
        [1, 0, 0, -2]
    ], columns=variables, index=restricciones)
    
    A_df = st.data_editor(A_inicial, use_container_width=True, num_rows="fixed")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='card-dashboard'>", unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.write("**Límites Operativos de Restricciones:**")
        # Corregidos los -np.inf para evitar fallos de factibilidad iniciales
        limites_df = pd.DataFrame({
            "Límite Inferior": [-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, 0],
            "Límite Superior": [500, 300, 40, 120, 80, 750000, np.inf]
        }, index=restricciones)
        limites_editados = st.data_editor(limites_df, use_container_width=True, num_rows="fixed")
        
    with col_r:
        st.write("**Naturaleza de Variable:**")
        st.caption("0 = Continua | 1 = Entera")
        integrality = []
        for var in variables:
            val = st.selectbox(f"{var}", options=[0, 1], index=1, key=f"int_{var}")
            integrality.append(val)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PROCESAMIENTO Y EJECUCIÓN
# =========================================================
st.markdown("### 🚀 Ejecución del Sistema")

if st.button("Calcular Despliegue Óptimo"):
    # Animación moderna de carga con st.status
    with st.status("Ejecutando algoritmo MILP de SciPy...", expanded=True) as status:
        try:
            A = A_df.values
            bl = limites_editados["Límite Inferior"].values
            bu = limites_editados["Límite Superior"].values

            constraints = LinearConstraint(A, bl, bu)
            bounds = Bounds([0] * len(variables), [np.inf] * len(variables))

            res = milp(
                c=c,
                constraints=constraints,
                bounds=bounds,
                integrality=integrality
            )
            
            status.update(label="¡Optimización completada con éxito!", state="complete", expanded=False)
            
            # Despliegue estético de resultados
            st.markdown("---")
            st.header("🎯 Resultados del Despliegue")
            
            if res.success:
                c1, c2 = st.columns([1, 2])
                
                with c1:
                    # Tarjeta de KPI principal
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); padding: 20px; border-radius: 12px; color: white;'>
                        <p style='margin:0; font-size: 14px; opacity: 0.9;'>BENEFICIO MÁXIMO</p>
                        <h2 style='margin:0; color: white; font-size: 36px;'>{:,}</h2>
                        <p style='margin:0; font-size: 12px; opacity: 0.8;'>Usuarios totales soportados</p>
                    </div>
                    """.format(int(-res.fun)), unsafe_allow_html=True)
                    
                    st.write("")
                    st.light_泪 = st.info(f"**Estado del Solver:** {res.message}")

                with c2:
                    # Tabla de resultados limpia y formateada como enteros
                    resultado_df = pd.DataFrame({
                        "Infraestructura Recomendada": variables,
                        "Unidades a Instalar": np.round(res.x).astype(int)
                    })
                    
                    st.subheader("📦 Plan de Equipamiento")
                    st.dataframe(
                        resultado_df.set_index("Infraestructura Recomendada"),
                        use_container_width=True
                    )
            else:
                st.error("❌ El modelo no encontró una solución factible con las restricciones dadas.")
                
        except Exception as e:
            status.update(label="Error en el proceso", state="error")
            st.error(f"Ocurrió un error matemático o de compilación: {e}")
