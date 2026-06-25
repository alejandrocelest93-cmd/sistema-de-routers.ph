import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Optimización de Infraestructura de Routers",
    page_icon="⚙️",
    layout="wide"
)

# =========================================================
# ESTILO CSS - INTERFAZ PREMIUM "TECH DARK"
# =========================================================

st.markdown("""
<style>
/* Fondo general oscuro y elegante */
.stApp {
    background: linear-gradient(135deg, #0b0f19 0%, #111827 100%);
}

/* Título con gradiente de color eléctrico */
h1 {
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
    margin-bottom: 25px !important;
}

h2, h3, p, span, label {
    color: #f3f4f6 !important;
}

/* Tarjetas flotantes translúcidas para los contenedores */
div[data-testid="stVerticalBlock"] > div {
    background: rgba(31, 41, 55, 0.4);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 10px;
}

/* Botón "Glow" ultra llamativo */
div.stButton > button {
    background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    height: 3.5em !important;
    width: 100%;
    font-size: 16px !important;
    font-weight: bold !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 30px rgba(168, 85, 247, 0.6);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO PRINCIPAL
# =========================================================

st.title("⚙️ Optimización de Infraestructura de Routers")

st.markdown("""
<p style='font-size: 1.1rem; color: #9ca3af !important; margin-bottom: 30px;'>
Modelo de optimización entera para planificación de infraestructura tecnológica.
</p>
""", unsafe_allow_html=True)

# =========================================================
# VARIABLES
# =========================================================

variables = [
    "Routers tipo1",
    "Routers tipo2",
    "Routers tipo3",
    "Routers tipo4"
]

# =========================================================
# DISTRIBUCIÓN EN COLUMNAS PRINCIPALES (LADOS CAMBIADOS)
# =========================================================

panel_izquierdo, panel_derecho = st.columns([1.2, 1])

# ---------------------------------------------------------
# LADO IZQUIERDO: CONFIGURACIÓN DEL MODELO
# ---------------------------------------------------------
with panel_izquierdo:
    
    st.header("🎛️ Parámetros de Entrada")
    
    # --- FUNCIÓN OBJETIVO ---
    st.subheader("🎯 Maximizar Beneficio Total")
    st.write("Ingrese la cantidad de usuarios asociada a cada tipo de router.")
    
    col1, col2, col3, col4 = st.columns(4)
    
    u1 = col1.number_input("Router tipo1", value=20)
    u2 = col2.number_input("Router tipo2", value=50)
    u3 = col3.number_input("Router tipo3", value=90)
    u4 = col4.number_input("Router tipo4", value=150)
    
    # Negativos porque scipy minimiza
    c = [-u1, -u2, -u3, -u4]
    
    # --- RESTRICCIONES ---
    st.subheader("🛡️ Restricciones del Sistema")
    
    restricciones = [
        "Energía",
        "Ancho de Banda",
        "Disponibilidad de Equipos",
        "Disipación Térmica",
        "Personal de Mantenimiento",
        "Cobertura de Routers",
        "Dependencia Mínima"
    ]
    
    A_inicial = pd.DataFrame(
        [
            [6, 12, 25, 40],
            [5, 10, 20, 45],
            [1, 2, 3, 5],
            [2, 4, 15, 20],
            [3, 5, 8, 12],
            [400, 1200, 3000, 7000],
            [1, 0, 0, -2]
        ],
        columns=variables,
        index=restricciones
    )
    
    st.write("**Coeficientes de Restricciones**")
    A_df = st.data_editor(A_inicial, use_container_width=True, num_rows="fixed")
    
    # --- LIMITES ---
    st.write("**Límites de Restricciones**")
    limites_df = pd.DataFrame({
        "Límite Inferior": [1, 1, 1, 1, 1, 1, 1],
        "Límite Superior": [500, 300, 40, 120, 80, 750000, np.inf]
    }, index=restricciones)
    
    limites_editados = st.data_editor(limites_df, use_container_width=True, num_rows="fixed")
    
    # --- TIPO DE VARIABLES ---
    st.subheader("🧬 Tipo de Variables")
    st.caption("0 = Continua  |  1 = Entera")
    
    integrality = []
    cols = st.columns(4)
    for i, var in enumerate(variables):
        val = cols[i].selectbox(f"{var}", options=[0, 1], index=1)
        integrality.append(val)

    st.markdown("<br>", unsafe_allow_html=True)
    ejecutar_optimizacion = st.button("⚡ Ejecutar Motor de Optimización")

# ---------------------------------------------------------
# LADO DERECHO: DISPARADOR Y RESULTADOS EN TIEMPO REAL
# ---------------------------------------------------------
with panel_derecho:
    
    st.header("📊 Panel de Resultados")
    st.write("Presiona el botón de la izquierda para procesar el modelo matemático.")
    
    if ejecutar_optimizacion:
        try:
            A = A_df.values
            bl = limites_editados["Límite Inferior"].values
            bu = limites_editados["Límite Superior"].values

            constraints = LinearConstraint(A, bl, bu)

            bounds = Bounds(
                [0] * len(variables),
                [np.inf] * len(variables)
            )

            res = milp(
                c=c,
                constraints=constraints,
                bounds=bounds,
                integrality=integrality
            )

            st.subheader("✨ Resultado de Optimización")
            st.write("**Estado del Solver:**", res.message)

            if res.success:
                st.success("¡Solución óptima calculada correctamente!")

                # Banner de KPI diseñado a medida con CSS inline y fondo neón
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%); 
                            padding: 30px; border-radius: 16px; text-align: center; margin-top: 15px; margin-bottom: 25px;
                            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3); border: 1px solid rgba(255,255,255,0.1);'>
                    <p style='margin:0; font-size: 13px; font-weight: 700; color: #e0f2fe !important; letter-spacing: 2px; text-transform: uppercase;'>BENEFICIO MÁXIMO LOGRADO</p>
                    <h1 style='margin:10px 0; color: white !important; -webkit-text-fill-color: white !important; font-size: 50px !important; font-weight: 800;'>{round(-res.fun, 2):,}</h1>
                    <p style='margin:0; font-size: 14px; color: #cbd5e1 !important;'>Usuarios totales soportados de forma eficiente</p>
                </div>
                """, unsafe_allow_html=True)

                resultado_df = pd.DataFrame({
                    "Tipo de Router": variables,
                    "Cantidad Óptima": np.round(res.x, 2)
                })

                st.subheader("📦 Cantidad Óptima de Routers")
                st.dataframe(resultado_df, use_container_width=True)

                st.subheader("🔮 Vector Solución raw")
                st.write(res.x)

            else:
                st.error("No se encontró solución factible con los límites actuales.")

        except Exception as e:
            st.error(f"Error en el modelo: {e}")
    else:
        # Estado en espera amigable
        st.info("🤖 Esperando activación... Ajusta las variables a la izquierda y presiona el botón.")
