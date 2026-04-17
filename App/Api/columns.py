from fastapi import APIRouter, UploadFile, Response, status

from App.helper.columns import get_column_info, get_columns_values

router = APIRouter(prefix="/datalens")

@router.get("/columns/{dataset_id}/{column}")
def get_columns_info(dataset_id: str, column: str):
    return get_column_info(dataset_id, column)

@router.get("/columns/pagination/{dataset_id}/{column}/{page}/{limit}")
def get_columns_values_pagination(dataset_id: str, column: str, page: int, limit: int):
    return get_columns_values(dataset_id, column, page, limit)