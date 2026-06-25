import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# MAQUILLAJE DE LA INTERFAZ (CONFIGURACIÓN)
# =========================================================

st.set_page_config(
    page_title="RouterOptima v2.0 | Inteligencia de Red",
    layout="wide"
)

# =========================================================
# ESTILO CSS - REVOLUCIÓN RETRO-SYNTH (SIN FONDO BLANCO)
# =========================================================

st.markdown("""
<style>
/* Fondo profundo de la app en azul medianoche/morado */
.stApp {
    background-color: #1a103c;
}

/* Títulos con gradiente de color Retro-Fucsia a Amarillo Eléctrico */
h1 {
    background: linear-gradient(90deg, #ff007f 0%, #ff00ff 50%, #ffea00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Impact', 'Arial Black', sans-serif;
    font-weight: bold !important;
    font-size: 3rem !important;
    letter-spacing: 1px;
}

h2 {
    color: #ff00ff !important;
    font-size: 1.6rem !important;
    font-weight: bold !important;
    border-bottom: 2px dashed #ffea00;
    padding-bottom: 5px;
}

h3, p, span, label {
    color: #00ffff !important;
    font-weight: 500;
}

/* Contenedores con fondo morado medio y bordes cian neón */
div[data-testid="stVerticalBlock"] > div {
    background-color: #24144b;
    border-radius: 16px;
    border: 2px solid #00ffff;
    box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.2);
    padding: 20px;
}

/* Modificación de data editors para que entonen con el modo oscuro */
div[data-testid="stDataEditor"] {
    background-color: #1a103c !important;
}

/* Botón de acción ultra-llamativo estilo retro rectangular */
div.stButton > button {
    background: linear-gradient(45deg, #ff007f 0%, #7000ff 100%) !important;
    color: #ffea00 !important;
    border-radius: 0px !important; 
    border: 3px solid #ffea00 !important;
    height: 3.5em !important;
    width: 100%;
    font-size: 18px !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 5px 5px 0px #00ffff;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0px #00ffff;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO PRINCIPAL (UPGRADE VISUAL)
# =========================================================

st.title("⚡ MATRIX_OPT: ARQUITECTURA DE ROUTERS SUPERESTRELLA")

st.markdown("""
<p style='color: #ffea00 !important; margin-bottom: 30px; font-size: 1.1rem; font-family: monospace;'>
[ALGORITMO MILP AVANZADO PARA MAXIMIZAR EL DESPLIEGUE DE RED EN TIEMPO REAL]
</p>
""", unsafe_allow_html=True)

# =========================================================
# CAPAS DE HARDWARE (MÉTRICAS BASE)
# =========================================================

variables = [
    "Routers tipo1",
    "Routers tipo2",
    "Routers tipo3",
    "Routers tipo4"
]

# =========================================================
# MOTOR DE BENEFICIOS (FUNCIÓN OBJETIVO)
# =========================================================

st.header("🎯 PODER DE TRÁFICO: MAXIMIZAR CONECTIVIDAD")

st.write("""
Ajuste el impacto de usuarios potenciales que soportará cada nivel de hardware.
""")

col1, col2, col3, col4 = st.columns(4)

u1 = col1.number_input(
    "Cantidad de usuarios - Router tipo1",
    value=20
)

u2 = col2.number_input(
    "Cantidad de usuarios - Router tipo2",
    value=50
)

u3 = col3.number_input(
    "Cantidad de usuarios - Router tipo3",
    value=90
)

u4 = col4.number_input(
    "Cantidad de usuarios - Router tipo4",
    value=150
)

# Multiplicadores negativos para engañar al minimizador de scipy
c = [-u1, -u2, -u3, -u4]

# =========================================================
# RESTRICCIONES CRÍTICAS DEL ENTORNO
# =========================================================

st.header("🛑 BARRERAS Y RESTRICCIONES DEL ENTORNO")

restricciones = [
    "Energía",
    "Ancho de Banda",
    "Disponibilidad de Equipos",
    "Disipación Térmica",
    "Personal de Mantenimiento",
    "Cobertura de Routers",
    "Dependencia Mínima"
]

# =========================================================
# MATRIZ DE CONSUMO TECNOLÓGICO
# =========================================================

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

st.subheader("📊 Coeficientes de Consumo de Recursos")

A_df = st.data_editor(
    A_inicial,
    use_container_width=True,
    num_rows="fixed"
)

# =========================================================
# CAPACIDAD MÁXIMA PERMITIDA (LÍMITES)
# =========================================================

st.subheader("⚙️ Umbrales Críticos Operativos (Mín / Máx)")

limites_df = pd.DataFrame({
    "Límite Inferior": [1, 1, 1, 1, 1, 1, 1],
    "Límite Superior": [500, 300, 40, 120, 80, 750000, np.inf]
}, index=restricciones)

limites_editados = st.data_editor(
    limites_df,
    use_container_width=True,
    num_rows="fixed"
)

# =========================================================
# COMPORTAMIENTO MATEMÁTICO (NATURALEZA DE VARIABLE)
# =========================================================

st.subheader("🧬 Topología de Variables")

st.write("""
0 = Escalar Continua (Fracciones) | 1 = Entera Rígida (Equipos Físicos)
""")

integrality = []

cols = st.columns(4)

for i, var in enumerate(variables):

    val = cols[i].selectbox(
        f"{var}",
        options=[0, 1],
        index=1
    )

    integrality.append(val)

# =========================================================
# IGNICIÓN DEL RESOLVEDOR (CÁLCULO)
# =========================================================

if st.button("🔥 DISPARAR OPTIMIZACIÓN DE INFRAESTRUCTURA 🔥"):

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

        st.header("🔮 PREDICCIÓN Y RESULTADOS DE RED")

        st.write("Estado del Motor:", res.message)

        if res.success:

            st.success("¡Despliegue matemático resuelto con éxito!")

            # Bloque de salida destacado con marquesina Retro / Synth
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ff007f 0%, #7000ff 100%); 
                        padding: 30px; border: 3px solid #00ffff; text-align: center;
                        box-shadow: 8px 8px 0px #ffea00; margin-bottom: 25px;'>
                <p style='margin:0; font-size: 14px; font-weight: bold; color: #ffea00 !important; letter-spacing: 2px;'>MÁXIMO FLUJO DE USUARIOS LOGRADO</p>
                <h1 style='margin:15px 0; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-size: 50px !important; font-family: Impact;'>{round(-res.fun, 2):,}</h1>
                <p style='margin:0; font-size: 13px; color: #00ffff !important;'>CAPACIDAD TOTAL SOPORTADA</p>
            </div>
            """, unsafe_allow_html=True)

            resultado_df = pd.DataFrame({
                "Tipo de Router": variables,
                "Cantidad Óptima": np.round(res.x, 2)
            })

            st.subheader("📦 Plan Técnico: Unidades Recomendadas")

            st.dataframe(
                resultado_df,
                use_container_width=True
            )

            st.subheader("🔮 Vector de Configuración Final")

            st.write(res.x)

        else:
            st.error("Error: Las restricciones del sistema bloquean cualquier combinación matemática viable.")

    except Exception as e:
        st.error(f"Fallo en el núcleo matemático: {e}")
