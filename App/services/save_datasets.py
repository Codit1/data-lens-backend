import uuid
import time
import shutil
from pathlib import Path
from fastapi import HTTPException, status


BASE_DIR = Path(__file__).resolve().parent.parent


def generating_uniqueID():
    timestamp = str(int(time.time()))[-6:]
    short_uuid = uuid.uuid4().hex[:8]
    return f"{timestamp}{short_uuid}"


def save_datasets(dataset):

    dataset_id = generating_uniqueID()

    dataset_dir = BASE_DIR / "datasets"
    dataset_dir.mkdir(exist_ok=True)

    filename = dataset.filename.lower()

    if filename.endswith(".csv"):
        file_path = dataset_dir / f"{dataset_id}.csv"

    elif filename.endswith((".xlsx", ".xls")):
        file_path = dataset_dir / f"{dataset_id}.xlsx"

    elif filename.endswith(".json"):
        file_path = dataset_dir / f"{dataset_id}.json"

    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported dataset format"
        )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(dataset.file, buffer)

    return dataset_id

