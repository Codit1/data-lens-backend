from fastapi import HTTPException, status
import pandas as pd
import numpy as np
from pathlib import Path

from App.services.load_datasets import load_dataset

BASE_DIR = Path(__file__).resolve().parent.parent

def search_by_column(dataset_id: str, column: str, query: str, page: int =1, limit: int=50):
    
    try:
        df = load_dataset(dataset_id)
        if column not in df.columns.to_list():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Column not found")
        
        result = df[df[column].astype(str).str.contains(query, case=False, na=False)]

        total = len(result)

        start = (page - 1) * limit
        end = start + limit

        result = result.iloc[start:end]

        if result.empty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")

        return {
            "total_results": total,
            "page": page,
            "limit": limit,
            "data": result.to_dict(orient="records")
        }    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def search_all_dataset(dataset_id: str, query: str, page: int =1, limit: int=50):


    try:
        df = load_dataset(dataset_id)

        result = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False).any(), axis=1)]

        total = len(result)

        start = (page - 1) * limit
        end = start + limit

        result = result.iloc[start:end]

        if result.empty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")

        return {
            "total_results": total,
            "page": page,
            "limit": limit,
            "data": result.to_dict(orient="records")
        }    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    