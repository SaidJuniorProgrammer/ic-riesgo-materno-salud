import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tamizaje de Riesgo Materno - Salud Pública",
    page_icon=":material/monitor_heart:",
    layout="centered"
)

# Estilos CSS e íconos vectoriales Lucide (SVG)
st.markdown("""
<style>
    .lucide-header {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    .lucide-subheader {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 1.2rem;
        margin-bottom: 0.75rem;
    }
    .lucide-icon {
        stroke: #0284c7;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
        flex-shrink: 0;
    }
</style>
""", unsafe_allow_html=True)

LUCIDE_SVGS = {
    "heart_pulse": '<svg class="lucide-icon" width="32" height="32" viewBox="0 0 24 24"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/></svg>',
    "sliders": '<svg class="lucide-icon" width="20" height="20" viewBox="0 0 24 24"><line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="2" x2="6" y1="14" y2="14"/><line x1="10" x2="14" y1="8" y2="8"/><line x1="18" x2="22" y1="16" y2="16"/></svg>',
    "stethoscope": '<svg class="lucide-icon" width="20" height="20" viewBox="0 0 24 24"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>',
    "activity": '<svg class="lucide-icon" width="20" height="20" viewBox="0 0 24 24"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/></svg>',
}

# Busca primero el modelo recién entrenado (pipeline_riesgo_materno.joblib)
MODEL_PATH = os.path.join("models", "pipeline_riesgo_materno.joblib")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join("models", "pipeline_materno_final.joblib")


@st.cache_resource
def load_pipeline():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def validar_entradas(age, sys_bp, dia_bp, bs_mmol, temp_f, hr):
    errores = []
    advertencias = []

    if sys_bp <= dia_bp:
        errores.append(
            "Entrada inválida: La presión sistólica debe ser estrictamente mayor que la presión diastólica."
        )
    if (sys_bp - dia_bp) < 15:
        errores.append(
            "Entrada inválida: Presión de pulso demasiado estrecha (< 15 mmHg). Verifique la medición."
        )
    if not (40 <= hr <= 200):
        errores.append(
            "Entrada inválida: Frecuencia cardíaca fuera de rango fisiológico viable (40 - 200 lpm)."
        )
    if not (50 <= sys_bp <= 250) or not (30 <= dia_bp <= 160):
        errores.append(
            "Entrada inválida: Valores de presión arterial fuera de límites medibles."
        )
    if not (2.5 <= bs_mmol <= 35.0):
        errores.append(
            "Entrada inválida: Nivel de glucosa fuera de rango fisiológico (2.5 - 35.0 mmol/L)."
        )
    if not (93.0 <= temp_f <= 108.0):
        errores.append(
            "Entrada inválida: Temperatura corporal fuera de rango viable (34.0 °C - 42.2 °C)."
        )

    if age < 12 or age > 55:
        advertencias.append(
            f"Edad ({age} años) fuera del rango obstétrico habitual (12–55 años). "
            "La predicción puede presentar sesgo de extrapolación."
        )
    return errores, advertencias


def cargar_caso(age, sys_bp, dia_bp, bs, temp_c, hr):
    st.session_state.input_age = age
    st.session_state.input_sys = sys_bp
    st.session_state.input_dia = dia_bp
    st.session_state.input_bs_mmol = float(bs)
    st.session_state.input_bs_mgdl = round(float(bs) * 18.0182, 1)
    st.session_state.input_temp_c = float(temp_c)
    st.session_state.input_hr = hr


if "input_age" not in st.session_state:
    cargar_caso(22, 100, 65, 7.8, 36.7, 80)

# Encabezado con ícono Lucide Heart-Pulse
st.markdown(
    f'<div class="lucide-header">{LUCIDE_SVGS["heart_pulse"]}<span>Sistema de Apoyo al Triaje de Riesgo Materno</span></div>',
    unsafe_allow_html=True
)

st.info(
    "**Aviso de Salud Pública:** Herramienta preventiva de priorización comunitaria. "
    "**No constituye diagnóstico ni decisión clínica automática.** Todo caso debe ser validado por personal de salud.",
    icon=":material/info:"
)

pipeline = load_pipeline()
if pipeline is None:
    st.error(
        "No se encontró el modelo entrenado en `models/`. Ejecuta primero `python src/train_final.py`.",
        icon=":material/error:"
    )
    st.stop()

st.markdown(
    f'<div class="lucide-subheader">{LUCIDE_SVGS["sliders"]}<span>Casos de prueba demostrativos</span></div>',
    unsafe_allow_html=True
)
col_c1, col_c2, col_c3, col_c4 = st.columns(4)

if col_c1.button("Caso 1: Bajo Riesgo", icon=":material/check_circle:", use_container_width=True):
    cargar_caso(22, 100, 65, 7.8, 36.7, 80)
    st.rerun()

if col_c2.button("Caso 2: Alto Riesgo", icon=":material/emergency:", use_container_width=True):
    cargar_caso(25, 140, 100, 11.5, 36.7, 86)
    st.rerun()

if col_c3.button("Caso 3: Límite / Incierto", icon=":material/help:", use_container_width=True):
    cargar_caso(35, 120, 80, 6.9, 36.7, 80)
    st.rerun()

if col_c4.button("Caso Adverso", icon=":material/block:", use_container_width=True):
    cargar_caso(28, 80, 120, 7.0, 36.7, 7)
    st.rerun()

st.markdown(
    f'<div class="lucide-subheader">{LUCIDE_SVGS["stethoscope"]}<span>Ingreso de signos vitales y parámetros fisiológicos</span></div>',
    unsafe_allow_html=True
)
c1, c2 = st.columns(2)

with c1:
    age = st.number_input("Edad de la paciente (años)", min_value=1, max_value=100, key="input_age", step=1)
    sys_bp = st.number_input("Presión Arterial Sistólica (mmHg)", min_value=0, max_value=300, key="input_sys", step=1)
    dia_bp = st.number_input("Presión Arterial Diastólica (mmHg)", min_value=0, max_value=300, key="input_dia", step=1)

with c2:
    unidad_bs = st.selectbox("Unidad de Glucosa", ["mmol/L (Estándar del modelo)", "mg/dL (Glucómetro común)"])
    if "mmol/L" in unidad_bs:
        bs_input = st.number_input("Glucosa en sangre (mmol/L)", min_value=0.0, max_value=50.0, key="input_bs_mmol", step=0.1)
        bs_mmol = bs_input
    else:
        bs_mgdl = st.number_input("Glucosa en sangre (mg/dL)", min_value=0.0, max_value=900.0, key="input_bs_mgdl", step=1.0)
        bs_mmol = round(bs_mgdl / 18.0182, 2)
        st.caption(f"Conversión interna aplicada: **{bs_mmol} mmol/L**")

    temp_c = st.number_input("Temperatura Corporal (°C)", min_value=30.0, max_value=45.0, key="input_temp_c", step=0.1)
    temp_f = round((temp_c * 9 / 5) + 32, 2)
    st.caption(f"Equivalencia para el modelo: **{temp_f} °F**")

    hr = st.number_input("Frecuencia Cardíaca (lpm)", min_value=0, max_value=250, key="input_hr", step=1)

if st.button("Evaluar Nivel de Prioridad", icon=":material/analytics:", type="primary", use_container_width=True):
    errores, advertencias = validar_entradas(age, sys_bp, dia_bp, bs_mmol, temp_f, hr)

    if errores:
        st.error(
            "**Se detectaron entradas fuera de los límites fisiológicos permitidos:**",
            icon=":material/gpp_bad:"
        )
        for err in errores:
            st.write(f"- {err}")
        st.stop()

    for adv in advertencias:
        st.warning(adv, icon=":material/warning:")

    registro = pd.DataFrame([{
        "Age": age,
        "SystolicBP": sys_bp,
        "DiastolicBP": dia_bp,
        "BS": bs_mmol,
        "BodyTemp": temp_f,
        "HeartRate": hr
    }])

    pred_clase = pipeline.predict(registro)[0]
    probas = pipeline.predict_proba(registro)[0]
    clases = pipeline.classes_
    mapa_probas = dict(zip(clases, probas))

    confianza_max = float(np.max(probas))
    eps = 1e-12
    entropia_norm = float(-np.sum(probas * np.log(probas + eps)) / np.log(len(clases)))

    etiquetas_es = {
        0: ("Riesgo Bajo (Seguimiento prenatal de rutina)", "success", ":material/verified_user:"),
        1: ("Riesgo Moderado (Priorizar control preventivo)", "warning", ":material/notification_important:"),
        2: ("Riesgo Alto (Derivación prioritaria a valoración obstétrica)", "error", ":material/e911_emergency:"),
        "low risk": ("Riesgo Bajo (Seguimiento prenatal de rutina)", "success", ":material/verified_user:"),
        "mid risk": ("Riesgo Moderado (Priorizar control preventivo)", "warning", ":material/notification_important:"),
        "high risk": ("Riesgo Alto (Derivación prioritaria a valoración obstétrica)", "error", ":material/e911_emergency:")
    }
    nombres_tabla = {
        0: "BAJO RIESGO (LOW RISK)",
        1: "RIESGO MEDIO (MID RISK)",
        2: "ALTO RIESGO (HIGH RISK)",
        "low risk": "BAJO RIESGO (LOW RISK)",
        "mid risk": "RIESGO MEDIO (MID RISK)",
        "high risk": "ALTO RIESGO (HIGH RISK)"
    }

    texto_res, tipo_alerta, icono_alerta = etiquetas_es.get(
        pred_clase, (str(pred_clase), "info", ":material/info:")
    )

    st.divider()
    st.markdown(
        f'<div class="lucide-subheader">{LUCIDE_SVGS["activity"]}<span>Resultado del Tamizaje e Incertidumbre</span></div>',
        unsafe_allow_html=True
    )
    getattr(st, tipo_alerta)(f"**Clasificación sugerida:** {texto_res}", icon=icono_alerta)

    m1, m2 = st.columns(2)
    m1.metric("Confianza de la predicción", f"{confianza_max * 100:.1f}%")
    m2.metric("Índice de incertidumbre (Entropía)", f"{entropia_norm * 100:.1f}%")

    prob_alto = mapa_probas.get(2, mapa_probas.get("high risk", 0.0))
    es_alto = pred_clase in (2, "high risk")

    if confianza_max < 0.65 or entropia_norm >= 0.55 or (not es_alto and prob_alto >= 0.25):
        st.warning(
            "**Alerta de Incertidumbre en Frontera de Decisión:** Las probabilidades entre niveles de riesgo están "
            f"divididas (Confianza máxima: {confianza_max*100:.1f}%, Entropía: {entropia_norm*100:.1f}%, "
            f"Probabilidad de Riesgo Alto: {prob_alto*100:.1f}%). Se recomienda evaluación manual por un profesional.",
            icon=":material/warning:"
        )

    df_probs = pd.DataFrame({
        "Nivel de Riesgo": [nombres_tabla.get(c, str(c).upper()) for c in clases],
        "Probabilidad (%)": [round(p * 100, 2) for p in probas]
    })
    st.dataframe(df_probs, use_container_width=True, hide_index=True)

    st.markdown("##### Distribución Visual de Probabilidades por Nivel de Riesgo")
    st.bar_chart(
        df_probs.set_index("Nivel de Riesgo")["Probabilidad (%)"],
        color="#0284c7"
    )

# Panel desplegable con las gráficas de evaluación en Test
PLOT_PATH = os.path.join("docs", "evaluacion_modelo_final_test.png")
ERRORES_PATH = os.path.join("docs", "analisis_errores_test.csv")

if os.path.exists(PLOT_PATH):
    st.divider()
    with st.expander("Ver Evidencia Experimental en Conjunto de Prueba (Matriz de Confusión, ROC-AUC e Importancia)", icon=":material/bar_chart:"):
        st.image(
            PLOT_PATH,
            caption="Evaluación única del modelo final (Random Forest) sobre el conjunto de prueba reservado (Test = 203 registros).",
            use_container_width=True
        )
        if os.path.exists(ERRORES_PATH):
            df_err = pd.read_csv(ERRORES_PATH)
            st.markdown(f"**Casos mal clasificados en el conjunto de prueba ({len(df_err)} de 203 registros):**")
            st.dataframe(df_err, use_container_width=True, hide_index=True)