from fastapi import HTTPException, status
import pandas as pd
import numpy as np
from pathlib import Path

from App.services.save_datasets import save_datasets

BASE_DIR = Path(__file__).resolve().parent.parent

def get_datasets_info(file):

    file_name = file.filename.lower()

    file.file.seek(0)

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

    columns_type = {col: str(dtype) for col, dtype in df.dtypes.items()}

    df = df.replace({np.nan: None})

    columns = df.columns.tolist()

    data_set_head = df.head(10).to_dict(orient="records")

    null_values_data_set = int(df.isnull().sum().sum())

    null_value_columns = df.isnull().sum().to_dict()

    null_percentage = float((df.isnull().sum().sum() / df.size) * 100)

    total_columns = int(df.shape[1])

    total_rows = int(df.shape[0])

    no_duplicate = int(df.duplicated().sum())

    no_unique = df.nunique().to_dict()

    return {
        "dataset_id": save_datasets(file),
        "columns": columns,
        "columns_type": columns_type,
        "data_set_head": data_set_head,
        "null_values_data_set": null_values_data_set,
        "null_value_columns": null_value_columns,
        "null_percentage": null_percentage,
        "total_columns": total_columns,
        "total_rows": total_rows,
        "no_duplicate": no_duplicate,
        "no_unique": no_unique
    }