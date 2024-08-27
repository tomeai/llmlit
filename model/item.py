from typing import Optional

from pydantic import BaseModel


class DiskItem(BaseModel):
    query: str
    category: Optional[int]
    type: Optional[int]
    topK: int


class DiskDetailItem(BaseModel):
    id: str
