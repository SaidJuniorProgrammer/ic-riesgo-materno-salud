import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score
)

# 1. Semilla aleatoria fija para reproducibilidad
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# 2. Cargar el dataset desde la carpeta data/
DATA_PATH = os.path.join("data", "Maternal Health Risk Data Set.csv")
df = pd.read_csv(DATA_PATH)

# Filtrar los 2 errores de sensor (HeartRate = 7 lpm)
df = df[df["HeartRate"] >= 40].copy()

# Codificación ordenada de la variable objetivo
mapa_riesgo = {"low risk": 0, "mid risk": 1, "high risk": 2}
df["Target"] = df["RiskLevel"].map(mapa_riesgo)

X = df[["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]]
y = df["Target"]

# 3. Partición Entrenamiento / Prueba ANTES de ajustar transformaciones
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=RANDOM_SEED
)

# 4. Pipeline sin fuga de información (Data Leakage)
pipeline_final = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=2,
        class_weight="balanced",
        random_state=RANDOM_SEED
    ))
])

# 5. Entrenamiento con datos de entrenamiento
pipeline_final.fit(X_train, y_train)

# 6. Evaluación ÚNICA en el conjunto de prueba reservado
y_pred = pipeline_final.predict(X_test)
y_proba = pipeline_final.predict_proba(X_test)

f1_macro = f1_score(y_test, y_pred, average="macro")
roc_auc = roc_auc_score(y_test, y_proba, multi_class="ovr", average="macro")

print("=== RESULTADOS EN EL CONJUNTO DE PRUEBA (EVALUACIÓN ÚNICA) ===")
print(f"F1-Score (Macro): {f1_macro:.4f}")
print(f"ROC-AUC (Macro OVR): {roc_auc:.4f}\n")
print("Matriz de Confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte por Clase (0: Bajo, 1: Medio, 2: Alto):")
print(classification_report(
    y_test, y_pred, target_names=["Bajo Riesgo", "Riesgo Medio", "Alto Riesgo"]
))

# 7. Guardar el pipeline entrenado en la carpeta models/
os.makedirs("models", exist_ok=True)
MODEL_PATH = os.path.join("models", "pipeline_riesgo_materno.joblib")
joblib.dump(pipeline_final, MODEL_PATH)
print(f"\nPipeline guardado exitosamente en: {MODEL_PATH}")