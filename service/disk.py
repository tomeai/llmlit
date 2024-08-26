from pymilvus import Collection, RRFRanker

from db.milvus import milvus_client
from utils.embedding import ZhiPuEmbedding


class DiskService:
    def __init__(self):
        self.milvus_client = milvus_client
        self.embedding = ZhiPuEmbedding()
        self.collection = Collection(name="disk_info_v1")
        self.ranker = RRFRanker()

    def hybrid(self, query: str, top_k: int):
        search_param = {
            "data": [self.embedding.embed_query(query)],
            "anns_field": "vector",
            "param": {"metric_type": "IP", "params": {"nprobe": 10, "nlist": 128}},
            "limit": top_k,
            "output_fields": [
                'title', 'share_name', 'source', 'type', 'path', 'pwd', 'insert_time',
                'create_time'
            ]
        }
        self.collection.load()

        hits = []
        results = self.collection.search(**search_param)
        for result in results:
            for item in result:
                did = item.id
                distance = item.distance
                entity = item.entity
                title = entity.title
                share_name = entity.share_name
                source = entity.source
                type_ = entity.type
                path = entity.path
                insert_time = item.insert_time
                create_time = item.create_time
                line = {
                    "id": did, "score": distance, "share_name": share_name,
                    "title": title, "source": source,
                    "type": type_, "path": path,
                    "insert_time": insert_time, "create_time": create_time
                }
                hits.append(line)

        return hits
