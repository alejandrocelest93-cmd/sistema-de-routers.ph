import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================
st.set_page_config(
    page_title="RouterOptima | CyberEdition",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# INTERFAZ DE ALTO IMPACTO (CSS PERSONALIZADO)
# =========================================================
st.markdown("""
<style>
    /* Fondo con gradiente cósmico / cyberpunk */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
    }
    
    /* Títulos con efecto neón y gradiente de texto */
    h1 {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #f355ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 900 !important;
        font-size: 3rem !important;
        text-shadow: 0px 0px 20px rgba(0, 242, 254, 0.3);
    }
    
    h2, h3, p, span, label {
        color: #e2e8f0 !important;
    }

    /* Tarjetas de contenido con bordes brillantes y fondo translúcido */
    .neon-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(243, 85, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
    }
    
    .neon-card-blue {
        border: 1px solid rgba(0, 242, 254, 0.3);
    }

    /* Modificaciones a inputs y selects para que encajen en el modo oscuro */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #1e293b !important;
        border-radius: 8px !important;
    }
    
    /* Botón de acción ULTRA LLAMATIVO */
    div.stButton > button {
        background: linear-gradient(90deg, #f355ff 0%, #fd3f94 50%, #ff7640 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 30px !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 25px rgba(243, 85, 255, 0.5);
        transition: all 0.4s ease-in-out;
    }
    
    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 40px rgba(253, 63, 148, 0.8);
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# MENÚ LATERAL (CONFIGURACIÓN DE VARIABLES)
# =========================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00f2fe !important;'>⚙️ PANEL DE CONTROL</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<b style='color: #f355ff;'>👥 CAPACIDAD DE USUARIOS</b>", unsafe_allow_html=True)
    st.write("Ajuste el rendimiento de cada equipo:")
    u1 = st.number_input("Router Tipo 1", value=20, step=5)
    u2 = st.number_input("Router Tipo 2", value=50, step=5)
    u3 = st.number_input("Router Tipo 3", value=90, step=5)
    u4 = st.number_input("Router Tipo 4", value=150, step=5)
    
    c = [-u1, -u2, -u3, -u4]

# =========================================================
# CUERPO PRINCIPAL
# =========================================================
st.title("⚡ ROUTER OPTIMA: HARDCORE MILP")
st.markdown("<p style='font-size: 1.2rem; color: #94a3b8 !important;'>Optimización matemática de infraestructura con restricciones críticas en tiempo real.</p>", unsafe_allow_html=True)

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

# Distribución en contenedores de diseño de alta vibración
st.markdown("<div class='neon-card neon-card-blue'>", unsafe_allow_html=True)
st.subheader("📊 Matriz de Coeficientes del Sistema")
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

col_izq, col_der = st.columns(2)

with col_izq:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.subheader("⚙️ Umbrales Operativos (Límites)")
    limites_df = pd.DataFrame({
        "Límite Inferior": [-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, 0],
        "Límite Superior": [500, 300, 40, 120, 80, 750000, np.inf]
    }, index=restricciones)
    limites_editados = st.data_editor(limites_df, use_container_width=True, num_rows="fixed")
    st.markdown("</div>", unsafe_allow_html=True)

with col_der:
    st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
    st.subheader("🧬 Tipo de Variables (Matemática)")
    st.caption("0 = Continua (Variables fluidas) | 1 = Entera (Equipos físicos completos)")
    
    integrality = []
    c1, c2 = st.columns(2)
    for i, var in enumerate(variables):
        target_col = c1 if i < 2 else c2
        with target_col:
            val = st.selectbox(f"{var}", options=[0, 1], index=1, key=f"int_{var}")
            integrality.append(val)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ACCIÓN Y MOTOR MATEMÁTICO
# =========================================================
st.markdown("<div style='text-align: center; margin-top: 30px; margin-bottom: 30px;'>", unsafe_allow_html=True)
resolver = st.button("🔥 LANZAR OPTIMIZADOR INTELIGENTE 🔥")
st.markdown("</div>", unsafe_allow_html=True)

if resolver:
    with st.status("💥 Extrayendo tensores y compilando matriz MILP...", expanded=True) as status:
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
            
            status.update(label="🚀 ¡Solución Óptima Encontrada en Tiempo Récord!", state="complete", expanded=False)
            
            # SECCIÓN DE RESULTADOS DE ALTO IMPACTO VISUAL
            st.markdown("---")
            
            if res.success:
                res_col1, res_col2 = st.columns([1, 1.5])
                
                with res_col1:
                    # Mega widget personalizado con gradiente agresivo y contador gigante
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #00f2fe 0%, #9b51e0 100%); 
                                padding: 35px; border-radius: 20px; text-align: center;
                                box-shadow: 0 10px 30px rgba(0, 242, 254, 0.4);'>
                        <p style='margin:0; font-size: 16px; font-weight: bold; color: white !important; letter-spacing: 2px;'>BENEFICIO MÁXIMO GLOBAL</p>
                        <h1 style='margin:10px 0; color: white !important; -webkit-text-fill-color: white !important; font-size: 55px !important; font-weight: 900;'>{:,}</h1>
                        <p style='margin:0; font-size: 14px; color: rgba(255,255,255,0.8) !important;'>Usuarios totales soportados eficientemente</p>
                    </div>
                    """.format(int(-res.fun)), unsafe_allow_html=True)
                    
                    st.write("")
                    st.success(f"🤖 **Mensaje del Solver:** {res.message}")

                with res_col2:
                    st.markdown("<div class='neon-card' style='border: 1px solid #00f2fe;'>", unsafe_allow_html=True)
                    st.markdown("<h3 style='color: #00f2fe !important; margin-top:0;'>📦 ARQUITECTURA DE RED PROPUESTA</h3>", unsafe_allow_html=True)
                    
                    resultado_df = pd.DataFrame({
                        "Hardware Recomendado": variables,
                        "Unidades Óptimas": np.round(res.x).astype(int)
                    })
                    
                    st.dataframe(
                        resultado_df.set_index("Hardware Recomendado"),
                        use_container_width=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; padding: 20px; border-radius: 12px; text-align: center;'>
                    <h3 style='color: #f87171 !important;'>❌ SISTEMA INVIABLE</h3>
                    <p style='margin:0;'>Las restricciones son demasiado estrictas. Modifica los límites superiores o disminuye los consumos de la matriz.</p>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            status.update(label="Fallo en la simulación", state="error")
            st.error(f"Error crítico en la ejecución del algoritmo: {e}")
