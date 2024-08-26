from pymilvus import MilvusClient

from config.settings import settings

milvus_client = MilvusClient(
    uri=f"http://{settings.MILVUS_HOST}:{settings.MILVUS_PORT}",
    db_name='model'
)
