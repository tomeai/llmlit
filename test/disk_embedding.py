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
from pymilvus import MilvusClient
from zhipuai import ZhipuAI


class Config:
    MILVUS_HOST = os.getenv("MILVUS_HOST", "10.6.16.191")
    MILVUS_PORT = os.getenv("MILVUS_PORT", 30185)


client = MilvusClient(
    uri=f"http://{Config.MILVUS_HOST}:{Config.MILVUS_PORT}",
    db_name='opentome',
    keep_alive=True
)


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
            model="embedding-2",
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
            model="embedding-2",
            input=text,
        )
        return response.data[0].embedding


ml = ZhiPuEmbedding()


def read_disk():
    """
    {'name': '刘继卣-战国故事（插图）.pdf', 'share_name': '幻*倾城', 'source': '1', 'type': 1, 'path': 'e9-Ppxu4HYeyi9kWHxHhJA', 'pwd': 'o866', 'third_id': 'ysedsl2r', 'insert_time': '2022-05-29 20:11:08', 'create_time': 1623814610}}
    :param body:
    :return:
    """
    line = {'name': '刘继卣-战国故事（插图）.pdf', 'share_name': '幻*倾城', 'source': '1', 'type': 1,
            'path': 'e9-Ppxu4HYeyi9kWHxHhJA', 'pwd': 'o866', 'third_id': 'ysedsl2r',
            'insert_time': '2022-05-29 20:11:08', 'create_time': 1623814610}

    df = pd.read_csv('disk.csv', chunksize=500,
                     names=['name', 'share_name', 'source', 'type', 'path', 'pwd', 'third_id', 'insert_time',
                            'create_time'])

    for chunk in df:
        try:
            results = []
            item = [x for _, x in chunk.iterrows()]
            embeds = ml.embed_documents([x.get('name') for x in item])
            for index, line in enumerate(item):
                name = line.get('name')
                line['vector'] = embeds[index]
                # 目前只对name向量
                line['text'] = name
                line['id'] = line.get('path')
                line['title'] = line.pop('name')
                line['pwd'] = str(line['pwd'])
                line['create_time'] = str(line['create_time'])
                results.append(dict(line))
                print(dict(line))
            upsert_milvus(results)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    read_disk()
