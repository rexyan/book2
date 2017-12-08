# --coding:utf-8--

from models.model import *
from bson import ObjectId


def get_hot_book_time():
    return BookCache.objects.order_by("-up_time")[:30]


def get_order_book_down():
    return File_Map.objects.order_by("-push_down_count")[:30]


def get_book_info(*arg):
    obj_list = []
    for i, x in enumerate(arg[0]):
        obj_list.extend(BookCache.objects.filter(content__id = arg[0][i]))  # 采用extend，让返回的list只有一层
    return obj_list


def get_order_author():
    return BookCache.objects.order_by('-content__rating__average')[:10]


def get_order_tag():
    return BookCache.objects.order_by('-content__tags')[:10]