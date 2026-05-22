import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

def run_posts():
    try:
        df = pd.read_csv(
            r"C:\Users\HP\Downloads\archive (30)\home\sdf\marketing_sample_for_naukri_com-jobs__20190701_20190830__30k_data.csv",
            encoding="utf-8"
        )
    except FileNotFoundError:
        print("Fichier introuvable.")
        sys.exit(1)

    df = df.dropna()

    target_column = "Role"
    df = df.drop(columns=["Uniq ID"], errors="ignore")

    counts = df[target_column].value_counts()
    df = df[df[target_column].isin(counts[counts >= 2].index)]

    label_encoders = {}
    for col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=300, max_depth=10, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        random_state=42, eval_metric="mlogloss"
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nAccuracy :", accuracy_score(y_test, y_pred))
    print("\nMatrice de confusion :\n", confusion_matrix(y_test, y_pred))
    print("\nRapport de classification :\n", classification_report(y_test, y_pred, zero_division=0))

    model_lgb = LGBMClassifier(
        n_estimators=300, max_depth=10, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        random_state=42
    )
    model_lgb.fit(X_train, y_train)

    y_pred_lgb = model_lgb.predict(X_test)
    print("\n=== LightGBM ===")
    print("Accuracy :", accuracy_score(y_test, y_pred_lgb))
    print("Matrice de confusion :\n", confusion_matrix(y_test, y_pred_lgb))
    print("Rapport de classification :\n", classification_report(y_test, y_pred_lgb, zero_division=0))

    text_columns = ["Job Title", "Job Salary", "Job Experience Required", "Key Skills",
                    "Role Category", "Location", "Functional Area", "Industry"]
    job_texts = df[text_columns].astype(str).agg(" ".join, axis=1)

    job_texts.to_csv(r"C:\Users\HP\Desktop\pfe\data\job_texts.csv", index=False, header=["text"])

    return model, model_lgb
