# --coding:utf-8--

import mongoengine as models
import json
from tornado.util import ObjectDict
import datetime


class BaseDoc(object):
    @property
    def oid(self):
        return str(self.id)

    def to_dict(self):
        d = json.loads(self.to_json())
        d['id'] = self.oid
        d.pop('_id')
        return ObjectDict(d)

    def to_json(self):
        d = json.loads(self.to_json())
        d['id'] = self.oid
        d.pop('_id')
        return d

    def __unicode__(self):
        try:
            return self.name
        except AttributeError:
            return self.oid


class Book(models.Document, BaseDoc):
    name = models.StringField(max_length=100)  # 书名
    author_id = models.StringField(max_length=100)  # 作者ID
    subtitle = models.StringField(max_length=100)  # 副标题
    publication = models.StringField(max_length=20)  # 出版时间
    isdb = models.StringField(max_length=20)  # ISBN
    introduction = models.StringField(max_length=5000)  # 简介
    down_key = models.StringField(max_length=30)  # 七牛key
    img_link = models.StringField(max_length=200)  # 豆瓣图片链接
    douban_link = models.StringField(max_length=200)  # 豆瓣链接
    score = models.FloatField(default=0)  # 豆瓣评分
    integral = models.FloatField(default=0)  # 书籍积分
    up_time = models.DateTimeField(default=datetime.datetime.now)


class Author(models.Document, BaseDoc):
    name = models.StringField(max_length=100)  # 作者名称
    introduction = models.StringField(max_length=5000)  # 作者简介


class Down(models.Document, BaseDoc):
    user_id = models.StringField(max_length=50)  # 书籍ID
    book_id = models.StringField(max_length=50)  # BookID
    status = models.BooleanField(default=False) # 下载状态


class Push(models.Document, BaseDoc):
    user_id = models.StringField(max_length=50)  # 书籍ID
    book_id = models.StringField(max_length=50)  # BookID
    status = models.BooleanField(default=False)  # 推送状态


class Collection(models.Document, BaseDoc):   # 收藏表
    user_id = models.IntField(max_length=20)  # 书籍ID
    book_id = models.IntField(max_length=20)  # BookID


class User(models.Document, BaseDoc):
    name = models.StringField(max_length=100)  # 用户名称
    mail = models.StringField(max_length=30)  # 用户邮箱
    key = models.StringField(max_length=40)  # 用户唯一key
    password = models.StringField(max_length=40)  # 用户密码
    status = models.BooleanField(default=False)  # 用户状态
    down_remain = models.IntField(default=100)  # 下载剩余次数
    push_remain = models.IntField(default=100)  # 下载剩余次数


class BookCache(models.Document, BaseDoc):  # 从豆瓣获取书籍信息后，将此书信息保存
    content = models.DictField(max_length=8000)  # json内容
    up_time = models.DateTimeField(default=datetime.datetime.now)


class File_Map(models.Document, BaseDoc):
    user_id = models.StringField(max_length=100) # 上传用户ID
    user_name = models.StringField(max_length=100) # 上传用户name
    book_id = models.StringField(max_length=100) # 书籍ID
    qiniu_key =  models.StringField(max_length=100) # 七牛链接
    up_time = models.DateTimeField(default=datetime.datetime.now)  # 上传时间
    push_down_count = models.IntField(default=0)  # 下载次数