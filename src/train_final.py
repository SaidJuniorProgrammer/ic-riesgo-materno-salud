import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
    roc_curve,
    auc
)

# 1. Fijar semilla aleatoria para reproducibilidad (Sección 5)
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# 2. Cargar y depurar el dataset
DATA_PATH = os.path.join("data", "Maternal Health Risk Data Set.csv")
df = pd.read_csv(DATA_PATH)
df = df[df["HeartRate"] >= 40].copy()

mapa_riesgo = {"low risk": 0, "mid risk": 1, "high risk": 2}
mapa_inverso = {0: "Bajo Riesgo", 1: "Riesgo Medio", 2: "Alto Riesgo"}
df["Target"] = df["RiskLevel"].map(mapa_riesgo)

X = df[["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]]
y = df["Target"]

# 3. Partición Entrenamiento / Prueba ANTES de ajustar transformaciones
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=RANDOM_SEED
)

# 4. Hiperparámetros (usa los del Integrante 2 si exportó JSON, o los óptimos por defecto)
params_rf = {
    "n_estimators": 150,
    "max_depth": 12,
    "min_samples_split": 2,
    "class_weight": "balanced",
    "random_state": RANDOM_SEED
}
PARAMS_PATH = os.path.join("models", "mejores_hiperparametros.json")
if os.path.exists(PARAMS_PATH):
    with open(PARAMS_PATH, "r", encoding="utf-8") as f:
        params_rf.update(json.load(f))
    print(f"Hiperparámetros cargados desde {PARAMS_PATH}: {params_rf}")

# 5. Pipeline sin fuga de información (Data Leakage)
pipeline_final = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(**params_rf))
])

# 6. Reentrenamiento con entrenamiento y evaluación ÚNICA en prueba
pipeline_final.fit(X_train, y_train)
y_pred = pipeline_final.predict(X_test)
y_proba = pipeline_final.predict_proba(X_test)

f1_macro = f1_score(y_test, y_pred, average="macro")
roc_auc = roc_auc_score(y_test, y_proba, multi_class="ovr", average="macro")
nombres_clases = ["Bajo Riesgo", "Riesgo Medio", "Alto Riesgo"]

print("=== RESULTADOS EN EL CONJUNTO DE PRUEBA (EVALUACIÓN ÚNICA) ===")
print(f"F1-Score (Macro): {f1_macro:.4f}")
print(f"ROC-AUC (Macro OVR): {roc_auc:.4f}\n")
print("Matriz de Confusión:")
cm = confusion_matrix(y_test, y_pred)
print(cm)
print("\nReporte por Clase:")
print(classification_report(y_test, y_pred, target_names=nombres_clases))

# 7. Exportar el pipeline entrenado
os.makedirs("models", exist_ok=True)
MODEL_PATH = os.path.join("models", "pipeline_riesgo_materno.joblib")
joblib.dump(pipeline_final, MODEL_PATH)
print(f"Pipeline guardado exitosamente en: {MODEL_PATH}")

# 8. Generar y guardar gráficas de evaluación en docs/ (Sección 5 y Fase V)
os.makedirs("docs", exist_ok=True)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Gráfica A: Matriz de Confusión
sns.heatmap(
    cm, annot=True, fmt="d", cmap="Blues",
    xticklabels=nombres_clases, yticklabels=nombres_clases, ax=axes[0]
)
axes[0].set_title("Matriz de Confusión (Conjunto Test)")
axes[0].set_xlabel("Predicción del Modelo")
axes[0].set_ylabel("Clase Real")

# Gráfica B: Curvas ROC Multiclase
y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
colores = ["#2ca02c", "#ff7f0e", "#d62728"]
for i, (nombre, color) in enumerate(zip(nombres_clases, colores)):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
    roc_auc_val = auc(fpr, tpr)
    axes[1].plot(fpr, tpr, color=color, lw=2, label=f"{nombre} (AUC = {roc_auc_val:.3f})")

axes[1].plot([0, 1], [0, 1], "k--", lw=1)
axes[1].set_title("Curvas ROC Multiclase (One-vs-Rest)")
axes[1].set_xlabel("Tasa de Falsos Positivos (FPR)")
axes[1].set_ylabel("Tasa de Verdaderos Positivos (Recall)")
axes[1].legend(loc="lower right")
axes[1].grid(alpha=0.3)

# Gráfica C: Importancia de Variables
importancias = pipeline_final.named_steps["classifier"].feature_importances_
indices = np.argsort(importancias)
axes[2].barh(X.columns[indices], importancias[indices], color="#1f77b4")
axes[2].set_title("Importancia de Variables en el Modelo Final")
axes[2].set_xlabel("Importancia Relativa (Gini)")

plt.tight_layout()
PLOT_PATH = os.path.join("docs", "evaluacion_modelo_final_test.png")
plt.savefig(PLOT_PATH, dpi=150)
plt.close()
print(f"Gráfica de evaluación guardada en: {PLOT_PATH}")

# 9. Exportar tabla de errores en Test para análisis ético y crítico (Fase V)
df_errores = X_test.copy()
df_errores["Clase_Real"] = y_test.map(mapa_inverso)
df_errores["Prediccion"] = pd.Series(y_pred, index=X_test.index).map(mapa_inverso)
df_errores["Confianza_Max"] = np.round(np.max(y_proba, axis=1), 4)
df_errores = df_errores[df_errores["Clase_Real"] != df_errores["Prediccion"]]

ERRORES_PATH = os.path.join("docs", "analisis_errores_test.csv")
df_errores.to_csv(ERRORES_PATH, index=False)
print(f"Tabla de errores ({len(df_errores)} casos) exportada en: {ERRORES_PATH}")