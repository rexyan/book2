from views.index import *

url = [
        (r"/index", IndexHandler),
        (r"/", IndexHandler),
        (r"/upload", UploadHandler),
      ]