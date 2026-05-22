import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

def run_extract():
    df = pd.read_csv(
        r"C:\Users\HP\Downloads\archive (23)\candidate_job_role_dataset.csv",
        encoding="utf-8"
    ).dropna()

    target_column = "job_role"
    df = df.drop(columns=["candidate_id"], errors="ignore")

    counts = df[target_column].value_counts()
    df = df[df[target_column].isin(counts[counts >= 2].index)]

    for col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model_xgb = XGBClassifier(
        n_estimators=300, max_depth=10, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        random_state=42, eval_metric="mlogloss"
    )
    model_xgb.fit(X_train, y_train)

    text_columns = ["skills", "qualification", "experience_level"]
    cv_texts = df[text_columns].astype(str).agg(" ".join, axis=1)

    os.makedirs(r"C:\Users\HP\Desktop\pfe\data", exist_ok=True)
    cv_texts.to_csv(r"C:\Users\HP\Desktop\pfe\data\cv_texts.csv", index=False, header=["text"])

    return model_xgb
