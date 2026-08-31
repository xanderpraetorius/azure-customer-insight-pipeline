import os
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pyodbc
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

# --- Label and train ---
def label_sentiment(rating):
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

df["sentiment"] = df["rating"].apply(label_sentiment)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=500, stop_words="english")),
    ("clf", LogisticRegression(max_iter=200, random_state=42))
])
pipeline.fit(df["review_text"], df["sentiment"])

# --- Predict ---
df["predicted_sentiment"] = pipeline.predict(df["review_text"])
df["sentiment_score"] = df["rating"] / 5.0
print("Predictions complete")

# --- Write to Azure SQL ---
server = "customer-insight-server.database.windows.net"
database = "customer-insight-db"
username = "sqladmin"
password = os.getenv("SQL_PASSWORD")

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Clear existing scores
cursor.execute("DELETE FROM sentiment_scores")
conn.commit()
print("Cleared existing sentiment scores")

# Get actual review IDs from database
cursor.execute("SELECT review_id, reviewer_id FROM reviews")
db_reviews = cursor.fetchall()
print(f"Found {len(db_reviews)} reviews in database")

# Match on reviewer_id
df_merged = df.copy()
for db_review_id, db_reviewer_id in db_reviews:
    mask = df_merged["reviewer_id"] == db_reviewer_id
    if mask.any():
        row = df_merged[mask].iloc[0]
        cursor.execute("""
            INSERT INTO sentiment_scores 
                (review_id, sentiment_label, sentiment_score, topic_cluster)
            VALUES (?, ?, ?, ?)
        """,
            db_review_id,
            row["predicted_sentiment"],
            float(row["sentiment_score"]),
            row["category"]
        )

conn.commit()
conn.close()
print(f"Written sentiment scores to Azure SQL")