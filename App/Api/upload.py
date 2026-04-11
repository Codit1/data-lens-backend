from fastapi import APIRouter, UploadFile, Response, status, File

from App.helper.upload import get_datasets_info, get_datasets_summary, get_dataset_values

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/file", status_code=status.HTTP_202_ACCEPTED)
def upload_file(file: UploadFile = File(...)):

    return get_datasets_info(file=file)


@router.get("/summary/{dataset_id}")
def dataset_summary(dataset_id: str):
    
    return get_datasets_summary(dataset_id=dataset_id)

@router.post("/values/{dataset_id}/{page}/{limit}")
def get_dataset_values_pagination(dataset_id: str, page: int, limit: int):

    return get_dataset_values(dataset_id=dataset_id, page=page, limit=limit)