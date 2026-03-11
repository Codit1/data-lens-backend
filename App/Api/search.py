from fastapi import APIRouter, UploadFile, Response, status

from App.helper.search import search_all_dataset, search_by_column

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/search")
async def search(dataset_id: str, column: str, query: str, page: int =1, limit: int=50):
    return search_by_column(dataset_id, column, query, page, limit)


@router.post("/search_all")
async def search(dataset_id: str, query: str, page: int =1, limit: int=50):

    return search_all_dataset(dataset_id=dataset_id, query=query, page=page, limit=limit)


