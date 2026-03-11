from fastapi import APIRouter, UploadFile, Response, status

from App.helper.upload import get_datasets_info

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/file", status_code=status.HTTP_202_ACCEPTED)
def upload_file(file: UploadFile):

    return get_datasets_info(file=file)


@router.post("/test")
def upload_file():

    return get_datasets_info()