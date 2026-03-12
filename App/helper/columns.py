from fastapi import HTTPException, status
import pandas as pd
import numpy as np
from pathlib import Path

from App.services.load_datasets import load_dataset

BASE_DIR = Path(__file__).resolve().parent.parent

def get_column_info(dataset_id: str, column: str, ):

    df = load_dataset(dataset_id)

    col = df[column]

    profile = {
        "column_name": column,
        "dtype": str(col.dtype),
        "total_values": len(col),
        "null_count": int(col.isnull().sum()),
        "unique_values_count": int(col.nunique())
    }

    if pd.api.types.is_numeric_dtype(col):

        profile["stats"] = {
            "min": float(col.min()),
            "max": float(col.max()),
            "mean": float(col.mean()),
            "median": float(col.median()),
            "std": float(col.std())
        }


        hist = col.value_counts(bins=10)

        distribution = [
            {
                "range": str(k),
                "count": int(v)
            }
            for k, v in hist.items()
        ]

        profile["distribution"] = distribution

    profile["top_values"] = col.value_counts().head(10).to_dict()

    profile["value_count"] = col.value_counts().to_dict()

    profile["duplicate_counts"] = int(df[column].duplicated().sum())

    profile["unique_values"] = df[column].dropna().unique().tolist()[:100]

    profile["values"] = df[column].dropna().tolist()[:100]


    return profile


