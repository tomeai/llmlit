from fastapi import APIRouter

router = APIRouter(
    prefix="/disk",
    tags=["disk"],
    responses={404: {"description": "Not found"}},
)
