from fastapi import APIRouter

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)
