import contextlib

import uvicorn
from fastapi import FastAPI
from starlette import status

from db.mysql import account_database
from router import disk


@contextlib.asynccontextmanager
async def lifespan(app):
    async with account_database.connect():
        print("Run at startup!")
        yield
        print("Run on shutdown!")


app = FastAPI(
    lifespan=lifespan,
    root_path='/agent/v1',
    servers=[
        {
            "url": "http://39.107.54.241:8989/agent/v1",
            "description": "Production server"
        }
    ],
)


@app.get(
    "/healthz",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
def healthz():
    """
    心跳检测
    :return:
    """
    return "OK"


# @app.on_event("startup")
# async def startup_db():
#     print("Startup event is triggered.")
#     await account_database.connect()
#     connections.connect(host=MILVUS_HOST, port=MILVUS_PORT, alias="default")
#     print("Startup event is done.")
#
#
# @app.on_event("shutdown")
# async def shutdown_db():
#     print("shutdown event is triggered.")
#     await account_database.disconnect()
#     connections.disconnect(alias="default")
#     print("shutdown event is done.")


app.include_router(disk.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
