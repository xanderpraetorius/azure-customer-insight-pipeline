import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

# Sample Amazon-style reviews dataset
data = {
    "product_id": [
        "B001", "B001", "B001", "B002", "B002",
        "B003", "B003", "B004", "B004", "B005",
        "B001", "B002", "B003", "B004", "B005"
    ],
    "reviewer_id": [
        "U001", "U002", "U003", "U004", "U005",
        "U006", "U007", "U008", "U009", "U010",
        "U011", "U012", "U013", "U014", "U015"
    ],
    "rating": [5, 4, 2, 5, 3, 5, 4, 5, 1, 4, 3, 2, 5, 4, 5],
    "review_text": [
        "Exceptional sound quality and battery life. Best headphones I have owned.",
        "Great noise cancellation but slightly uncomfortable after long use.",
        "Stopped working after two months. Very disappointing build quality.",
        "Incredible bass and very loud for its size. Highly recommend.",
        "Decent speaker but battery drains faster than advertised.",
        "My back pain disappeared after switching to this chair. Worth every cent.",
        "Very comfortable but assembly instructions were confusing.",
        "Keeps water cold for 24 hours as promised. Excellent product.",
        "Lid started leaking after first wash. Complete waste of money.",
        "Very comfortable for long runs. True to size.",
        "Average product, nothing special but does the job.",
        "Terrible customer service when it broke after a week.",
        "Best office chair I have ever used. Highly recommend.",
        "Good quality but arrived with a small dent.",
        "Perfect fit and very comfortable for trail running."
    ],
    "category": [
        "Electronics", "Electronics", "Electronics", "Electronics", "Electronics",
        "Furniture", "Furniture", "Kitchen", "Kitchen", "Sports",
        "Electronics", "Electronics", "Furniture", "Kitchen", "Sports"
    ],
    "verified": [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1]
}

df = pd.DataFrame(data)
csv_path = "data/reviews_sample.csv"
df.to_csv(csv_path, index=False)
print(f"CSV created: {csv_path} ({len(df)} rows)")

# Upload to Blob Storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "customerinsight"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create container if it doesn't exist
try:
    blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created")
except Exception:
    print(f"Container '{container_name}' already exists")

# Upload CSV
blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob="data/reviews_sample.csv"
)
with open(csv_path, "rb") as f:
    blob_client.upload_blob(f, overwrite=True)

print(f"Uploaded reviews_sample.csv to blob storage container '{container_name}'")