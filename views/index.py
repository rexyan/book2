import tornado
from base import BaseHandler
from view_utils import *


class IndexHandler(BaseHandler):
    def get(self):
        book = get_hot_book()
        self.render('index.html', book=book)

class UploadHandler(BaseHandler):
    def get(self):
        self.render('upload.html')

    def post(self):
        pass
