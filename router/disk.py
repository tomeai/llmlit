from fastapi import APIRouter, Depends

from model.item import DiskItem, DiskDetailItem
from service.disk import DiskService
from utils import create_response

router = APIRouter(
    prefix="/disk",
    tags=["disk"],
    responses={404: {"description": "Not found"}},
)


@router.get("/info")
async def disk_info():
    """
    首页信息查询 缓存
    :return:
    """
    notice = '支持正版，严厉打击各类资源贩子，欢迎举报问题资源！'
    tips = '红盘搜索不储存、复制、传播任何文件，内容均由网络爬虫自动抓取'
    wx_pic = 'https://img.alicdn.com/tfs/TB1UdKEM6TpK1RjSZKPXXa3UpXa-256-256.png'
    keys = ['python', 'golang']
    hot_list = {
        'hot_time': '2021-05-02 12:12:12',
        'hot_resource': [{
            'id': '111',
            'title': 'python',
            'type': 1,
            'category': 2,
            'size': 1000,
            'modify_time': "2021-05-02 12:12:12",
        }] * 15
    }
    # 贡献资源最多的
    resource_rank = []

    # 社区互动最多的
    community_rank = []

    return create_response({
        'notice': notice,
        'tips': tips,
        'wx_pic': wx_pic,
        'keys': keys,
        'hot_list': hot_list,
        'community_rank': community_rank,
        'resource_rank': resource_rank,
    })


@router.post("/query")
async def disk_query(
        item: DiskDetailItem,
        service: DiskService = Depends(DiskService)
):
    """
    从mysql数据库查询
    :param item:
    :param service:
    :return:
    """
    data = {'title': '刘继卣-战国故事（插图）.pdf', 'share_name': '幻*倾城', 'source': '1', 'type': 1,
            'path': 'e9-Ppxu4HYeyi9kWHxHhJA', 'pwd': 'o866', 'third_id': 'ysedsl2r',
            'insert_time': '2022-05-29 20:11:08', 'create_time': 1623814610}

    return create_response(data)


@router.post("/search")
async def disk_search(
        item: DiskItem,
        service: DiskService = Depends(DiskService)
):
    """

    :param item:
    :param service:
    :return:
    """
    data = service.hybrid(item.query, item.topK)
    return create_response(data)
