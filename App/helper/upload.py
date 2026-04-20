from fastapi import HTTPException, status
import pandas as pd
import numpy as np
from pathlib import Path
import math

from App.services.save_datasets import save_datasets
from App.services.load_datasets import load_dataset

BASE_DIR = Path(__file__).resolve().parent.parent

def get_datasets_info(file):

    # ---------------------------
    # 1. Load file safely
    # ---------------------------
    file_name = file.filename.lower()
    file.file.seek(0)

    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file.file)

        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file.file)

        elif file_name.endswith(".json"):
            df = pd.read_json(file.file)

        else:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported file type"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading file: {str(e)}"
        )
    

    raw_df = df

    raw_df = raw_df.dropna()

    # ---------------------------
    # 2. Clean dataset (IMPORTANT)
    # ---------------------------
    df = df.replace([np.nan, np.inf, -np.inf], None)

    # ---------------------------
    # 3. Basic metadata
    # ---------------------------
    columns = df.columns.tolist()
    total_rows, total_columns = df.shape


    columns_type = {col: str(dtype) for col, dtype in raw_df.dtypes.items()}
    data_set_head = raw_df.head(100).to_dict(orient="records")

    # ---------------------------
    # 4. Null handling
    # ---------------------------
    null_counts = df.isnull().sum()
    total_nulls = int(null_counts.sum())

    null_value_columns = {col: int(val) for col, val in null_counts.items()}
    null_percentage = (
        float((total_nulls / df.size) * 100)
        if df.size > 0 else 0.0
    )

    # ---------------------------
    # 5. Duplicates & uniqueness
    # ---------------------------
    no_duplicate = int(df.duplicated().sum())
    no_unique = {col: int(val) for col, val in df.nunique().items()}
    total_no_unique = int(df.nunique().sum())
    total_value_columns = {col: int(val) for col, val in df.count().items()}
    total_no_value_columns = int(df.count().sum())

    # ---------------------------
    # 6. Column previews (optimized)
    # ---------------------------

    previews = {}

    for col in columns:
        value_counts = df[col].value_counts(dropna=True)

        previews[col] = {
            # "values": [
            #     str(v) if v is not None else None
            #     for v in col_series.tolist()
            # ],
            "value_counts": {str(k): int(v) for k, v in value_counts.items()}
        }

    # ---------------------------
    # 7. Dataset-wide value counts
    # ---------------------------

    # ---------------------------
    # 8. Final safety cleaner
    # ---------------------------
    def clean_nan(obj):
        if isinstance(obj, dict):
            return {k: clean_nan(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nan(i) for i in obj]
        elif isinstance(obj, float) and math.isnan(obj):
            return None
        return obj

    # ---------------------------
    # 9. Reset file pointer
    # ---------------------------
    file.file.seek(0)

    # ---------------------------
    # 10. Return response
    # ---------------------------
    return clean_nan({
        "dataset_id": save_datasets(file),
        "columns_list": columns,
        "columns_type": columns_type,
        "dataset_head": data_set_head,
        "total_nulls": total_nulls,
        "null_value_columns": null_value_columns,
        "null_percentage": null_percentage,
        "total_columns": total_columns,
        "total_rows": total_rows,
        "no_duplicate": no_duplicate,
        "no_unique": no_unique,
        "total_no_unique": total_no_unique,
        "total_value_columns": total_value_columns,
        "total_no_value_columns": total_no_value_columns,
        "value_counts": previews,
    })


def get_datasets_summary(dataset_id: int):
    
    df = load_dataset(dataset_id)

    raw_df = df

    raw_df = raw_df.dropna()

    # ---------------------------
    # 2. Clean dataset (IMPORTANT)
    # ---------------------------
    df = df.replace([np.nan, np.inf, -np.inf], None)

    # ---------------------------
    # 3. Basic metadata
    # ---------------------------
    columns = df.columns.tolist()
    total_rows, total_columns = df.shape

    columns_type = {col: str(dtype) for col, dtype in raw_df.dtypes.items()}
    data_set_head = raw_df.head(100).to_dict(orient="records")

    # ---------------------------
    # 4. Null handling
    # ---------------------------
    null_counts = df.isnull().sum()
    total_nulls = int(null_counts.sum())

    null_value_columns = {col: int(val) for col, val in null_counts.items()}
    null_percentage = (
        float((total_nulls / df.size) * 100)
        if df.size > 0 else 0.0
    )

    # ---------------------------
    # 5. Duplicates & uniqueness
    # ---------------------------
    no_duplicate = int(df.duplicated().sum())
    no_unique = {col: int(val) for col, val in df.nunique().items()}
    total_no_unique = int(df.nunique().sum())
    total_value_columns = {col: int(val) for col, val in df.count().items()}
    total_no_value_columns = int(df.count().sum())


    # ---------------------------
    # 6. Column previews (optimized)
    # ---------------------------

    previews = {}

    for col in columns:
        value_counts = df[col].value_counts(dropna=True)

        previews[col] = {
            # "values": [
            #     str(v) if v is not None else None
            #     for v in col_series.tolist()
            # ],
            "value_counts": {str(k): int(v) for k, v in value_counts.items()}
        }

    # ---------------------------
    # 7. Dataset-wide value counts
    # ---------------------------

    # ---------------------------
    # 8. Final safety cleaner
    # ---------------------------
    def clean_nan(obj):
        if isinstance(obj, dict):
            return {k: clean_nan(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nan(i) for i in obj]
        elif isinstance(obj, float) and math.isnan(obj):
            return None
        return obj


    # ---------------------------
    # 9. Return response
    # ---------------------------
    return clean_nan({
        "columns_list": columns,
        "columns_type": columns_type,
        "dataset_head": data_set_head,
        "total_nulls": total_nulls,
        "null_value_columns": null_value_columns,
        "null_percentage": null_percentage,
        "total_columns": total_columns,
        "total_rows": total_rows,
        "no_duplicate": no_duplicate,
        "no_unique": no_unique,
        "total_no_unique": total_no_unique,
        "total_value_columns": total_value_columns,
        "total_no_value_columns": total_no_value_columns,
        "value_counts": previews,
    })


# func to get datset values for pagination
def get_dataset_values(dataset_id: str, page: int =1, limit: int=100):

    df = load_dataset(dataset_id)

    start = (page - 1) * limit
    end = start + limit

    result = df.iloc[start:end]

    result = result.replace(
        [np.nan, np.inf, -np.inf],
        None
    )


    return result.to_dict(orient="records")
