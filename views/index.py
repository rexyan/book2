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
    def post(self, book_id):
        from common import up_qiniu
        douban_id = book_id
        #up_file = self.request.files["up_file"]
        up_file = self.request.files["up_file"]
        tmp_path = None
        if douban_id and up_file:
        # 将本地保存到本地
            for meta in up_file:
                filename = unicode(int(time.time()))+'.'+meta['filename'].split('.')[-1::][0]
                if meta['filename'].split('.')[-1::][0] in settings.UP_FILE_TYPE:
                    tmp_path = os.path.join(os.path.join(os.getcwd()), 'tmp_file', 'upload_file')
                    file_path = os.path.join(tmp_path, filename)
                    with open(file_path, 'wb') as up:
                        up.write(meta['body'])
                    up_server_status = True
                    up_server_msg = u'文件上传成功'
        # 文件上传七牛云
            up_qiniu_get_file_key = None
            ret, info = up_qiniu.upload_file_to_qiniu(os.path.join(tmp_path, filename), filename)
            if json.loads(info.text_body).get('key') and json.loads(info.text_body).get('hash'):
                up_qiniu = True
                up_qiniu_msg = u'文件存储成功，新文件名为：'+filename
                up_qiniu_get_file_key = json.loads(info.text_body).get('key')
        # 根据ID获取书籍信息
        book_info = None
        cache_obj = BookCache.objects.all()
        for x in cache_obj:
            if x['content']['id'] == douban_id:
                book_info= x.to_dict()

        # 保存作者信息
        is_save = True
        book_obj = Author.objects.all()
        for x in book_obj:
            if x['name'] == book_info['content']['author'][0]:
                is_save = False
                author_id = x.oid
                break
        if is_save:
            author_obj = Author(
                name = book_info['content']['author'][0],
                introduction = book_info['content']['author_intro']
            )
            author_obj.save()
        else:
            author_obj = Author.objects.get(id = author_id)

        # 保存书籍信息
        book_obj = Book(
            name= book_info['content']['alt_title'], # 书名
            author_id = author_obj.oid,  # 作者ID
            subtitle = book_info['content']['subtitle'], # 副标题
            publication = book_info['content']['pubdate'],  # 出版时间
            isdb = book_info['content']['isbn13'],  # ISBN
            introduction = book_info['content']['summary'],  # 简介
            down_key = up_qiniu_get_file_key,  # 七牛key
            img_link = book_info['content']['images']['large'],  # 豆瓣图片链接
            douban_link = book_info['content']['alt'],  # 豆瓣链接
            score = book_info['content']['rating']['average'],  # 豆瓣评分
            integral = float(book_info['content']['price'])/10,  # 书籍积分
        )
        book_obj.save()
        db_save = True
        db_save_msg = u'书籍信息保存成功'
        if db_save and up_qiniu and up_server_status:
            status = True
        else:
            status = False

        # 删除本地文件
        os.remove(os.path.join(tmp_path, filename))
        self.write_json(code=status, data=[up_server_msg,up_qiniu_msg,db_save_msg])