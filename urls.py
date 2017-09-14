from views.index import *

url = [
        (r"/index", IndexHandler),
        (r"/", IndexHandler),
        (r"/upload", UploadHandler),
        (r"/base", BaseHandler),
        (r"/login", LoginHandler),
        (r"/register", RegisterHandler),
        (r"/iframe_upload", IFrameHandler),
        (r"/getbook", GetbookHandler),
        (r"/up_file_to_server", UpFileToServerHandler),
      ]