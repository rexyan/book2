import tornado
from base import BaseHandler
from view_utils import *
import settings


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
        url = settings.DOUBAN_GET_BOOK_INFO_API+str(douban_book_id)
        info = requests.get(url)
        request_status = json.loads(info.content)
        if request_status.get('code'):
            status = False
            data = request_status.get('msg')
        else:
            status = True
            data = request_status
        self.write_json(code=status,data=data)

    def get(self):
        pass