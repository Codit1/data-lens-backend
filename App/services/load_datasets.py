from fastapi import HTTPException, status
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_dataset(dataset_id: str):

    files = list(BASE_DIR.glob(f"datasets/{dataset_id}*"))

    if not files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )

    file_path = files[0]

    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path)

    elif file_path.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(file_path)

    elif file_path.suffix == ".json":
        df = pd.read_json(file_path)

    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported dataset format"
        )

    return df