import uuid
import time
from pathlib import Path
from fastapi import HTTPException, status
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

def generating_uniqueID():
    timestamp = str(int(time.time()))[-6:]  # Last 6 digits of timestamp
    short_uuid = str(uuid.uuid4().hex[:8])  # First 8 characters of UUID
    return f"{timestamp}{short_uuid}"

def save_datasets(dataset):

    dataset_id = generating_uniqueID()

    if dataset.filename.endswith(".csv"):
        file_path = BASE_DIR / "datasets" / f"{dataset_id}.csv"

    elif dataset.filename.endswith((".xlsx", ".xls")):
        file_path = BASE_DIR / "datasets" / f"{dataset_id}.xlsx"

    elif dataset.filename.endswith(".json"):
        file_path = BASE_DIR / "datasets" / f"{dataset_id}.json"

    with open(file_path, "wb") as f:
        f.write(dataset.file.read())

    return dataset_id

