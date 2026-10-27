import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tamizaje de Riesgo Materno - Salud Pública",
    page_icon="🩺",
    layout="centered"
)

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

st.title("🩺 Sistema de Apoyo al Triaje de Riesgo Materno")
st.info(
    "**Aviso de Salud Pública:** Herramienta preventiva de priorización comunitaria. "
    "**No constituye diagnóstico ni decisión clínica automática.** Todo caso debe ser validado por personal de salud."
)

pipeline = load_pipeline()
if pipeline is None:
    st.error("No se encontró el modelo entrenado en `models/`. Ejecuta primero `python src/train_final.py`.")
    st.stop()

st.subheader("Casos de prueba demostrativos")
col_c1, col_c2, col_c3, col_c4 = st.columns(4)

if col_c1.button("Caso 1: Bajo Riesgo", use_container_width=True):
    cargar_caso(22, 100, 65, 7.8, 36.7, 80)
    st.rerun()

if col_c2.button("Caso 2: Alto Riesgo", use_container_width=True):
    cargar_caso(25, 140, 100, 11.5, 36.7, 86)
    st.rerun()

if col_c3.button("Caso 3: Límite / Incierto", use_container_width=True):
    cargar_caso(35, 120, 80, 6.9, 36.7, 80)
    st.rerun()

if col_c4.button("Caso Adverso (Inválido)", use_container_width=True):
    cargar_caso(28, 80, 120, 7.0, 36.7, 7)
    st.rerun()

st.subheader("Ingreso de signos vitales")
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

if st.button("Evaluar Nivel de Prioridad", type="primary", use_container_width=True):
    errores, advertencias = validar_entradas(age, sys_bp, dia_bp, bs_mmol, temp_f, hr)

    if errores:
        st.error("🚫 **Se detectaron entradas fuera de los límites fisiológicos permitidos:**")
        for err in errores:
            st.write(f"- {err}")
        st.stop()

    for adv in advertencias:
        st.warning(adv)

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

    # Compatible con clases numéricas (0, 1, 2) y de texto ('low risk', 'mid risk', 'high risk')
    etiquetas_es = {
        0: ("Riesgo Bajo (Seguimiento prenatal de rutina)", "success"),
        1: ("Riesgo Moderado (Priorizar control preventivo)", "warning"),
        2: ("Riesgo Alto (Derivación prioritaria a valoración obstétrica)", "error"),
        "low risk": ("Riesgo Bajo (Seguimiento prenatal de rutina)", "success"),
        "mid risk": ("Riesgo Moderado (Priorizar control preventivo)", "warning"),
        "high risk": ("Riesgo Alto (Derivación prioritaria a valoración obstétrica)", "error")
    }
    nombres_tabla = {
        0: "BAJO RIESGO (LOW RISK)",
        1: "RIESGO MEDIO (MID RISK)",
        2: "ALTO RIESGO (HIGH RISK)",
        "low risk": "BAJO RIESGO (LOW RISK)",
        "mid risk": "RIESGO MEDIO (MID RISK)",
        "high risk": "ALTO RIESGO (HIGH RISK)"
    }

    texto_res, tipo_alerta = etiquetas_es.get(pred_clase, (str(pred_clase), "info"))

    st.divider()
    st.subheader("Resultado del Tamizaje")
    getattr(st, tipo_alerta)(f"**Clasificación sugerida:** {texto_res}")

    m1, m2 = st.columns(2)
    m1.metric("Confianza de la predicción", f"{confianza_max * 100:.1f}%")
    m2.metric("Índice de incertidumbre (Entropía)", f"{entropia_norm * 100:.1f}%")

    prob_alto = mapa_probas.get(2, mapa_probas.get("high risk", 0.0))
    es_alto = pred_clase in (2, "high risk")

    if confianza_max < 0.65 or entropia_norm >= 0.55 or (not es_alto and prob_alto >= 0.25):
        st.warning(
            "⚠️ **Alerta de Incertidumbre en Frontera de Decisión:** Las probabilidades entre niveles de riesgo están "
            f"divididas (Confianza máxima: {confianza_max*100:.1f}%, Entropía: {entropia_norm*100:.1f}%, "
            f"Probabilidad de Riesgo Alto: {prob_alto*100:.1f}%). Se recomienda evaluación manual por un profesional."
        )

    df_probs = pd.DataFrame({
        "Nivel de Riesgo": [nombres_tabla.get(c, str(c).upper()) for c in clases],
        "Probabilidad (%)": [round(p * 100, 2) for p in probas]
    })
    st.dataframe(df_probs, use_container_width=True, hide_index=True)