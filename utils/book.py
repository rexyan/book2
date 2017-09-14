# --coding:utf-8--
from models.model import *


def get_mongo_book(id):
    return BookCache.objects.get(id=id)