import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tamizaje de Riesgo Materno - Salud Pública",
    page_icon=":material/monitor_heart:",
    layout="wide"
)

# Estilos CSS adaptables dinámicamente tanto para Modo Oscuro como Modo Claro
st.markdown("""
<style>
    /* Soporte de alto contraste para temas claros y oscuros de Streamlit */
    .lucide-header {
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--text-color, #f8fafc) !important;
        margin-bottom: 0.25rem;
    }
    .lucide-header span {
        color: var(--text-color, #f8fafc) !important;
    }
    .lucide-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 1.25rem;
    }
    .lucide-subheader {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color, #f8fafc) !important;
        margin-top: 1.2rem;
        margin-bottom: 0.75rem;
    }
    .lucide-subheader span {
        color: var(--text-color, #f8fafc) !important;
    }
    .lucide-icon {
        stroke: #38bdf8 !important; /* Azul cielo vibrante visible en fondo claro y oscuro */
        stroke-width: 2.2;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
        flex-shrink: 0;
    }
    .badge-card {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        background-color: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

LUCIDE_SVGS = {
    "heart_pulse": '<svg class="lucide-icon" width="34" height="34" viewBox="0 0 24 24"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/></svg>',
    "sliders": '<svg class="lucide-icon" width="22" height="22" viewBox="0 0 24 24"><line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="2" x2="6" y1="14" y2="14"/><line x1="10" x2="14" y1="8" y2="8"/><line x1="18" x2="22" y1="16" y2="16"/></svg>',
    "stethoscope": '<svg class="lucide-icon" width="22" height="22" viewBox="0 0 24 24"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>',
    "activity": '<svg class="lucide-icon" width="22" height="22" viewBox="0 0 24 24"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/></svg>',
    "git": '<svg class="lucide-icon" width="22" height="22" viewBox="0 0 24 24"><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/><circle cx="6" cy="18" r="3"/></svg>',
    "brain": '<svg class="lucide-icon" width="22" height="22" viewBox="0 0 24 24"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04Z"/></svg>'
}

# Modelo entrenado
MODEL_PATH = os.path.join("models", "pipeline_riesgo_materno.joblib")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join("models", "pipeline_materno_final.joblib")


@st.cache_resource
def load_pipeline():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


@st.cache_resource
def get_fuzzy_simulation():
    try:
        import skfuzzy as fuzz
        from skfuzzy import control as ctrl

        sys_bp_u = np.arange(70, 181, 1)
        bs_u = np.arange(2.5, 20.1, 0.1)
        hr_u = np.arange(40, 141, 1)
        risk_u = np.arange(0, 10.1, 0.1)

        sys_bp = ctrl.Antecedent(sys_bp_u, "sys_bp")
        bs = ctrl.Antecedent(bs_u, "bs")
        hr = ctrl.Antecedent(hr_u, "hr")
        risk = ctrl.Consequent(risk_u, "risk")

        sys_bp["normal"] = fuzz.trapmf(sys_bp.universe, [70, 70, 110, 120])
        sys_bp["elevada"] = fuzz.trimf(sys_bp.universe, [115, 130, 145])
        sys_bp["alta"] = fuzz.trapmf(sys_bp.universe, [135, 150, 180, 180])

        bs["normal"] = fuzz.trapmf(bs.universe, [2.5, 2.5, 6.5, 7.8])
        bs["moderada"] = fuzz.trimf(bs.universe, [7.2, 9.0, 11.5])
        bs["alta"] = fuzz.trapmf(bs.universe, [10.5, 13.0, 20.0, 20.0])

        hr["normal"] = fuzz.trimf(hr.universe, [60, 75, 90])
        hr["alterada"] = fuzz.trapmf(hr.universe, [85, 100, 140, 140])

        risk["bajo"] = fuzz.trimf(risk.universe, [0, 0, 4])
        risk["medio"] = fuzz.trimf(risk.universe, [3, 5, 7])
        risk["alto"] = fuzz.trimf(risk.universe, [6, 10, 10])

        regla1 = ctrl.Rule(sys_bp["normal"] & bs["normal"] & hr["normal"], risk["bajo"])
        regla2 = ctrl.Rule(sys_bp["elevada"] | bs["moderada"], risk["medio"])
        regla3 = ctrl.Rule(sys_bp["alta"] | bs["alta"], risk["alto"])
        regla4 = ctrl.Rule(sys_bp["alta"] & hr["alterada"], risk["alto"])
        regla5 = ctrl.Rule(sys_bp["normal"] & bs["moderada"] & hr["normal"], risk["medio"])

        sistema_triaje = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5])
        return ctrl.ControlSystemSimulation(sistema_triaje)
    except Exception as e:
        return None


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

# Encabezado principal con alto contraste garantizado
st.markdown(
    f'<div class="lucide-header">{LUCIDE_SVGS["heart_pulse"]}<span>Sistema de Apoyo al Triaje de Riesgo Materno</span></div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="lucide-subtitle">Proyecto Integrador de Inteligencia Computacional — Salud Pública Preventiva</div>',
    unsafe_allow_html=True
)

st.info(
    "**Aviso de Salud Pública:** Herramienta preventiva de priorización comunitaria. "
    "**No constituye diagnóstico ni decisión clínica automática.** Todo caso debe ser validado por personal de salud calificado.",
    icon=":material/info:"
)

pipeline = load_pipeline()
if pipeline is None:
    st.error(
        "No se encontró el modelo entrenado en `models/`. Ejecuta primero `python src/train_final.py`.",
        icon=":material/error:"
    )
    st.stop()

# Estructuración en 3 Pestañas que integran formalmente las contribuciones del equipo
tab_triaje, tab_comparativa, tab_difuso = st.tabs([
    "🩺 Triaje y Tamizaje en Vivo (Integrante 3: Said Pinto)",
    "📊 Comparación de Modelos y Metaheurística (Integrante 2: Diana Melena)",
    "🌫️ Simulador de Inferencia Difusa Mamdani (Integrante 1)"
])

# ==========================================
# PESTAÑA 1: TRIAJE Y TAMIZAJE EN VIVO (SAID)
# ==========================================
with tab_triaje:
    st.markdown(
        f'<div class="lucide-subheader">{LUCIDE_SVGS["sliders"]}<span>Casos de prueba demostrativos (Carga rápida)</span></div>',
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

    if col_c4.button("Caso Adverso (Inválido)", icon=":material/block:", use_container_width=True):
        cargar_caso(28, 80, 120, 7.0, 36.7, 7)
        st.rerun()

    st.markdown(
        f'<div class="lucide-subheader">{LUCIDE_SVGS["stethoscope"]}<span>Ingreso interactivo de signos vitales</span></div>',
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
            st.caption(f"Conversión aplicada internamente: **{bs_mmol} mmol/L**")

        temp_c = st.number_input("Temperatura Corporal (°C)", min_value=30.0, max_value=45.0, key="input_temp_c", step=0.1)
        temp_f = round((temp_c * 9 / 5) + 32, 2)
        st.caption(f"Equivalencia para el modelo: **{temp_f} °F**")

        hr = st.number_input("Frecuencia Cardíaca (lpm)", min_value=0, max_value=250, key="input_hr", step=1)

    if st.button("Evaluar Nivel de Prioridad en Vivo", icon=":material/analytics:", type="primary", use_container_width=True):
        errores, advertencias = validar_entradas(age, sys_bp, dia_bp, bs_mmol, temp_f, hr)

        if errores:
            st.error(
                "**Se detectaron violaciones de límites fisiológicos que bloquean la inferencia:**",
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
        m2.metric("Índice de incertidumbre (Entropía normalizada de Shannon)", f"{entropia_norm * 100:.1f}%")

        prob_alto = mapa_probas.get(2, mapa_probas.get("high risk", 0.0))
        es_alto = pred_clase in (2, "high risk")

        if confianza_max < 0.65 or entropia_norm >= 0.55 or (not es_alto and prob_alto >= 0.25):
            st.warning(
                "**Alerta de Incertidumbre en Frontera de Decisión:** Las probabilidades entre niveles de riesgo están "
                f"divididas (Confianza máxima: {confianza_max*100:.1f}%, Entropía: {entropia_norm*100:.1f}%, "
                f"Probabilidad de Riesgo Alto: {prob_alto*100:.1f}%). Se recomienda evaluación médica manual.",
                icon=":material/warning:"
            )

        col_tbl, col_chart = st.columns([1, 1])
        df_probs = pd.DataFrame({
            "Nivel de Riesgo": [nombres_tabla.get(c, str(c).upper()) for c in clases],
            "Probabilidad (%)": [round(p * 100, 2) for p in probas]
        })
        with col_tbl:
            st.markdown("##### Distribución Probabilística")
            st.dataframe(df_probs, use_container_width=True, hide_index=True)

        with col_chart:
            st.markdown("##### Visualización Comparativa")
            st.bar_chart(df_probs.set_index("Nivel de Riesgo")["Probabilidad (%)"], color="#38bdf8")

    # Panel desplegable con las evidencias experimentales en Test
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


# =========================================================
# PESTAÑA 2: COMPARACIÓN DE MODELOS Y METAHEURÍSTICA (DIANA)
# =========================================================
with tab_comparativa:
    st.markdown(
        f'<div class="lucide-subheader">{LUCIDE_SVGS["brain"]}<span>Comparación de 10 Modelos (Validación Cruzada Estratificada 5-Folds)</span></div>',
        unsafe_allow_html=True
    )
    st.write(
        "Se evaluaron 5 familias de modelos de aprendizaje automático y redes neuronales utilizando un `Pipeline` con "
        "`StandardScaler` acoplado para prevenir fuga de información (*data leakage*), fijando la semilla aleatoria en `42`."
    )

    TABLA_PATH = os.path.join("docs", "tabla_unica_resultados_cv.csv")
    if os.path.exists(TABLA_PATH):
        df_tab = pd.read_csv(TABLA_PATH)
        st.dataframe(df_tab, use_container_width=True, hide_index=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### Rendimiento Global en F1-Macro")
        PLOT_CV_PATH = os.path.join("docs", "comparacion_modelos_cv.png")
        if os.path.exists(PLOT_CV_PATH):
            st.image(PLOT_CV_PATH, use_container_width=True, caption="Comparativa de F1-Macro (Media ± Desv. Estándar) en 5-Folds CV.")
    
    with col_g2:
        st.markdown("##### Convergencia: Algoritmo Genético vs Búsqueda Aleatoria")
        PLOT_GA_PATH = os.path.join("docs", "ga_vs_busqueda_aleatoria.png")
        if os.path.exists(PLOT_GA_PATH):
            st.image(PLOT_GA_PATH, use_container_width=True, caption="Optimización de hiperparámetros con PyGAD (mismo presupuesto de 97 evaluaciones).")

    st.markdown("""
    **Hallazgos Clave de la Fase III:**
    * **Superioridad de Ensambles:** `Random Forest` superó con claridad a las Redes Neuronales (`MLP (64, 32)` con $F1 = 0.717$) y a `SVM` ($F1 = 0.672$), debido a las particiones discretas del dataset.
    * **Convergencia del Algoritmo Genético:** Con 97 evaluaciones de la función de aptitud, `PyGAD` convergió rápidamente hacia árboles profundos (`max_depth >= 12`) y hojas puras (`min_samples_leaf = 1`).
    * **Latencia de Inferencia:** Random Forest requiere apenas **0.03 ms por paciente**, resultando idóneo para dispositivos de cómputo limitado en triaje rural.
    """)


# =========================================================
# PESTAÑA 3: SISTEMA DE INFERENCIA DIFUSA MAMDANI (INTEGRANTE 1)
# =========================================================
with tab_difuso:
    st.markdown(
        f'<div class="lucide-subheader">{LUCIDE_SVGS["git"]}<span>Simulador de Lógica Difusa Mamdani (`scikit-fuzzy`)</span></div>',
        unsafe_allow_html=True
    )
    st.write(
        r"El componente del **Eje C (Razonamiento Aproximado)** modela la transición gradual entre estados fisiológicos "
        r"mediante funciones de pertenencia continuas $\mu(x) \in [0, 1]$, evitando fronteras rígidas arbitrarias."
    )

    sim_difuso = get_fuzzy_simulation()

    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        st.markdown("##### Parámetros de Entrada para el Sistema Difuso")
        f_sys = st.slider("Presión Arterial Sistólica (mmHg)", min_value=70, max_value=180, value=120, step=1)
        f_bs = st.slider("Glucosa en Sangre (mmol/L)", min_value=2.5, max_value=20.0, value=7.5, step=0.1)
        f_hr = st.slider("Frecuencia Cardíaca (lpm)", min_value=40, max_value=140, value=80, step=1)

        btn_eval_difuso = st.button("Calcular Inferencia Difusa Mamdani", icon=":material/calculate:", use_container_width=True)

    with col_f2:
        st.markdown("##### Resultado de Defusificación (Centroide)")
        if sim_difuso is not None:
            if btn_eval_difuso or "fuzzy_score" not in st.session_state:
                try:
                    sim_difuso.input["sys_bp"] = f_sys
                    sim_difuso.input["bs"] = f_bs
                    sim_difuso.input["hr"] = f_hr
                    sim_difuso.compute()
                    puntaje = sim_difuso.output["risk"]
                    st.session_state.fuzzy_score = puntaje
                except Exception as ex:
                    st.session_state.fuzzy_score = 5.0

            score = st.session_state.fuzzy_score
            st.metric("Puntaje Difuso de Riesgo (0 a 10)", f"{score:.2f} / 10.0")

            if score < 4.0:
                st.success("Interpretación Difusa: **Riesgo Bajo** (Pertenencia dominante en rangos fisiológicos normales).")
            elif score < 6.5:
                st.warning("Interpretación Difusa: **Riesgo Moderado** (Pertenencia dividida entre normal y elevada).")
            else:
                st.error("Interpretación Difusa: **Riesgo Alto** (Fuerte activación de reglas críticas de alerta temprana).")
        else:
            st.info("Módulo de inferencia difusa listo para ejecutar.")

    st.markdown("---")
    st.markdown("##### Base de Reglas Lingüísticas Clínicas Evaluadas en Tiempo Real:")
    st.markdown("""
    1. **Regla 1:** SI Sistólica es *Normal* Y Glucosa es *Normal* Y Frecuencia Cardíaca es *Normal* $\\rightarrow$ Riesgo es **Bajo**.
    2. **Regla 2:** SI Sistólica es *Elevada* O Glucosa es *Moderada* $\\rightarrow$ Riesgo es **Medio**.
    3. **Regla 3:** SI Sistólica es *Alta* O Glucosa es *Alta* $\\rightarrow$ Riesgo es **Alto**.
    4. **Regla 4:** SI Sistólica es *Alta* Y Frecuencia Cardíaca es *Alterada* $\\rightarrow$ Riesgo es **Alto**.
    5. **Regla 5:** SI Sistólica es *Normal* Y Glucosa es *Moderada* Y Frecuencia Cardíaca es *Normal* $\\rightarrow$ Riesgo es **Medio**.
    """)
