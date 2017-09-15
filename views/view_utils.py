# --coding:utf-8--

from models.model import *
from bson import ObjectId


def get_hot_book():
    return BookCache.objects.all()