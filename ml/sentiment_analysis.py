import os
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import io

load_dotenv()

# --- Load data from Blob Storage ---
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(
    container="customerinsight",
    blob="data/reviews_sample.csv"
)
blob_data = blob_client.download_blob().readall()
df = pd.read_csv(io.BytesIO(blob_data))
print(f"Loaded {len(df)} reviews from Blob Storage")

# --- Label sentiment from rating ---
def label_sentiment(rating):
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

df["sentiment"] = df["rating"].apply(label_sentiment)
print(f"Sentiment distribution:\n{df['sentiment'].value_counts()}")

# Set MLflow tracking to a path without spaces
os.makedirs("C:/Users/xande/mlflow_runs", exist_ok=True)
mlflow.set_tracking_uri("file:///C:/Users/xande/mlflow_runs")

# --- MLflow experiment tracking ---
mlflow.set_experiment("customer-sentiment-analysis")

with mlflow.start_run(run_name="tfidf-logistic-regression"):

    # Log parameters
    mlflow.log_param("model_type", "LogisticRegression")
    mlflow.log_param("vectorizer", "TF-IDF")
    mlflow.log_param("dataset_size", len(df))
    mlflow.log_param("max_features", 500)

    # --- Build pipeline ---
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=500, stop_words="english")),
        ("clf", LogisticRegression(max_iter=200, random_state=42))
    ])

    # --- Train/test split ---
    X = df["review_text"]
    y = df["sentiment"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # --- Train ---
    pipeline.fit(X_train, y_train)

    # --- Evaluate ---
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    # --- Log metrics ---
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("train_size", len(X_train))
    mlflow.log_metric("test_size", len(X_test))

    # Log per-class metrics where available
    for label in ["positive", "neutral", "negative"]:
        if label in report:
            mlflow.log_metric(f"f1_{label}", report[label]["f1-score"])

    # --- Category-level sentiment summary ---
    df["predicted_sentiment"] = pipeline.predict(df["review_text"])
    category_summary = df.groupby("category")["predicted_sentiment"].value_counts().unstack(fill_value=0)
    print(f"\nCategory sentiment summary:\n{category_summary}")
    print(f"\nAccuracy: {accuracy:.2f}")

    # --- Log model ---
    mlflow.sklearn.log_model(pipeline, "sentiment-model")
    print(f"\nMLflow run complete. Model logged.")