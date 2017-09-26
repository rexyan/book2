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
        (r"/up_file_to_server/(?P<book_id>\w*)", UpFileToServerHandler),
        (r"/up_file_to_server/(?P<book_id>\w*)", UpFileToServerHandler),
        (r"/get_check_code", CheckCodeHandler),
        (r"/activation/(\w*)", ActivaHandler),
        (r"/select_version", SelectVersionHandler),
        (r"/push_down_book", Push_Or_DownHandler),
        (r"/ciyu", CiYuWordCloud),
      ]