# --coding:utf-8--

import tornado
from base import BaseHandler
from view_utils import *
import settings
import os
import time


class IndexHandler(BaseHandler):
    def get(self):
        book = get_hot_book()
        self.render('index.html', book=book)


class UploadHandler(BaseHandler):
    def get(self):
        book = get_hot_book()
        self.render('upload.html', book=book)

    def post(self):
        pass


class BaseHandler(BaseHandler):
    def get(self):
        self.render('base.html')

    def post(self):
        pass


class LoginHandler(BaseHandler):
    def get(self):
        self.render('signin.html')

    def post(self):
        pass


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        pass


class IFrameHandler(BaseHandler):
    def get(self):
        self.render('iframe_upload.html')

    def post(self):
        pass


class GetbookHandler(BaseHandler):
    def post(self):
        import requests
        import json

        douban_book_id = self.get_argument('data')
        cache_data = None
        # 查询数据库是否有该书的信息，有则返回，没有调用豆瓣
        skip_douban = False
        cache_obj = BookCache.objects.all()
        for x in cache_obj:
            if x['content']['id'] == douban_book_id:
                skip_douban = True
                cache_data = x.to_dict()['content']
                break

        # 走API
        if not skip_douban:
            url = settings.DOUBAN_GET_BOOK_INFO_API+str(douban_book_id)
            info = requests.get(url)
            request_status = json.loads(info.content)
            if request_status.get('code'):
                status = False
                data = request_status.get('msg')
            else:
                status = True
                data = request_status
                # 将信息存入数据库，下次就不用再去调用API
                cache_obj = BookCache(content=data)
                cache_obj.save()
        else:
            status = True
            data = cache_data
        # TODO 查询该书是否已经有人上传了
        self.write_json(code=status, data=data)


    def get(self):
        pass


class UpFileToServerHandler(BaseHandler):
    def post(self, *args, **kwargs):
        douban_id = self.get_body_arguments('douban_id', None)
        up_file = self.request.files["up_file"]
        if douban_id and up_file:
            # 将本地保存到本地
            for meta in up_file:
                if meta['content_type'] in settings.UP_FILE_TYPE:
                    filename = meta['filename'].split('.')
                    tmp_path = os.path.join(os.path.join(os.getcwd()), 'tmp_file', 'upload_file')
                    file_path = os.path.join(tmp_path, filename)
                    with open(file_path, 'wb') as up:
                        up.write(meta['body'])

        self.write_json('11111')