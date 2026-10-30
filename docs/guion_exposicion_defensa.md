# 🎙️ Guion Oficial de Exposición — Proyecto Integrador de Inteligencia Computacional
## "Sistema de Apoyo al Triaje Preventivo de Riesgo Materno"
**Universidad Estatal Península de Santa Elena (UPSE) — Carrera de Ingeniería en Software 7/1**  
**Docente:** Ing. Daniel Iván Quirumbay Yagual  
**Tiempo Límite de Exposición:** 10:00 minutos exactos (más 5 minutos de preguntas)  
**Presentadores:**
- **Gino Maximiliano Bermúdez Santos (Integrante 1):** Diapositivas 1 a 4 (~3:20 min)
- **Diana Lucía Melena Santander (Integrante 2):** Diapositivas 5 a 7 (~3:00 min)
- **Said Fausto Pinto Tamayo (Integrante 3):** Diapositivas 8 a 10 (~3:40 min, incluye demo)

---

## ⏱️ Cronograma de Tiempos por Diapositiva

| Diapositiva | Título / Tema Principal | Presentador | Tiempo Sugerido | Tiempo Acumulado |
| :---: | :--- | :---: | :---: | :---: |
| **1** | Portada, contextualización del proyecto y roles del equipo | **Gino** | 0:40 min | 0:40 |
| **2** | El problema de salud pública, 6 signos vitales y pregunta | **Gino** | 0:50 min | 1:30 |
| **3** | Calidad de datos, depuración, desbalance y prevención de fugas | **Gino** | 1:00 min | 2:30 |
| **4** | Eje C: Lógica Difusa Mamdani, funciones de pertenencia y reglas | **Gino** | 1:00 min | 3:30 |
| **5** | Eje A: Comparativa de 4 modelos vs. Baseline y lógica de decisión | **Diana** | 1:00 min | 4:30 |
| **6** | Eje B: Algoritmo Genético, los 5 pasos y cromosoma de 6 genes | **Diana** | 1:00 min | 5:30 |
| **7** | Validación rigurosa del AG: 15 particiones y empate técnico | **Diana** | 1:00 min | 6:30 |
| **8** | Modelo final Random Forest: matriz de confusión y test único | **Said** | 1:00 min | 7:30 |
| **9** | Prototipo Streamlit: validación fisiológica, entropía y 4 casos | **Said** | 1:30 min | 9:00 |
| **10** | Análisis ético, errores en salud pública, síntesis de los 3 ejes | **Said / Todos** | 1:00 min | 10:00 |

---

## 🗣️ GUION DETALLADO PASO A PASO

---

### Diapositiva 1: Portada con el equipo y sus roles
* **Presenta:** Gino Maximiliano Bermúdez Santos  
* **Tiempo asignado:** 0:40 min  
* **Qué se muestra en pantalla:** Título del proyecto *"Maternal Health Risk Triage"*, logo de la UPSE, nombres y fotos/roles de los tres integrantes (Gino, Diana, Said).

> **[INICIA GINO]**  
> *"Muy buenos días estimado docente, Ing. Daniel Quirumbay, y compañeros. Somos el equipo conformado por Diana Melena, Said Pinto y mi persona, Gino Bermúdez. Hoy presentamos nuestro Proyecto Integrador de Inteligencia Computacional titulado **Maternal Health Risk Triage: Sistema de Apoyo al Triaje Preventivo de Salud Materna**.*  
>  
> *Para abordar este reto con máximo rigor, distribuimos el trabajo en tres roles técnicos complementarios:*  
> * *Mi rol como **Integrante 1** abarca la ingeniería de datos, los modelos base y el modelado de incertidumbre con Lógica Difusa.*  
> * *Nuestra compañera **Diana (Integrante 2)** lideró el entrenamiento de modelos avanzados como SVM y Redes Neuronales, junto a la optimización metaheurística con Algoritmos Genéticos.*  
> * *Y nuestro compañero **Said (Integrante 3)** estuvo a cargo de la evaluación final en prueba, el prototipo interactivo en Streamlit y el análisis ético y de errores.*  
>  
> *Comencemos viendo el problema que motivó nuestra investigación."*

---

### Diapositiva 2: El problema: 6 signos vitales entran y sale el nivel de riesgo; pregunta de investigación
* **Presenta:** Gino Maximiliano Bermúdez Santos  
* **Tiempo asignado:** 0:50 min  
* **Qué se muestra en pantalla:** Diagrama de caja negra del sistema (6 signos vitales entran: Edad, Presión Sistólica, Presión Diastólica, Glucosa, Temperatura, Frecuencia Cardíaca; sale una de 3 categorías: Bajo, Medio o Alto Riesgo), la pregunta de investigación y los usuarios beneficiarios.

> **[CONTINÚA GINO]**  
> *"La morbimortalidad materna por complicaciones como preeclampsia o diabetes gestacional es prevenible si se detecta a tiempo. Sin embargo, en centros de atención primaria y áreas rurales no hay especialistas ginecoobstetras ni laboratorios complejos las 24 horas.*  
>  
> *El personal de enfermería y promotores comunitarios únicamente cuentan con equipos básicos de signos vitales. Nuestro sistema se concibe como una herramienta de **triaje preventivo**: recibe 6 parámetros fisiológicos no invasivos y sugiere un nivel de prioridad: **Riesgo Bajo** para control de rutina, **Riesgo Medio** para seguimiento cercano, o **Riesgo Alto** para derivación prioritaria.*  
>  
> *Queremos enfatizar un principio ético de salud pública: **este sistema no emite un diagnóstico médico automático ni prescribe tratamientos**. Su función es ordenar la prioridad de atención para que el profesional de salud decida oportunamente.*  
>  
> *De aquí formulamos nuestra pregunta de investigación: ¿En qué medida el aprendizaje automático, la optimización evolutiva y el manejo de incertidumbre permiten clasificar el nivel de riesgo materno a partir de signos vitales básicos en atención primaria?"*

---

### Diapositiva 3: Los datos: gráfico de clases, limpieza y cómo evitaron la fuga de datos
* **Presenta:** Gino Maximiliano Bermúdez Santos  
* **Tiempo asignado:** 1:00 min  
* **Qué se muestra en pantalla:** Gráfico de distribución de clases (Bajo: 39.9%, Medio: 33.2%, Alto: 26.9%), tarjetas estadísticas (0 nulos, 2 anomalías eliminadas, 561 duplicados conservados) y el diagrama de 4 pasos para evitar Data Leakage (split 80/20, Pipeline, CV estratificada y test único).

> **[CONTINÚA GINO]**  
> *"Trabajamos con el conjunto de datos público de salud materna de la Universidad de California en Irvine (UCI), con 1,014 registros originales.*  
>  
> *Durante el Análisis Exploratorio identificamos tres aspectos clave:*  
> 1. *Primero: **Cero valores ausentes**.*  
> 2. *Segundo: Detectamos dos registros con **Frecuencia Cardíaca de 7 latidos por minuto**. En obstetricia, 7 lpm es biológicamente inviable en una paciente ambulatoria viva; correspondía a un fallo de contacto del sensor IoT. Los eliminamos justificadamente, quedando **1,012 registros útiles**.*  
> 3. *Tercero: Hallamos 561 perfiles con valores idénticos. **No los borramos** porque los sensores comunitarios redondean los signos vitales; borrarlos significaría eliminar más del 50% de la cohorte y distorsionar la prevalencia real.*  
>  
> *Como observan en el gráfico, las clases están desbalanceadas: 40% bajo, 33% medio y 27% alto. Por eso **no usamos únicamente Accuracy**, sino **F1-Score Macro** y **Recall de la clase crítica**.*  
>  
> *Para garantizar cero fuga de información (Data Leakage), realizamos una partición estratificada 80/20 antes de cualquier cálculo: 809 casos para entrenamiento y 203 reservados para prueba final. Además, encapsulamos el escalador `StandardScaler` dentro de un objeto `Pipeline` de scikit-learn con semilla fija 42, asegurando que ningún pliegue vea datos del conjunto de prueba."*

---

### Diapositiva 4: Lógica difusa: gráfico de las funciones de glucosa, reglas y puntajes
* **Presenta:** Gino Maximiliano Bermúdez Santos  
* **Tiempo asignado:** 1:00 min  
* **Qué se muestra en pantalla:** Gráfico de funciones de pertenencia de Glucosa (Normal, Moderada, Alta con la línea punteada en 7.5 mmol/L), el esquema del sistema Mamdani (3 entradas, 5 reglas lingüísticas) y la tabla con los 3 casos clínicos defusificados.

> **[CONTINÚA GINO]**  
> *"Esto nos conecta directamente con el **Eje C: Razonamiento Aproximado y Manejo de Incertidumbre**.*  
>  
> *En medicina, la frontera entre la salud y el riesgo no es una pared vertical. Una paciente con glucosa de 7.5 mmol/L no pasa bruscamente de sana a enferma. Por eso diseñamos en `scikit-fuzzy` un sistema de inferencia difusa tipo Mamdani.*  
>  
> *Como aprecian en el gráfico, un valor de 7.5 mmol/L pertenece un 40% al conjunto 'Normal' y un 60% al conjunto 'Moderado' simultáneamente. No la encasillamos a la fuerza.*  
>  
> *El sistema procesa tres entradas: presión sistólica, glucosa y frecuencia cardíaca; y aplica cinco reglas redactadas en lenguaje clínico natural, por ejemplo: 'Si la presión es alta O la glucosa es alta, el riesgo es Alto'.*  
>  
> *El resultado se defusifica por centroide en una escala continua de 0 a 10. Por ejemplo, una gestante con presión 100 y glucosa 7.0 obtiene un puntaje de 1.48 (Riesgo Bajo); mientras que una paciente con presión 145 y glucosa 12.0 alcanza 8.56, clasificándose inmediatamente como Alto Riesgo.*  
>  
> *Ahora doy el paso a mi compañera Diana, quien explicará el modelado de Machine Learning y la optimización evolutiva."*

---

### Diapositiva 5: Comparación de modelos: barras de F1 y cómo decide cada modelo
* **Presenta:** Diana Lucía Melena Santander  
* **Tiempo asignado:** 1:00 min  
* **Qué se muestra en pantalla:** Gráfico de barras de F1-Score Macro en validación cruzada (Dummy: 0.190, KNN: 0.668, SVM: 0.672, MLP: 0.717, Random Forest: 0.832), recuadro explicativo de cómo decide cada algoritmo y justificación de por qué gana Random Forest.

> **[INICIA DIANA]**  
> *"Muchas gracias, Gino. Entrando al **Eje A: Aprendizaje Automático y Redes Neuronales**, evaluamos cuatro algoritmos supervisados frente a una línea base ingenua (`DummyClassifier`), utilizando los mismos 809 registros de entrenamiento bajo validación cruzada estratificada de 5 particiones con el Pipeline de Gino.*  
>  
> *Cada modelo toma decisiones bajo un paradigma computacional distinto:*  
> * *`KNN` clasifica buscando a las 5 gestantes más parecidas en el espacio multidimensional.*  
> * *`SVM` con kernel RBF traza el hiperplano con el margen más amplio entre las clases.*  
> * *La `Red Neuronal MLP` aprende mediante capas ocultas y propagación hacia atrás del error (Backpropagation).*  
> * *Y `Random Forest` combina múltiples árboles de decisión mediante votación por mayoría.*  
>  
> *Los resultados en F1-Macro son contundentes: la línea base apenas obtuvo 0.190, demostrando que todos los modelos aprendieron patrones reales. `KNN` logró 0.668, `SVM` 0.672 y la Red Neuronal `MLP` alcanzó 0.717.*  
>  
> *Sin embargo, el ganador indiscutible fue **Random Forest con 0.832**, superando por más de 11 puntos a la red neuronal. La explicación clínica es clara: en obstetricia, las decisiones se rigen por umbrales jerárquicos (por ejemplo, si la glucosa supera 7.8 mmol/L o la presión sistólica supera 140 mmHg), y las divisiones ortogonales de los árboles de decisión modelan este comportamiento mucho mejor que las funciones sigmoideas o hiperplanos."*

---

### Diapositiva 6: Algoritmo genético: los 5 pasos y el cromosoma de 6 genes
* **Presenta:** Diana Lucía Melena Santander  
* **Tiempo asignado:** 1:00 min  
* **Qué se muestra en pantalla:** Diagrama de ciclo de los 5 pasos del AG (Población 12, Fitness F1-Macro CV, Selección por Torneo k=3, Cruzamiento en 2 puntos, Mutación 20% + Elitismo 2 mejores) y anatomía del cromosoma de 6 genes del Random Forest.

> **[CONTINÚA DIANA]**  
> *"Pasamos al **Eje B: Búsqueda y Optimización Metaheurística**.*  
>  
> *Para optimizar los hiperparámetros del Random Forest, implementamos un **Algoritmo Genético** utilizando la librería `PyGAD`. Representamos cada configuración como un individuo o cromosoma compuesto por **6 genes**: número de árboles (de 50 a 600), profundidad máxima, muestras mínimas para dividir, muestras mínimas en hoja, criterio de atributos máximos y ponderación de clases.*  
>  
> *El espacio total de búsqueda comprendía **6,720 combinaciones posibles**. El algoritmo opera en un ciclo evolutivo de 5 fases:*  
> 1. *Genera una **población inicial** de 12 configuraciones aleatorias.*  
> 2. *Evalúa la **función de aptitud (Fitness)** como el F1-Macro obtenido en validación cruzada de 5 pliegues.*  
> 3. *Aplica **selección por torneo** de tamaño 3, donde el individuo más apto se convierte en progenitor.*  
> 4. *Aplica **cruzamiento** combinando genes de dos padres.*  
> 5. *Introduce una tasa de **mutación del 20% por gen** para mantener diversidad genética y escapar de óptimos locales.*  
>  
> *Evolucionamos la población durante 12 generaciones con **elitismo**, preservando siempre intactos a los 2 mejores individuos. En total exploramos solo 97 configuraciones.*  
>  
> *Para que la comparación fuera científicamente rigurosa, construimos un competidor directo: una **Búsqueda Aleatoria (Random Search)** con el mismo presupuesto exacto de 97 evaluaciones. Veamos qué ocurrió en la siguiente diapositiva."*

---

### Diapositiva 7: Resultado del algoritmo genético: empate técnico al validar con 15 particiones nuevas
* **Presenta:** Diana Lucía Melena Santander  
* **Tiempo asignado:** 1:00 min  
* **Qué se muestra en pantalla:** Gráficos comparativos de barras (F1 aparente durante la búsqueda vs. F1 validado en 15 particiones independientes: 0.824 inicial, 0.821 GA, 0.827 Random Search) y la explicación del empate técnico y sesgo del optimizador.

> **[CONTINÚA DIANA]**  
> *"Al finalizar la búsqueda inicial en los mismos 5 pliegues, el Algoritmo Genético reportó un F1 aparente de 0.838 y la Búsqueda Aleatoria 0.842, frente al 0.832 del modelo inicial. Parecía que la metaheurística había ganado.*  
>  
> *Sin embargo, en ciencia de datos existe el fenómeno de **sobreajuste al proceso de optimización (Selection Bias)**: el mejor individuo suele verse beneficiado por la partición específica en la que compitió.*  
>  
> *Para comprobar si la mejora era real, sometimos las tres configuraciones a una **segunda validación rigurosa**: 3 repeticiones de validación cruzada estratificada con semillas distintas, evaluando 15 pliegues totalmente nuevos.*  
>  
> *El resultado fue esclarecedor: el modelo inicial obtuvo 0.824, el Algoritmo Genético 0.821 y la Búsqueda Aleatoria 0.827. Las diferencias son de apenas 0.005, mientras que la desviación estándar natural entre pliegues es de 0.025. **Estadísticamente es un empate técnico**.*  
>  
> *Nuestra hipótesis planteaba que la metaheurística igualaría o mejoraría el desempeño: **igualó el desempeño, pero no lo superó significativamente**.*  
>  
> *Siguiendo el principio de la Navaja de Ockham, seleccionamos el modelo más simple y eficiente: **150 árboles con profundidad 12**, que consume 3 veces menos memoria que el individuo de 500 árboles del AG y ofrece el mejor Recall en alto riesgo (0.885).*  
>  
> *Ahora cedo la palabra a Said, quien presentará la evaluación final en prueba y el prototipo funcional."*

---

### Diapositiva 8: Modelo final: matriz de confusión y métricas en prueba
* **Presenta:** Said Fausto Pinto Tamayo  
* **Tiempo asignado:** 1:00 min  
* **Qué se muestra en pantalla:** Matriz de confusión sobre el conjunto de prueba reservado (Test = 203 registros), tarjetas con métricas finales (Recall Alto Riesgo: 0.96, F1-Macro: 0.85, Accuracy: 0.84, ROC-AUC: 0.943) e importancia relativa de variables (Glucosa 37%, Presión Sistólica 19%).

> **[INICIA SAID]**  
> *"Muchas gracias, Diana. Llegamos a la **Fase IV: Selección y Evaluación Única del Modelo Final**.*  
>  
> *Seleccionamos el Pipeline de Random Forest (150 árboles, profundidad 12, balanceo de pesos) por su estabilidad, bajo costo computacional y alta interpretabilidad. Lo reentrenamos con los 809 registros de entrenamiento y realizamos **una única evaluación sobre los 203 registros de prueba que jamás habían sido tocados**.*  
>  
> *Los resultados en prueba son sobresalientes:*  
> * *Alcanzamos un **F1-Score Macro de 0.85**, una exactitud del **84%** y un **ROC-AUC de 0.943**.*  
> * *Y la métrica más crítica para la salud pública: el **Recall en Alto Riesgo fue de 0.96 (96%)**.*  
>  
> *Miren la matriz de confusión: de 55 gestantes en situación de Alto Riesgo, **el modelo detectó correctamente a 53**, fallando únicamente en 2 casos. Los errores restantes se concentraron entre Bajo y Medio Riesgo, lo cual es clínicamente mucho menos peligroso.*  
>  
> *Nuestros criterios de éxito iniciales exigían un F1 superior a 0.75 y un Recall en alto riesgo superior a 0.80: **ambos fueron superados holgadamente**.*  
>  
> *Además, el análisis de importancia de variables reveló que la **Glucosa en sangre (37%)** y la **Presión Sistólica (19%)** concentran más del 56% del poder predictivo, coincidiendo con la literatura médica sobre preeclampsia y diabetes gestacional."*

---

### Diapositiva 9: Prototipo: flujo de la app, reglas de alerta y los 4 casos de prueba
* **Presenta:** Said Fausto Pinto Tamayo  
* **Tiempo asignado:** 1:30 min (incluye demostración rápida del prototipo en vivo)  
* **Qué se muestra en pantalla:** Flujo operativo de la app en 5 pasos, las 3 condiciones que disparan la Alerta de Incertidumbre, la tabla resumen de los 4 casos de prueba demostrativos y cambio a la ventana de Streamlit.

> **[CONTINÚA SAID]**  
> *"Para cumplir con el requisito indispensable de aprobación, integramos este pipeline en un prototipo funcional desarrollado en **Streamlit**.*  
>  
> *El flujo del prototipo opera en 5 etapas:*  
> 1. *Permite el ingreso de los 6 signos vitales (con soporte para °C o °F, y mmol/L o mg/dL).*  
> 2. *Ejecuta una **validación fisiológica estricta**: si un usuario ingresa una presión sistólica menor que la diastólica o una frecuencia cardíaca imposible, el sistema bloquea la predicción.*  
> 3. *El pipeline predice la clase de riesgo y las probabilidades.*  
> 4. *Calcula el nivel de confianza máxima y la **Entropía Normalizada de Shannon**.*  
> 5. *Y aquí está la gran innovación del **Eje C**: el sistema activa una **Alerta de Incertidumbre** si la confianza es menor al 65%, si la entropía supera el 55%, o si la probabilidad residual de Alto Riesgo supera el 25% en una predicción baja.*  
>  
> *Diseñamos 4 botones de prueba rápida en la interfaz:*  
> * *El **Caso 1 (Bajo Riesgo)**: paciente sana de 22 años, presión 100/65; predice Bajo Riesgo con 86% de certeza.*  
> * *El **Caso 2 (Alto Riesgo)**: paciente hipertensa de 140/100 y glucosa alta; predice Alto Riesgo con 99% de certidumbre y alerta roja.*  
> * *El **Caso 3 (Límite / Incierto)**: paciente en frontera de 120/80; activa la alerta amarilla porque las probabilidades se dividen entre las tres clases.*  
> * *Y el **Caso 4 (Adverso / Inválido)**: paciente con presión invertida de 80/120 y pulso de 7 lpm; el sistema **bloquea la inferencia** y reporta los errores.*  
>  
> *(Acción en vivo: Said muestra en 20 segundos la app en pantalla cargando un caso y demostrando la alerta en vivo).*  
> *La aplicación cuenta además con tres pestañas que integran los aportes de todo el equipo: Triaje en vivo, Comparativa con el Algoritmo Genético de Diana, y el Simulador Difuso de Gino."*

---

### Diapositiva 10: Errores, ética y conclusiones de los 3 ejes; preguntas
* **Presenta:** Said Fausto Pinto Tamayo (con cierre compartido de Diana y Gino)  
* **Tiempo asignado:** 1:00 min  
* **Qué se muestra en pantalla:** Análisis de falsos positivos y negativos, limitaciones y sesgos del dataset (datos de Bangladés), postulado ético 'Human in the Loop', síntesis de los 3 ejes y enlace al repositorio GitHub.

> **[CONTINÚA SAID]**  
> *"Para cerrar, analizamos las implicaciones éticas y los riesgos en salud pública:*  
> * *El peor error posible es un **Falso Negativo en Alto Riesgo**: enviar a casa a una madre con preeclampsia. Nuestro modelo minimizó este riesgo al alcanzar 96% de sensibilidad, errando solo 2 casos.*  
> * *Un **Falso Positivo**, en cambio, significa una valoración médica preventiva adicional, lo cual es seguro y preferible.*  
> * *Como limitación, el dataset proviene de comunidades rurales de Bangladés y no incluye semanas de gestación. Por tanto, antes de un despliegue real en Ecuador, se requiere calibración con datos locales.*  
> * *Nuestro principio rector es **'Human in the Loop'**: la inteligencia artificial asiste en el triaje, pero el criterio clínico humano siempre toma la decisión.*  
>  
> *Sintetizamos el proyecto conectando los tres ejes de la asignatura:*  
> * *En el **Eje A**, demostramos la superioridad de Random Forest con 0.85 de F1.*  
> * *En el **Eje B**, aplicamos un Algoritmo Genético reportando con honestidad científica un empate técnico.*  
> * *Y en el **Eje C**, modelamos la incertidumbre combinando Lógica Difusa y Entropía de Shannon.*  
>  
> *Todo nuestro código, pipeline serializado y documentación están disponibles en nuestro repositorio público de GitHub.*  
>  
> *Agradecemos su atención y quedamos atentos a sus preguntas."*

---

## 🛡️ BANCO DE PREGUNTAS Y RESPUESTAS PARA LA DEFENSA (5 Minutos)

### Pregunta 1 (Para Gino — Datos y Lógica Difusa):
**Profesor:** *"¿Por qué eliminaron los registros con frecuencia cardíaca de 7 lpm pero decidieron mantener los 561 duplicados?"*  
> **Respuesta sugerida de Gino:**  
> *"Excelente pregunta, profesor. Los dos registros con 7 lpm representaban una imposibilidad fisiológica para una paciente ambulatoria viva; mantenerlos distorsionaría los límites del clasificador al introducir ruido instrumental de un sensor descalibrado. En cambio, los 561 registros con perfiles idénticos no son duplicados erróneos por error de copiado, sino el resultado de la discretización natural de los sensores de telemetría IoT en puestos de salud comunitarios (donde la presión se anota redondeada en múltiplos de 5 o 10 y la glucosa en decimales fijos). Si hubiéramos eliminado esos 561 registros, habríamos borrado al 55% de la población del estudio, alterando gravemente la prevalencia epidemiológica real de las enfermedades en la comunidad."*

### Pregunta 2 (Para Diana — Modelos y Algoritmo Genético):
**Profesor:** *"¿Por qué el Algoritmo Genético empató técnicamente con el modelo inicial y con Random Search en lugar de superarlo ampliamente?"*  
> **Respuesta sugerida de Diana:**  
> *"Profesor, esto se debe a dos razones fundamentales: primero, Random Forest es un algoritmo muy robusto cuyos hiperparámetros por defecto o base ya se ubican muy cerca de la meseta óptima de convergencia en este conjunto de datos. Segundo, durante la búsqueda inicial el AG parecía superior (0.838 frente a 0.832), pero al realizar una validación cruzada repetida con 15 pliegues nuevos e independientes descubrimos que esa pequeña ganancia era un artefacto del sesgo del optimizador (Selection Bias). Al promediar sobre 15 pliegues nuevos, la variabilidad natural entre particiones (±0.025) superó ampliamente la diferencia entre algoritmos (0.005). Por rigor científico, en lugar de forzar un resultado artificial, reportamos con honestidad el empate técnico y seleccionamos el modelo más liviano de 150 árboles."*

### Pregunta 3 (Para Said — Prototipo e Incertidumbre):
**Profesor:** *"¿Cómo protege su prototipo interactivo a una paciente cuando el modelo no está seguro de su predicción?"*  
> **Respuesta sugerida de Said:**  
> *"Profesor, esa es precisamente la función del componente de incertidumbre del Eje C en nuestra aplicación. Un modelo tradicional siempre devuelve una clase con la probabilidad más alta, aunque sea por una diferencia mínima (por ejemplo 37% vs 35%). En nuestro prototipo, implementamos la **Entropía Normalizada de Shannon**. Si la confianza de la clase ganadora es menor al 65%, o si la entropía supera el 55%, la app despliega automáticamente una alerta amarilla visible indicando que la gestante se encuentra en una **frontera de decisión difusa**. Además, incluimos una regla de riesgo residual: si el modelo sugiere 'Riesgo Bajo' pero la probabilidad de 'Alto Riesgo' supera el 25%, se emite una advertencia preventiva obligando a una reevaluación manual por personal médico."*
