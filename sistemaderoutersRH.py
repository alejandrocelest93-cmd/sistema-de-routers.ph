import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import milp, LinearConstraint, Bounds

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================

st.set_page_config(
    page_title="Optimización de Infraestructura de Routers",
    page_icon="🏢",
    layout="wide"
)

# =========================================================
# ESTILO CSS - MINIMALISTA INDUSTRIAL / TECH NÓRDICO
# =========================================================

st.markdown("""
<style>
/* Fondo gris claro/cemento ultra limpio */
.stApp {
    background-color: #f4f5f7;
}

/* Tipografía y títulos en gris carbón profundo */
h1 {
    color: #1e293b !important;
    font-family: 'Inter', sans-serif;
    font-weight: 700 !important;
    font-size: 2.3rem !important;
    letter-spacing: -0.5px;
    margin-bottom: 20px !important;
}

h2 {
    color: #334155 !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 8px;
    margin-top: 20px !important;
}

h3, p, span, label {
    color: #475569 !important;
}

/* Tarjetas blancas puras con bordes suaves y sombras sutiles */
div[data-testid="stVerticalBlock"] > div {
    background-color: #ffffff;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.02);
    padding: 15px;
}

/* Botón sólido en Verde Esmeralda Industrial */
div.stButton > button {
    background-color: #0f766e !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
    height: 3.2em !important;
    width: 100%;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    transition: background-color 0.2s ease;
}

div.stButton > button:hover {
    background-color: #115e59 !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TÍTULO
# =========================================================

st.title("🏢 Planificación de Infraestructura: Routers")

st.markdown("""
<p style='color: #64748b !important; margin-bottom: 25px; font-size: 1rem;'>
Panel de ingeniería y optimización entera lineal para el despliegue eficiente de recursos tecnológicos.
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
# DISTRIBUCIÓN EN MATRIZ SUPERIOR (3 COLUMNAS DE CONTROL)
# =========================================================

bloque_usuarios, bloque_coeficientes, bloque_limites = st.columns([1, 1.5, 1.2])

# --- COLUMNA 1: FUNCIÓN OBJETIVO ---
with bloque_usuarios:
    st.header("👥 Capacidad de Usuarios")
    st.caption("Especifique la carga de usuarios objetivo por dispositivo.")
    
    u1 = st.number_input("Router tipo1", value=20, key="u1")
    u2 = st.number_input("Router tipo2", value=50, key="u2")
    u3 = st.number_input("Router tipo3", value=90, key="u3")
    u4 = st.number_input("Router tipo4", value=150, key="u4")
    
    # Negativos porque scipy minimiza
    c = [-u1, -u2, -u3, -u4]

# --- RESTRICCIONES COMPARTIDAS ---
restricciones = [
    "Energía",
    "Ancho de Banda",
    "Disponibilidad de Equipos",
    "Disipación Térmica",
    "Personal de Mantenimiento",
    "Cobertura de Routers",
    "Dependencia Mínima"
]

# --- COLUMNA 2: MATRIZ DE COEFICIENTES ---
with bloque_coeficientes:
    st.header("📊 Matriz Tecnológica")
    st.caption("Coeficientes de consumo e impacto por tipo de router.")
    
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
    
    A_df = st.data_editor(
        A_inicial,
        use_container_width=True,
        num_rows="fixed",
        key="editor_A"
    )

# --- COLUMNA 3: LIMITES Y NATURALEZA ---
with bloque_limites:
    st.header("⚙️ Umbrales Operativos")
    st.caption("Límites del entorno y tipo de variable (0: Cont. | 1: Ent.)")
    
    limites_df = pd.DataFrame({
        "Límite Inferior": [1, 1, 1, 1, 1, 1, 1],
        "Límite Superior": [500, 300, 40, 120, 80, 750000, np.inf]
    }, index=restricciones)
    
    limites_editados = st.data_editor(
        limites_df,
        use_container_width=True,
        num_rows="fixed",
        key="editor_lim"
    )
    
    # Renderizado en línea de los selectboxes para ahorrar espacio
    integrality = []
    sub_cols = st.columns(4)
    for i, var in enumerate(variables):
        val = sub_cols[i].selectbox(
            f"R{i+1}",
            options=[0, 1],
            index=1,
            help=f"Tipo de variable para {var}"
        )
        integrality.append(val)

# =========================================================
# ACCIÓN CENTRAL
# =========================================================

st.markdown("<div style='margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
calcular = st.button("Calcular Configuración de Infraestructura")
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SECCIÓN INFERIOR: RESULTADOS DEL SISTEMA
# =========================================================

if calcular:
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

        st.header("✨ Diagnóstico y Resultados")
        st.write("**Estado de ejecución:**", res.message)

        if res.success:
            
            # Distribución limpia de los resultados en dos bloques inferiores
            col_resultado_1, col_resultado_2 = st.columns([1, 1.5])
            
            with col_resultado_1:
                # Banner minimalista premium para el KPI
                st.markdown(f"""
                <div style='background-color: #115e59; padding: 25px; border-radius: 10px; text-align: center;'>
                    <p style='margin:0; font-size: 12px; font-weight: 600; color: #ccfbf1 !important; letter-spacing: 1px;'>BENEFICIO MÁXIMO CALCULADO</p>
                    <h1 style='margin:10px 0; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; font-size: 42px !important;'>{round(-res.fun, 2):,}</h1>
                    <p style='margin:0; font-size: 13px; color: #99f6e4 !important;'>Usuarios totales soportados</p>
                </div>
                """, unsafe_allow_html=True)

            with col_resultado_2:
                resultado_df = pd.DataFrame({
                    "Tipo de Router": variables,
                    "Cantidad Óptima": np.round(res.x, 2)
                })
                
                st.dataframe(
                    resultado_df,
                    use_container_width=True
                )
                
                st.write("**Vector Solución:**", res.x)

        else:
            st.error("No se encontró solución factible con los parámetros provistos.")

    except Exception as e:
        st.error(f"Error en el modelo: {e}")
