from fastapi import APIRouter, UploadFile, Response, status

from App.helper.columns import get_column_info

router = APIRouter(prefix="/datalens")

@router.get("/columns/{dataset_id}/{column}")
def get_columns_info(dataset_id: str, column: str):
    return get_column_info(dataset_id, column)