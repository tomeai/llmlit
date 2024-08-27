import os

from pymilvus import MilvusClient, DataType


class Config:
    MILVUS_HOST = os.getenv("MILVUS_HOST", "10.6.16.191")
    MILVUS_PORT = os.getenv("MILVUS_PORT", 30186)


client = MilvusClient(
    uri=f"http://{Config.MILVUS_HOST}:{Config.MILVUS_PORT}",
    db_name='opentome',
    keep_alive=True
)


def create_disk_index():
    """
    {'name': '刘继卣-战国故事（插图）.pdf', 'share_name': '幻*倾城', 'source': '1', 'type': 1, 'path': 'e9-Ppxu4HYeyi9kWHxHhJA', 'pwd': 'o866', 'third_id': 'ysedsl2r', 'insert_time': '2022-05-29 20:11:08', 'create_time': 1623814610}
    :return:
    """
    # 不使用动态字段, 默认使用动态字段
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=False,
    )

    # 主键 取网盘资源id
    schema.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=100, is_primary=True)
    # 标题
    schema.add_field(field_name="title", datatype=DataType.VARCHAR, max_length=1000)
    # 分享人
    schema.add_field(field_name="share_name", datatype=DataType.VARCHAR, max_length=100)
    # 网盘类型  百度云 阿里云 ...
    schema.add_field(field_name="source", datatype=DataType.INT8)
    # 文件类型  txt mp4 ....
    schema.add_field(field_name="type", datatype=DataType.INT8)
    # 文件链接
    schema.add_field(field_name="path", datatype=DataType.VARCHAR, max_length=1000)
    # 密码
    schema.add_field(field_name="pwd", datatype=DataType.VARCHAR, max_length=20)
    # third_id
    schema.add_field(field_name="third_id", datatype=DataType.VARCHAR, max_length=100)
    # insert_time
    schema.add_field(field_name="insert_time", datatype=DataType.VARCHAR, max_length=20)
    # create_time
    schema.add_field(field_name="create_time", datatype=DataType.VARCHAR, max_length=20)

    # 向量内容 目前只对标题  后期对标题+内容
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=3000)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)

    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="IVF_FLAT",
        metric_type="IP",
        params={"nprobe": 10, "nlist": 128}
    )
    client.create_collection(collection_name="disk_info_v1", schema=schema, index_params=index_params)


if __name__ == '__main__':
    create_disk_index()
