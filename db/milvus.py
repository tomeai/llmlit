import os

from pymilvus import MilvusClient

MILVUS_BIYAO_CATE_INFO = os.getenv("MILVUS_BIYAO_CATE_INFO", "biyao_cate_info_v1")
MILVUS_TMALL_CATE_INFO = os.getenv("MILVUS_TMALL_CATE_INFO", "tmall_cate_info_v1")
MILVUS_SPU_INFO = os.getenv("MILVUS_SPU_INFO", "product_spu_info_v1")
MILVUS_QA_INFO = os.getenv("MILVUS_QA_INFO", "butler_qa_pairs_v1")
MILVUS_DOCUMENT_INFO = os.getenv("MILVUS_DOCUMENT_INFO", "butler_document_chunk_v2")

MILVUS_HOST = os.getenv("MILVUS_HOST", "10.6.16.191")
MILVUS_PORT = os.getenv("MILVUS_PORT", "30185")

model_client = MilvusClient(
    uri=f"http://{MILVUS_HOST}:{MILVUS_PORT}",
    db_name='model'
)

rag_client = MilvusClient(
    uri=f"http://{MILVUS_HOST}:{MILVUS_PORT}",
    db_name='rag'
)