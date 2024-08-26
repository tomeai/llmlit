from pydantic import BaseModel


class DiskItem(BaseModel):
    query: str
    topK: int
