# 🩺 Sistema de Apoyo al Triaje Preventivo de Salud Materna
**Proyecto Integrador Final — Inteligencia Computacional**

## 1. Propósito del Proyecto
Este proyecto implementa una solución de Inteligencia Computacional orientada a la **salud pública preventiva (sin decisiones clínicas automáticas)** para clasificar el nivel de riesgo obstétrico (`low risk`, `mid risk`, `high risk`) a partir de seis signos vitales básicos. Su objetivo es apoyar la priorización de atención temprana en centros de salud primarios y comunitarios mediante un prototipo interactivo.

### Relación con los 3 Ejes de Inteligencia Computacional
1. **Aprendizaje Automático y Redes Neuronales:** Entrenamiento y evaluación comparativa con validación cruzada estratificada de `DummyClassifier` (línea base), `KNN`, `SVM`, `Random Forest` y Perceptrón Multicapa (`MLP`).
2. **Búsqueda y Optimización Metaheurística:** Optimización de hiperparámetros mediante Algoritmos Evolutivos (`PyGAD`) / PSO comparada frente a búsqueda convencional.
3. **Razonamiento Aproximado y Manejo de Incertidumbre:** Modelado con lógica difusa (`scikit-fuzzy`) y cuantificación de incertidumbre en el prototipo mediante **Entropía Normalizada de Shannon**, umbrales de confianza ($< 65\%$) y alerta de riesgo residual en la clase crítica (`high risk` $\ge 25\%$).

---

## 2. Estructura del Repositorio

```text
ic-riesgo-materno-salud/
│
├── data/
│   └── Maternal Health Risk Data Set.csv        # Dataset original (UCI / Kaggle)
├── docs/
│   └── capturas_casos_uso/                      # Evidencias de pruebas del prototipo
├── models/
│   └── pipeline_riesgo_materno.joblib           # Pipeline final entrenado y exportado
├── notebooks/
│   ├── 01_eda_preprocesamiento.ipynb            # Fase II: EDA, limpieza y partición
│   └── 02_comparacion_optimizacion.ipynb        # Fase III: 4 modelos, CV y metaheurística
├── src/
│   ├── train_final.py                           # Fase IV: Entrenamiento y evaluación única en Test
│   └── app.py                                   # Fase IV: Interfaz funcional en Streamlit
├── requirements.txt                             # Dependencias con versiones exactas
└── README.md                                    # Documentación técnica e instrucciones
```

---

## 3. Conjunto de Datos y Diccionario de Variables
* **Nombre:** Maternal Health Risk Data Set
* **Fuente Original:** UCI Machine Learning Repository / Kaggle (Donado por Maruf Ahmed et al.)
* **Enlace Estable:** https://archive.ics.uci.edu/dataset/863/maternal+health+risk
* **Licencia:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Fecha de Consulta:** Octubre de 2026
* **Tamaño:** 1,014 registros originales (`1,012` registros útiles tras depurar 2 errores de captura con `HeartRate = 7 lpm`).

| Variable | Tipo | Unidad en Modelo | Soporte en Interfaz (`app.py`) | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `Age` | Numérica (Entera) | Años (10 – 70) | Años (Advertencia fuera de 12–55) | Edad registrada de la paciente. |
| `SystolicBP` | Numérica (Entera) | mmHg (70 – 160) | mmHg (50 – 250) | Presión arterial sistólica (debe ser $>$ diastólica). |
| `DiastolicBP` | Numérica (Entera) | mmHg (49 – 100) | mmHg (30 – 160) | Presión arterial diastólica (diferencia de pulso $\ge 15$ mmHg). |
| `BS` | Numérica (Continua) | mmol/L (6.0 – 19.0) | **mmol/L** o conversión desde **mg/dL** | Nivel de glucosa en sangre. |
| `BodyTemp` | Numérica (Continua) | °F (98.0 – 103.0) | Ingreso en **°C** con conversión a **°F** | Temperatura corporal de la paciente. |
| `HeartRate` | Numérica (Entera) | lpm (60 – 90) | lpm (40 – 200 viables) | Frecuencia cardíaca en reposo en latidos por minuto. |
| `RiskLevel` | Categórica (Objetivo) | `0: Bajo`, `1: Medio`, `2: Alto` | `low risk`, `mid risk`, `high risk` | Nivel de prioridad para triaje preventivo. |

### Limitaciones del Dataset
* Presenta perfiles repetidos producto de lecturas discretizadas en sensores IoT comunitarios.
* Contiene dos registros anómalos con `HeartRate = 7 lpm` (filas 499 y 908) atribuibles a error de sensor, los cuales se filtran antes de la partición.
* No incluye semanas de gestación ni antecedentes obstétricos previos, por lo que su uso es exclusivamente de tamizaje preventivo primario.

---

## 4. Reproducibilidad: Entorno de Hardware y Software
* **Semilla Aleatoria Fija:** `RANDOM_SEED = 42` aplicada en la partición estratificada (`80% train / 20% test`), validación cruzada (`StratifiedKFold`) e inicialización de algoritmos.
* **Sistema Operativo y Lenguaje:** Windows 64-bit (`win_amd64`) | **Python 3.13**
* **Versiones Exactas de Librerías (`requirements.txt`):**
  * `pandas==2.2.3`
  * `numpy==2.1.3`
  * `scikit-learn==1.5.2`
  * `joblib==1.4.2`
  * `streamlit==1.40.0`
  * `matplotlib==3.9.2`
  * `seaborn==0.13.2`
  * `pygad==3.3.1`
  * `scikit-fuzzy==0.5.0`
* **Prevención de Fuga de Información (Data Leakage):** El escalado estándar (`StandardScaler`) y el clasificador final están encapsulados en un único objeto `Pipeline` ajustado exclusivamente sobre `X_train`.

---

## 5. Instrucciones de Instalación y Ejecución

### Paso 1: Clonar el repositorio e instalar dependencias
```bash
git clone <URL_DEL_REPOSITORIO>
cd ic-riesgo-materno-salud
pip install -r requirements.txt
```

### Paso 2: Entrenar y exportar el Pipeline final (Evaluación única en Test)
```bash
python src/train_final.py
```
Este script procesa `data/Maternal Health Risk Data Set.csv`, evalúa el modelo seleccionado una sola vez sobre el conjunto de prueba reservado (`203` registros) y exporta el archivo `models/pipeline_riesgo_materno.joblib`.

**Resumen de Resultados en el Conjunto de Prueba (`Test = 203 registros`):**
* **Exactitud (Accuracy):** `0.84` (`84.0%`)
* **F1-Score (Macro):** `0.85` (`85.0%`)
* **Recall (Macro):** `0.85` (`85.0%`)
* **Desempeño en Clase Crítica (`Alto Riesgo`):** Precisión = `0.88`, **Recall = `0.96` (`96.0%`)**, F1-Score = `0.92`.

### Paso 3: Ejecutar el prototipo interactivo en Streamlit
```bash
streamlit run src/app.py
```
*(Si es la primera vez que ejecutas Streamlit y aparece en consola `Email:`, presiona `Enter` dejando el campo en blanco para abrir automáticamente `http://localhost:8501` en el navegador).*

---

## 6. Casos de Prueba Incluidos en la Interfaz (`src/app.py`)
El prototipo incorpora 4 botones de carga rápida en la parte superior para verificar en vivo los casos exigidos:
1. **Caso 1 (Bajo Riesgo):** Paciente de 22 años, PA `100/65` mmHg, Glucosa `7.8` mmol/L, Temp `36.7` °C, FC `80` lpm $\rightarrow$ Predicción de **Riesgo Bajo** con alta certidumbre.
2. **Caso 2 (Alto Riesgo):** Paciente de 25 años, PA `140/100` mmHg, Glucosa `11.5` mmol/L, Temp `36.7` °C, FC `86` lpm $\rightarrow$ Predicción de **Riesgo Alto** (alerta roja de derivación prioritaria).
3. **Caso 3 (Límite / Incierto):** Paciente de 35 años, PA `120/80` mmHg, Glucosa `6.9` mmol/L, Temp `36.7` °C, FC `80` lpm $\rightarrow$ Activa la **Alerta de Incertidumbre en Frontera de Decisión** por alta entropía de Shannon y probabilidades divididas entre clases.
4. **Caso Adverso (Inválido):** Paciente con PA incoherente (`80/120` mmHg, sistólica menor que diastólica) y FC `7` lpm $\rightarrow$ **Bloquea la inferencia** y reporta las violaciones de límites fisiológicos.

---

## 7. Anexo de Contribuciones y Declaración de Uso de IA Generativa

| Integrante | Rol y Contribuciones Específicas |
| :--- | :--- |
| **Integrante 1** | Investigación Fase I (planteamiento, objetivos, 2 fuentes), EDA (`01_eda_preprocesamiento.ipynb`), depuración de anomalías, partición sin fuga de información, modelos `Dummy`, `KNN`, `Random Forest` y módulo de lógica difusa. |
| **Integrante 2** | Investigación Fase I (fundamentos de RN y algoritmos evolutivos, 2 fuentes), entrenamiento de `SVM` y `MLP` (`02_comparacion_optimizacion.ipynb`), optimización de hiperparámetros con metaheurística y tabla comparativa única. |
| **Integrante 3 (Said Fausto Pinto Tamayo)** | Investigación Fase I (hipótesis comprobable, manejo de incertidumbre, 2 fuentes), selección y evaluación única del modelo final en prueba (`src/train_final.py`), desarrollo del prototipo en Streamlit (`src/app.py`), validación de casos de uso y análisis ético/errores. |

**Declaración de Uso de IA Generativa:** Se utilizaron herramientas de IA generativa como asistencia en la estructuración de código en `scikit-learn` y `Streamlit`, formato de documentación y revisión de estilo técnico. Todo el código, pruebas experimentales, validación de métricas e interpretación clínica preventiva fueron ejecutados y verificados por los integrantes del equipo.