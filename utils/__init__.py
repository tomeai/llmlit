from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: int
    data: dict | list | str | None = None
    msg: str


def create_response(data: dict | list | str | None = None, code: int = 200, msg: str = "success") -> ResponseModel:
    return ResponseModel(code=code, data=data, msg=msg)
