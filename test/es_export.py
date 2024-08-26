#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：codeline
@File    ：stream_query.py
@Author  ：fovegage
@Email   ：fovegage@gmail.com
@Date    ：2022/5/29 19:13
"""
import os
from typing import List

import pandas as pd
from elasticsearch import Elasticsearch
from pymilvus import MilvusClient
from zhipuai import ZhipuAI


class Config:
    MILVUS_HOST = os.getenv("MILVUS_HOST", "10.6.16.191")
    MILVUS_PORT = os.getenv("MILVUS_PORT", 30185)


# client = MilvusClient(
#     uri=f"http://{Config.MILVUS_HOST}:{Config.MILVUS_PORT}",
#     db_name='opentome',
#     keep_alive=True
# )


def upsert_milvus(rows, col='disk_info_v1'):
    res = client.upsert(
        collection_name=col,
        data=rows
    )
    print(res)


class ZhiPuEmbedding:
    def __init__(self):
        self.client = ZhipuAI(api_key="4db7d8ee4b10c5909ee4dd532185ba95.JeiZeNSwhL04PIGn")

    def embed_documents(self, texts: List[str]):
        """Compute doc embeddings using a modelscope embedding model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
            :param texts:
            :param model:
        """
        response = self.client.embeddings.create(
            model="embedding-3",
            input=texts,
        )

        return [x.embedding for x in response.data]

    def embed_query(self, text: str):
        """Compute query embeddings using a modelscope embedding model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
            :param text:
        """
        response = self.client.embeddings.create(
            model="embedding-3",
            input=text,
        )
        return response.data[0].embedding


es = Elasticsearch(['elastic:416798GaoZhe!@192.168.12.126:9200'])
ml = ZhiPuEmbedding()
page = es.search(
    index='disk_resources',
    scroll='2m',
    size=10000,
    body={
        "query": {
            "match_all": {}
        }
    }
)


def write_es(body):
    """
    {'name': '刘继卣-战国故事（插图）.pdf', 'share_name': '幻*倾城', 'source': '1', 'type': 1, 'path': 'e9-Ppxu4HYeyi9kWHxHhJA', 'pwd': 'o866', 'third_id': 'ysedsl2r', 'insert_time': '2022-05-29 20:11:08', 'create_time': 1623814610}}
    :param body:
    :return:
    """
    # print(len(body), body)
    # for item in body:
    #     _source = item['_source']
    #     name = _source.get('name')
    #     embedding = ml.embed_query(name)
    #     _source['vector'] = embedding
    #     # 目前只对name向量
    #     _source['text'] = name
    #     _source['id'] = _source.get('path')
    #     upsert_milvus(_source)

    df = pd.DataFrame([x['_source'] for x in body])
    print(df)
    df.to_csv('disk.csv', mode='a', index=False, header=False)


sid = page['_scroll_id']
scroll_size = page['hits']['total']['value']
print(sid, scroll_size)
actions = page['hits']['hits']
# print(actions)
write_es(actions)
# Start scrolling
while True:
    page = es.scroll(scroll_id=sid, scroll='2m')
    # Update the scroll ID
    sid = page['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = page['hits']['hits']
    if len(scroll_size) == 0:
        break
    write_es(scroll_size)
