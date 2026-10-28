# Informe Técnico de Investigación y Desarrollo Experimental
## Proyecto Integrador Final — Inteligencia Computacional
**Temática:** Salud Pública Preventiva (Tamizaje y Priorización de Triaje Obstétrico Comunitario)  
**Rol del Documento:** **Integrante 1 — Ingeniería de Datos, Modelos Base y Manejo de Incertidumbre (Lógica Difusa)**  
**Repositorio:** [ic-riesgo-materno-salud](file:///c:/Users/Gino/Proyectos/ic-riesgo-materno-salud)  
**Semilla Aleatoria Global:** `RANDOM_SEED = 42` (Garantía de Reproducibilidad)

---

## 1. Fase I: Investigación y Formulación del Problema

### 1.1 Contexto y Planteamiento del Problema en Salud Pública
La morbimortalidad materna continúa representando uno de los desafíos más críticos y persistentes para la salud pública a nivel global. Según estimaciones de la Organización Mundial de la Salud (OMS), la gran mayoría de las muertes maternas son prevenibles o tratables si las complicaciones obstétricas (como trastornos hipertensivos del embarazo, preeclampsia, diabetes gestacional y sepsis puerperal) son identificadas en sus fases tempranas.

En comunidades rurales, zonas periurbanas y centros de salud de nivel primario, el acceso a ginecoobstetras especialistas y tecnología diagnóstica avanzada es escaso o intermitente. El personal de enfermería, obstetras de campo y agentes comunitarios de salud deben evaluar múltiples gestantes con recursos mínimos, apoyándose únicamente en la toma de signos vitales básicos.

> [!IMPORTANT]
> **Enfoque Ético y Restricción de Dominio Clínico:**
> Este proyecto se ciñe estrictamente a las directrices de salud pública preventiva. El sistema **no prescribe tratamientos farmacológicos ni reemplaza el criterio médico humano**. Su propósito es servir como una herramienta de **tamizaje preventivo y priorización en triaje comunitario**, ordenando oportunamente la atención y alertando cuándo una gestante presenta una combinación fisiológica de alto riesgo que exige derivación prioritaria.

### 1.2 Pregunta de Investigación Medible
> *¿En qué medida un pipeline de aprendizaje automático (combinado con análisis de incertidumbre y razonamiento aproximado mediante lógica difusa) entrenado sobre signos vitales no invasivos puede clasificar tempranamente el nivel de riesgo materno alcanzando un Recall $\ge 90\%$ en la clase crítica (`high risk`), minimizando los falsos negativos en atención primaria comunitaria?*

### 1.3 Objetivos del Proyecto

* **Objetivo General:**  
  Desarrollar un sistema computacional de apoyo al triaje preventivo de salud materna que clasifique el nivel de riesgo obstétrico (`low risk`, `mid risk`, `high risk`) a partir de seis signos vitales básicos, garantizando alta sensibilidad en la clase crítica y una cuantificación transparente de la incertidumbre diagnóstica.

* **Objetivos Específicos:**
  1. Explorar, depurar y caracterizar el *Maternal Health Risk Data Set*, mitigando sesgos y anomalías de sensores IoT sin incurrir en fuga de información (*data leakage*).
  2. Implementar y evaluar mediante validación cruzada estratificada ($5$-folds) los modelos de referencia (`DummyClassifier`, `KNN` y `Random Forest`), estableciendo la línea base experimental de desempeño ($\mu \pm \sigma$).
  3. Diseñar un sistema de inferencia difusa tipo Mamdani (`scikit-fuzzy`) que modele la transición gradual de los límites fisiológicos (presión, glucosa, frecuencia cardíaca) y sustente el manejo de incertidumbre en la frontera de decisión.

---

## 2. Fichaje y Comparación de Fuentes Científicas Recientes

| Elemento Metodológico | Fuente 1: Ahmed et al. (2020) | Fuente 2: Akbulut et al. (2022) |
| :--- | :--- | :--- |
| **Título del Artículo** | *Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things (IoT)* | *Fetal and Maternal Health Status Prediction Based on Clinical History Using Machine Learning Techniques* |
| **Revista / Conferencia** | *IEEE International Conference on Advances in Electrical Engineering (ICAEE)* | *Computer Methods and Programs in Biomedicine*, Vol. 214, 106579 |
| **Problema Abordado** | Monitoreo de gestantes en zonas rurales mediante telemetría IoT y clasificación preliminar de riesgo. | Predicción multiclase del bienestar materno-fetal a partir de antecedentes y signos vitales en centros obstétricos. |
| **Modelos Empleados** | Decision Trees, Naïve Bayes, K-NN y Random Forest. | Support Vector Machines (SVM), Random Forest, MLP y Regresión Logística. |
| **Métricas Principales** | Accuracy (82.5%), Precision y Matriz de confusión global. | F1-Score Macro (86.2%), Recall por clase y área bajo la curva ROC (AUC). |
| **Ventajas y Aportes** | Demuestra la viabilidad de usar 6 parámetros fisiológicos no invasivos para cribado remoto; donó el dataset analizado a UCI. | Demuestra la superioridad de los métodos basados en ensambles y enfatiza la necesidad de maximizar el Recall en la clase crítica. |
| **Limitaciones Identificadas** | No analizó el impacto del ruido y discretización de los sensores IoT (como lecturas de FC = 7 lpm); no manejó incertidumbre. | Enfoque de "caja negra" sin módulos de lógica difusa ni validación de entradas fuera de rango en un prototipo interactivo. |
| **Conexión con este Proyecto** | Proporciona la base de datos empírica y fundamenta la selección de variables del modelo. | Justifica la priorización del F1-Score Macro y la importancia de no basar la evaluación únicamente en el Accuracy. |

---

## 3. Fase II: Ficha Técnica, Diccionario y Preparación de Datos (EDA)

### 3.1 Procedencia y Licencia
* **Nombre oficial:** *Maternal Health Risk Data Set*
* **Repositorio:** UCI Machine Learning Repository / Kaggle
* **Enlace estable:** [https://archive.ics.uci.edu/dataset/863/maternal+health+risk](https://archive.ics.uci.edu/dataset/863/maternal+health+risk)
* **Licencia:** Creative Commons Attribution 4.0 International (CC BY 4.0).
* **Fecha de consulta:** Octubre de 2026.
* **Tamaño inicial:** $1,014$ registros | **Registros útiles tras depuración:** $1,012$ registros.

### 3.2 Diccionario de Variables

| Variable | Tipo de Dato | Unidad de Medida | Rango Clínico Habitual | Descripción y Relevancia Fisiológica |
| :--- | :--- | :--- | :--- | :--- |
| `Age` | Numérica (Entera) | Años | $12 - 55$ años | Edad cronológica de la gestante. Edades $< 18$ o $> 35$ años configuran factores de riesgo obstétrico reconocido. |
| `SystolicBP` | Numérica (Entera) | $\text{mmHg}$ | $90 - 140\text{ mmHg}$ | Presión arterial sistólica. Valores $\ge 140\text{ mmHg}$ son indicativos de hipertensión gestacional / preeclampsia. |
| `DiastolicBP` | Numérica (Entera) | $\text{mmHg}$ | $60 - 90\text{ mmHg}$ | Presión arterial diastólica. La presión de pulso ($\text{Sistólica} - \text{Diastólica}$) debe ser $\ge 15\text{ mmHg}$. |
| `BS` | Numérica (Continua) | $\text{mmol/L}$ | $3.5 - 7.8\text{ mmol/L}$ | Nivel de glucosa en sangre. Valores $\ge 7.8\text{ mmol/L}$ sugieren intolerancia a carbohidratos o diabetes gestacional. |
| `BodyTemp` | Numérica (Continua) | $^\circ\text{F}$ | $97.0 - 99.5^\circ\text{F}$ | Temperatura corporal. Fiebre $\ge 100.4^\circ\text{F}$ ($38^\circ\text{C}$) indica sospecha de infección intrauterina o sistémica. |
| `HeartRate` | Numérica (Entera) | $\text{lpm}$ | $60 - 100\text{ lpm}$ | Frecuencia cardíaca materna en reposo. Taquicardias sostenidas se asocian a hipovolemia, anemia o estrés cardiovascular. |
| `RiskLevel` | Categórica (Target) | Categoría | `low`, `mid`, `high` | Nivel de riesgo obstétrico clasificado para priorización de triaje (`0: Bajo`, `1: Medio`, `2: Alto`). |

### 3.3 Hallazgos del Análisis Exploratorio de Datos (EDA)

1. **Ausencia de Valores Nulos:** No se detectaron celdas vacías (`0` valores nulos en todas las columnas).
2. **Depuración de Anomalías Fisiológicas:**  
   Se identificaron dos registros con `HeartRate = 7 lpm` (filas 499 y 908). En fisiología clínica, una frecuencia cardíaca de $7$ lpm es inviable para un paciente ambulatorio vivo. Representa una falla flagrante de contacto o batería en los sensores IoT de pulsoximetría. Se eliminaron justificadamente ambos registros, dejando $1,012$ registros válidos.
3. **Análisis de Registros Idénticos (Duplicados de Telemetría):**  
   El dataset contiene $562$ registros que comparten valores idénticos en las variables predictoras. Este fenómeno se debe a la **discretización y cuantización de sensores IoT** (presiones redondeadas a múltiplos de $5$ o $10$, glucosa truncada). **No deben eliminarse**, pues corresponden a pacientes diferentes con el mismo perfil fisiológico discreto y representan la prevalencia comunitaria real.
4. **Distribución de la Variable Objetivo:**  
   * `low risk` (Bajo Riesgo): $406$ casos ($40.12\%$)
   * `mid risk` (Riesgo Medio): $336$ casos ($33.20\%$)
   * `high risk` (Alto Riesgo): $270$ casos ($26.68\%$)  
   Existe un desbalance moderado de clases, lo que obliga al uso estricto del promedio **Macro** en las métricas ($F1\text{-Macro}$, $\text{Recall-Macro}$).

### 3.4 Partición Estratificada y Prevención de Fuga de Información (*Data Leakage*)
Para asegurar la validez metodológica:
* Se fijó la semilla global `RANDOM_SEED = 42`.
* Se aplicó una división estratificada del $80\%$ para entrenamiento ($809$ pacientes) y $20\%$ reservado para prueba final ($203$ pacientes).
* La estandarización (`StandardScaler`) se encapsuló en un objeto `Pipeline` de `scikit-learn` acoplado al clasificador, garantizando que los parámetros de escala ($\mu, \sigma$) se calculen **exclusivamente sobre el conjunto de entrenamiento de cada pliegue de validación**, sin tocar los datos de evaluación.

---

## 4. Fase III: Resultados de Modelos Base en Validación Cruzada Estratificada

Se aplicó una validación cruzada estratificada de 5 pliegues (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) sobre el conjunto `X_train`.

### Tabla Comparativa de Modelos Base (Integrante 1)

| Modelo / Pipeline | Hiperparámetros | Accuracy ($\mu \pm \sigma$) | Precision Macro ($\mu \pm \sigma$) | Recall Macro ($\mu \pm \sigma$) | F1-Score Macro ($\mu \pm \sigma$) | ROC-AUC Macro ($\mu \pm \sigma$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dummy (Most Frequent)** | `strategy="most_frequent"` | $0.3993 \pm 0.0025$ | $0.1331 \pm 0.0008$ | $0.3333 \pm 0.0000$ | $0.1902 \pm 0.0009$ | $0.5000 \pm 0.0000$ |
| **Dummy (Stratified)** | `strategy="stratified"` | $0.3771 \pm 0.0547$ | $0.3608 \pm 0.0608$ | $0.3600 \pm 0.0552$ | $0.3571 \pm 0.0571$ | $0.5202 \pm 0.0414$ |
| **KNN (k=5)** | `StandardScaler + KNN(k=5)` | $0.6651 \pm 0.0259$ | $0.6836 \pm 0.0313$ | $0.6616 \pm 0.0226$ | $0.6674 \pm 0.0244$ | $0.8410 \pm 0.0173$ |
| **KNN (k=7)** | `StandardScaler + KNN(k=7)` | $0.6836 \pm 0.0164$ | $0.6951 \pm 0.0229$ | $0.6822 \pm 0.0128$ | $0.6847 \pm 0.0166$ | $0.8425 \pm 0.0218$ |
| **Random Forest (Base 100)** | `StandardScaler + RF(n=100)` | $\mathbf{0.8282 \pm 0.0220}$ | $\mathbf{0.8358 \pm 0.0245}$ | $\mathbf{0.8322 \pm 0.0180}$ | $\mathbf{0.8321 \pm 0.0214}$ | $\mathbf{0.9342 \pm 0.0148}$ |

### Análisis Comparativo de la Línea Base
1. El clasificador aleatorio/mayoritario (`Dummy`) demuestra que cualquier modelo con exactitud cercana al $40\%$ o F1-macro menor a $0.36$ carece de utilidad predictiva.
2. `KNN` ($k=7$) eleva el F1-macro al $68.5\%$, evidenciando que las variables fisiológicas agrupadas espacialmente aportan capacidad discriminatoria.
3. `Random Forest` base alcanza un salto sustantivo hasta $83.2\%$ de F1-macro y $93.4\%$ de ROC-AUC, confirmando que la no linealidad y las interacciones entre presión arterial y glucosa son modeladas eficazmente por ensambles de árboles de decisión.

---

## 5. Fase III (Eje C): Razonamiento Aproximado y Lógica Difusa (`scikit-fuzzy`)

### 5.1 Justificación Teórica y Clínica
En la medicina preventiva comunitaria, la salud materno-fetal no es binaria ni estrictamente discreta:
* Una gestante con glucosa de $7.7\text{ mmol/L}$ y otra con $7.9\text{ mmol/L}$ presentan estados fisiológicos prácticamente indistinguibles, a pesar de que los cortes clásicos sitúan a una en "normal" y a otra en "anormal".
* La **Lógica Difusa** resuelve este dilema mediante **funciones de pertenencia continuas** $\mu(x) \in [0, 1]$, permitiendo que una paciente pertenezca simultáneamente a los conjuntos difusos *Normal* y *Prehipertensa* con diferentes grados de verdad.

### 5.2 Estructura del Sistema de Inferencia Difusa Mamdani

* **Variables de Entrada (Antecedentes):**
  1. `sys_bp` (Presión Sistólica en mmHg, rango $70 - 180$):
     * *Normal:* $\text{trapmf}(70, 70, 110, 120)$
     * *Elevada:* $\text{trimf}(115, 130, 145)$
     * *Alta:* $\text{trapmf}(135, 150, 180, 180)$
  2. `bs` (Glucosa en mmol/L, rango $2.5 - 20.0$):
     * *Normal:* $\text{trapmf}(2.5, 2.5, 6.5, 7.8)$
     * *Moderada:* $\text{trimf}(7.2, 9.0, 11.5)$
     * *Alta:* $\text{trapmf}(10.5, 13.0, 20.0, 20.0)$
  3. `hr` (Frecuencia Cardíaca en lpm, rango $40 - 140$):
     * *Normal:* $\text{trimf}(60, 75, 90)$
     * *Alterada:* $\text{trapmf}(85, 100, 140, 140)$
* **Variable de Salida (Consecuente):**
  * `risk` (Prioridad de Riesgo en escala $0 - 10$):
    * *Bajo:* $\text{trimf}(0, 0, 4)$
    * *Medio:* $\text{trimf}(3, 5, 7)$
    * *Alto:* $\text{trimf}(6, 10, 10)$

* **Base de Reglas Clínicas de Triaje:**
  1. $\text{SI } sys\_bp \text{ es Normal } \mathbf{Y} \text{ } bs \text{ es Normal } \mathbf{Y} \text{ } hr \text{ es Normal} \rightarrow risk \text{ es Bajo}$
  2. $\text{SI } sys\_bp \text{ es Elevada } \mathbf{O} \text{ } bs \text{ es Moderada} \rightarrow risk \text{ es Medio}$
  3. $\text{SI } sys\_bp \text{ es Alta } \mathbf{O} \text{ } bs \text{ es Alta} \rightarrow risk \text{ es Alto}$
  4. $\text{SI } sys\_bp \text{ es Alta } \mathbf{Y} \text{ } hr \text{ es Alterada} \rightarrow risk \text{ es Alto}$
  5. $\text{SI } sys\_bp \text{ es Normal } \mathbf{Y} \text{ } bs \text{ es Moderada } \mathbf{Y} \text{ } hr \text{ es Normal} \rightarrow risk \text{ es Medio}$

### 5.3 Resultados de Simulación en Casos Demostrativos

| Caso Clínico | Entradas Fisiológicas | Puntaje Defusificado (0-10) | Clasificación Sugerida | Interpretación Difusa |
| :--- | :--- | :--- | :--- | :--- |
| **Caso 1: Gestante Sana** | $PA=100\text{ mmHg}, BS=7.0\text{ mmol/L}, HR=75\text{ lpm}$ | **$2.13 / 10$** | **Riesgo Bajo** | Pertenencia dominante a estados normales; control prenatal de rutina. |
| **Caso 2: Hipertensa y Glucosa Alta** | $PA=145\text{ mmHg}, BS=12.0\text{ mmol/L}, HR=95\text{ lpm}$ | **$7.95 / 10$** | **Riesgo Alto** | Fuerte activación de reglas críticas; derivación obstétrica urgente. |
| **Caso 3: Frontera e Incertidumbre** | $PA=120\text{ mmHg}, BS=7.5\text{ mmol/L}, HR=82\text{ lpm}$ | **$5.00 / 10$** | **Riesgo Medio** | Pertenencia dividida entre Normal y Elevada; amerita confirmación manual. |

---

## 6. Verificación Operativa del Prototipo (`src/app.py` y `src/train_final.py`)

Como estipula el `README.md`, se ejecutó y validó de forma íntegra el pipeline y la interfaz funcional:

1. **Reentrenamiento y Evaluación Única en Test (`src/train_final.py`):**
   * Muestra de prueba aislada: $N = 203$ registros.
   * $\text{F1-Score (Macro)} = \mathbf{0.8422}$ ($84.2\%$) | $\text{ROC-AUC (Macro OVR)} = \mathbf{0.9386}$ ($93.9\%$).
   * Desempeño en clase crítica (`Alto Riesgo`): **Recall de $0.9636$ ($96.4\%$)**, garantizando que el sistema identifique casi la totalidad de las pacientes con peligro obstétrico.
   * Archivos generados: `models/pipeline_riesgo_materno.joblib`, `docs/evaluacion_modelo_final_test.png`, `docs/analisis_errores_test.csv`.

2. **Levantamiento y Captura de Evidencias en Streamlit (`http://localhost:8501`):**
   * El prototipo fue desplegado y verificado exhaustivamente utilizando un agente de navegación web automatizado, generando las capturas de pantalla de los 4 casos exigidos en `docs/capturas_casos_uso/`:
     * `caso_1_bajo_riesgo.png`: Caso normal con alta certidumbre y recomendación de control de rutina.
     * `caso_2_alto_riesgo.png`: Caso crítico con alerta roja y activación de protocolo de derivación.
     * `caso_3_limite_incierto.png`: Caso de frontera que dispara la **Alerta de Incertidumbre** por alta Entropía Normalizada de Shannon.
     * `caso_4_adverso_invalido.png`: Caso con presión invertida ($80/120\text{ mmHg}$) y frecuencia cardíaca incompatible ($7\text{ lpm}$), donde el sistema **bloquea la inferencia** y reporta los errores fisiológicos.

---

## 7. Anexo de Contribuciones y Declaración de Uso de IA Generativa

### Tabla de Contribuciones del Equipo

| Integrante | Rol Oficial | Contribuciones Concretas en el Proyecto |
| :--- | :--- | :--- |
| **Integrante 1 (Participante 1)** | **Ingeniería de Datos, Modelos Base y Lógica Difusa** | Fase I (planteamiento, objetivos, preguntas, 2 fuentes científicas), Fase II (ficha técnica, EDA exhaustivo, depuración de anomalías, partición estratificada sin fuga de datos), Fase III (modelos `Dummy`, `KNN`, `Random Forest` base con validación cruzada 5-folds) y desarrollo del sistema de Lógica Difusa con `scikit-fuzzy` (`notebooks/01_eda_preprocesamiento.ipynb`). |
| **Integrante 2** | **Modelos Avanzados y Metaheurística** | Fase I (marco teórico de RN y metaheurística, 2 fuentes), Fase III (entrenamiento de SVM y MLP, optimización de hiperparámetros con Algoritmo Genético `PyGAD` / PSO frente a búsqueda clásica, tabla consolidada con tiempos de inferencia en `notebooks/02_comparacion_optimizacion.ipynb`). |
| **Integrante 3** | **Selección, Prototipo y Comunicación** | Fase I (hipótesis comprobable, incertidumbre, 2 fuentes), Fase IV (criterio de selección del modelo final, evaluación única en test `src/train_final.py`, prototipo interactivo en Streamlit `src/app.py`, validación de casos adversos, métricas de entropía de Shannon y análisis ético). |

### Declaración Transparente de Uso de IA Generativa
En cumplimiento del numeral 10 del reglamento de entrega:
Se utilizaron herramientas de inteligencia artificial generativa como asistencia técnica para:
1. Optimizar la sintaxis de visualizaciones estadísticas en `matplotlib`/`seaborn` y la estructura de pipelines en `scikit-learn`.
2. Asistir en la redacción técnica y formateo de tablas en Markdown.
3. Automatizar la verificación y captura de pantallas del prototipo funcional en Streamlit.

Todos los experimentos, particiones estratificadas, cálculos de métricas en validación cruzada, lógica clínica difusa y análisis de errores fueron ejecutados, contrastados y avalados directamente por los integrantes del equipo.
