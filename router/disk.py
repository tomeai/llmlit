from fastapi import APIRouter, Depends

from model.item import DiskItem
from service.disk import DiskService
from utils import create_response

router = APIRouter(
    prefix="/disk",
    tags=["disk"],
    responses={404: {"description": "Not found"}},
)


@router.post("/search")
async def disk_search(
        item: DiskItem,
        service: DiskService = Depends(DiskService)
):
    """

    :param item:
    :param service:
    :return:
    """
    data = service.hybrid(item.query, item.topK)
    return create_response(data)
