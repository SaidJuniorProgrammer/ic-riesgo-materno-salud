# Guía de Planificación y División de Trabajo
**Asignatura:** Inteligencia Computacional — Proyecto Integrador Final  
**Temática asignada:** Salud Pública (Sin decisiones clínicas automáticas)  
**Modalidad:** Equipo de 3 integrantes | **Duración:** 3 semanas | **Puntaje total:** 25 puntos

---

## 1. Requisitos Clave del Proyecto (Resumen de Reglas)

1. **Enfoque en Salud Pública:** El sistema **no debe** plantearse como un diagnóstico médico definitivo ni prescribir tratamientos automáticos. Debe enfocarse en **tamizaje preventivo, alerta temprana, priorización de triaje comunitario o estimación de niveles de riesgo poblacional**.
2. **Los 3 Ejes de Inteligencia Computacional (Obligatorios en el informe):**
   * **Eje A:** Aprendizaje automático y redes neuronales (KNN, SVM, Random Forest, MLP y línea base `Dummy`).
   * **Eje B:** Búsqueda y optimización de hiperparámetros mediante algoritmos evolutivos (Algoritmo Genético) u otra metaheurística (ej. PSO).
   * **Eje C:** Razonamiento aproximado o manejo de incertidumbre mediante **lógica difusa** o **análisis de confianza**.
3. **Condición Indispensable de Aprobación:** Entregar un prototipo funcional (Streamlit, Gradio, Flask o consola) que cargue el pipeline final entrenado y procese al menos un registro nuevo en vivo durante la defensa.

---

## 2. Propuestas de Datasets (Públicos y con $>500$ registros)

### Opción A: Maternal Health Risk Data Set (Recomendada)
* **Fuente:** UCI Machine Learning Repository / Kaggle (Licencia CC BY 4.0).
* **Enlace de referencia:** `https://archive.ics.uci.edu/dataset/863/maternal+health+risk`
* **Tamaño:** $1,014$ registros y $7$ variables (supera el mínimo de $500$ registros útiles).
* **Variables de entrada ($X$):**
  * `Age`: Edad de la paciente (años).
  * `SystolicBP`: Presión arterial sistólica ($\text{mmHg}$).
  * `DiastolicBP`: Presión arterial diastólica ($\text{mmHg}$).
  * `BS`: Nivel de glucosa en sangre ($\text{mmol/L}$).
  * `BodyTemp`: Temperatura corporal ($^\circ\text{F}$ o convertible a $^\circ\text{C}$).
  * `HeartRate`: Frecuencia cardíaca en reposo ($\text{latidos/min}$).
* **Variable objetivo ($y$):** `RiskLevel` — Clasificación multiclase del nivel de riesgo materno (`low risk`, `mid risk`, `high risk`).
* **Justificación para el proyecto:**
  * **Utilidad en salud pública:** Herramienta de triaje comunitario para centros de atención primaria o zonas rurales que permite priorizar qué gestantes requieren valoración preventiva urgente.
  * **Conexión con los 3 ejes:** Sus variables fisiológicas continuas son ideales para construir funciones de pertenencia en **Lógica Difusa** (ej. presión "normal", "elevada", "crítica") y compararlas o integrarlas con el análisis de incertidumbre de los $4$ modelos de Machine Learning.

---

## 3. División del Trabajo para 3 Integrantes

Para asegurar una carga equitativa donde todos comprendan el flujo completo (requisito de la defensa oral) y puedan completar el **Anexo de Contribuciones**, el trabajo se divide en $3$ roles técnicos complementarios:

### Integrante 1: Ingeniería de Datos, Modelos Base y Manejo de Incertidumbre (Lógica Difusa)
* **Fase I (Investigación):**
  * Redactar el planteamiento del problema, objetivo general, objetivos específicos, pregunta de investigación e impacto en salud pública.
  * Buscar y fichar **$2$ artículos científicos** recientes sobre aprendizaje automático aplicado al problema de salud elegido.
* **Fase II (Datos y Preparación - 5 pts):**
  * Documentar origen, licencia, fecha de consulta, diccionario de variables y limitaciones del dataset.
  * Realizar el Análisis Exploratorio de Datos (EDA): valores faltantes, duplicados, distribución de clases y análisis de sesgos.
  * Crear la partición `train/test` fijando una semilla aleatoria (`random_state=42`) y construir el objeto `Pipeline` base en `scikit-learn` (imputación, codificación y escalado) para que todo el equipo lo utilice sin fuga de información.
* **Fase III (Modelos Base y Eje C):**
  * Entrenar y validar con validación cruzada el modelo base (`DummyClassifier`/`DummyRegressor`), **KNN** y **Random Forest**.
  * Desarrollar e investigar el componente del **Eje C**: sistema de inferencia difusa (`scikit-fuzzy`) o análisis de umbrales de confianza/incertidumbre en las predicciones.

### Integrante 2: Modelos Avanzados (SVM y Redes Neuronales) y Optimización Metaheurística
* **Fase I (Investigación):**
  * Buscar y fichar **$2$ artículos científicos** recientes enfocados en redes neuronales y optimización de hiperparámetros en salud.
  * Redactar el marco teórico del **Eje A** (fundamentos matemáticos de Redes Neuronales Multicapa) y **Eje B** (Algoritmos Genéticos / PSO).
* **Fase III (Modelos Avanzados y Eje B - 8 pts):**
  * Utilizando el `Pipeline` del Integrante 1, entrenar y evaluar mediante validación cruzada la **Máquina de Vectores de Soporte (SVM)** y la **Red Neuronal Multicapa (MLP)**.
  * Implementar la **optimización de hiperparámetros con Algoritmo Genético (GA) o Enjambre de Partículas (PSO)** sobre el modelo con mejor proyección, y compararla formalmente contra una búsqueda tradicional (`GridSearchCV` / `RandomizedSearchCV`) o configuración inicial.
  * Consolidar la **Tabla Única de Resultados**: hiperparámetros, media y desviación estándar en validación cruzada ($\text{Precisión}$, $\text{Recall}$, $\text{F1-macro}$, $\text{ROC-AUC}$ o $\text{MAE}$, $\text{RMSE}$, $R^2$) y tiempos de entrenamiento/inferencia.

### Integrante 3: Selección Final, Prototipo Funcional y Comunicación Científica
* **Fase I (Investigación):**
  * Buscar y fichar **$2$ artículos científicos** sobre interpretabilidad, incertidumbre o sistemas de apoyo a la decisión en salud.
  * Redactar la hipótesis comprobable (criterio de éxito) y el marco teórico del **Eje C** (Lógica Difusa o manejo de incertidumbre).
* **Fase IV (Selección y Prototipo Operativo - 5 pts):**
  * Redactar la justificación técnica para elegir el **modelo final** (balanceando métricas, estabilidad, costo computacional e interpretabilidad) y explicar por qué se descartan los demás.
  * Reentrenar el `Pipeline` ganador con todo el conjunto de entrenamiento (`X_train`, `y_train`), ejecutar la **evaluación única** sobre el conjunto de prueba (`X_test`, `y_test`), generar la matriz de confusión final y exportar el archivo serializado (`.joblib` o `.pkl`).
  * Construir la **interfaz interactiva** (en **Streamlit** o **Gradio**) que cargue el pipeline guardado, valide entradas fuera de rango o inválidas, y muestre la predicción junto con su nivel de confianza o interpretación.
  * Diseñar y documentar los **$3$ casos de prueba** (caso normal/bajo riesgo, caso de alto riesgo y **caso límite o adverso**).
* **Fase V (Repositorio y Defensa - 5 pts):**
  * Estructurar el repositorio final (`requirements.txt`, `README.md` con instrucciones de instalación y ejecución, scripts organizados).
  * Redactar el análisis de errores, implicaciones éticas en salud pública, sesgos y mejoras futuras.


## 4. Plantilla de Control de Entregables (Checklist de 25 Puntos)

- [ ] **Informe Técnico (8–12 páginas, sin contar anexos):**
  - [ ] Portada, Resumen, Planteamiento del Problema y Antecedentes ($6$ referencias académicas).
  - [ ] Explicación teórica y conexión práctica con los $3$ ejes: Redes Neuronales, Optimización Evolutiva/Metaheurística y Lógica Difusa/Incertidumbre.
  - [ ] Hipótesis comprobable formulada antes de ver resultados.
  - [ ] Diccionario de variables, enlace al dataset, EDA y diagrama/explicación del `Pipeline` sin fuga de datos.
  - [ ] Tabla comparativa única (`Dummy`, `KNN`, `SVM`, `Random Forest`, `MLP` + modelo optimizado con GA/PSO) con media y desviación estándar en validación cruzada.
  - [ ] Resultados en el conjunto de prueba (`test`) del modelo seleccionado y justificación de descarte de los demás.
  - [ ] Capturas de los $3$ casos de uso en el prototipo (incluyendo caso límite/adverso y validación de entradas erróneas).
  - [ ] Discusión de errores (falsos positivos/falsos negativos y su impacto en salud pública), ética, limitaciones y conclusiones.
- [ ] **Anexos Obligatorios:**
  - [ ] Tabla de contribuciones individuales firmada/avalada por los $3$ integrantes.
  - [ ] Declaración transparente del uso de herramientas de IA generativa.
- [ ] **Repositorio / Carpeta Comprimida:**
  - [ ] Código ejecutable (`.ipynb` / `.py`) con semilla aleatoria fija.
  - [ ] Archivo `requirements.txt` con versiones de librerías y descripción de hardware/software.
  - [ ] Archivo `README.md` con instrucciones paso a paso para instalar y correr el prototipo.
  - [ ] Pipeline entrenado exportado (`.pkl` o `.joblib`) y script de la interfaz gráfica.
- [ ] **Presentación (Máx. 10 diapositivas):**
  - [ ] Incluye tabla comparativa de modelos y demostración en vivo del prototipo.