# --coding:utf-8--

import tornado
from base import BaseHandler
from view_utils import *
import settings
import os
import time
from common import check_code
import io
from utils import auth
from common import up_qiniu
from common import send_mail
from common.log_utils import getLogger
log = getLogger('index.py')


class IndexHandler(BaseHandler):
    def get(self):
        # 首页部分（按时间排序）
        book = get_hot_book_time()

        # 下载排行（按下载推荐数）
        book_down_order_id = get_order_book_down()
        book_down_order_id_list =  [x.book_id for x in book_down_order_id]
        book_down_order_data = get_book_info(book_down_order_id_list)

        # 热门作家（按书籍评分）
        hot_author_order_id = get_order_author()
        order_author_list = [x.content['id'] for x in hot_author_order_id]
        hot_author_order_data = get_book_info(order_author_list)

        self.render('index.html', book=book, book_down_order_data = book_down_order_data, hot_author_order_data= hot_author_order_data)


class UploadHandler(BaseHandler):
    def get(self):
        # 第一列（按时间）
        book = get_hot_book_time()

        # 第二列（tag排序）
        for x in get_order_tag():
            print x
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
        from utils import auth
        password = self.get_argument('pass', None)
        email = self.get_argument('email', None)
        obj = User.objects.filter(mail=email, password=auth.sec_pass(password))
        status = False
        data = None
        if obj:
            for x in obj:
                if not x.status:
                    data = u'账户未激活！请转到注册邮箱激活'
                else:
                    status = True
                    self.session.set('user_id', x.to_dict())
        else:
            data = u'邮箱或密码不正确！'
        self.write_json(code=status, data=data)


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        from utils import auth
        from common import send_mail
        import time
        status = False
        data = None
        name = self.get_argument('name', None)
        password = self.get_argument('pass', None)
        email = self.get_argument('email', None)
        user_key = auth.randomstring(40)
        if name and password and email:
            if auth.check_email_re(email):
                if auth.check_pass_re(password):
                    if auth.check_mail_exist(email):
                        obj = User(
                            name = name,
                            key = user_key,
                            password = auth.sec_pass(password),
                            mail = email
                        )
                        obj.save()
                        status = True
                        send_mail.email([email, ], settings.DOMAIN_NAME + '/' +'activation/?user_key='+user_key, u'Kindle15-账户激活', [u"kinlde15", u'book@kindle15.com'])
                        data = u'完成注册，需激活邮箱才能正常使用，赶快去激活吧！'
                    else:
                        data = u'邮箱已经被注册'
                else:
                    data = u'密码为大于8位的大小写字母及数字组合'
            else:
                data = u'邮箱格式不正确'
        else:
            data = u'信息未填写完整'
        self.write_json(code=status, data=data)


class IFrameHandler(BaseHandler):
    def get(self):
        self.render('iframe_upload.html')

    def post(self):
        pass


class GetbookHandler(BaseHandler):
    @auth.authenticated
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
    @auth.authenticated
    def post(self, book_id):
        from common import up_qiniu
        douban_id = book_id
        # up_file = self.request.files["up_file"]
        up_file = self.request.files["up_file"]
        tmp_path = None
        filename = None
        up_server_status = None
        up_qiniu_get_file_key = None
        up_server_msg = None
        up_qiniu_msg = None
        # 将本地保存到本地
        if douban_id and up_file:
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
                book_info = x.to_dict()

        # 保存作者信息
        is_save = True
        author_id = None
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
            author_obj = Author.objects.get(id=author_id)

        # 保存到文件映射表
        map_obj = File_Map(
            user_id = self.session.get('user_id')['id'],
            user_name = self.session.get('user_id')['name'],
            book_id = book_info['content']['id'],
            qiniu_key = up_qiniu_get_file_key
        )
        map_obj.save()

        if  up_qiniu and up_server_status:
            status = True
        else:
            status = False

        # 删除本地文件
        os.remove(os.path.join(tmp_path, filename))
        self.write_json(code=status, data=[up_server_msg, up_qiniu_msg])


class CheckCodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        stream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(stream, "png")
        self.session.set('check_code', code)  # 利用session保存验证码
        self.write(stream.getvalue())


class ActivaHandler(BaseHandler):
    def get(self, *args, **kwargs):
        status = False
        user_key =self.get_argument('user_key')
        if len(user_key) == 40:
            obj = User.objects.filter(key=user_key)
            if obj:
                for x in obj:
                    x.status = True
                    x.save()
                data = u'success'
                status = True
            else:
                data = u'param_error'
        else:
            data = u'param_error'
        self.redirect("/login?user_active="+str(status))
        #self.write_json(code=status, data=data)


class SelectVersionHandler(BaseHandler):
    def get(self):
        book_id = self.get_argument('book_id', None)
        if book_id:
            map_obj = File_Map.objects.filter(book_id =book_id)
            print [x.to_dict() for x in map_obj]
        self.render('select_version.html' ,map_obj=map_obj)

    def post(self):
        pass


class Push_Or_DownHandler(BaseHandler):
    @auth.authenticated
    def get(self):
        status = False
        data = ''
        id = self.get_argument('id', None)
        type = self.get_argument('type', None)
        # 下载七牛文件到本地
        if id and type:
            obj = File_Map.objects.get(id=id)
            sta, url, key = up_qiniu.get_file_on_qiniu(obj.qiniu_key)  # 获取七牛url
            tmp_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'tmp_file','download_file')
            down_status = up_qiniu.down_file(url, key, tmp_path)
            user = self.session.get('user_id')
            if down_status:
                if type == '1':  # 下载
                    down_data_file = os.path.join(tmp_path, key)
                    self.set_header('Content-Type', 'application/octet-stream')
                    self.set_header('Content-Disposition', 'attachment; filename=' + key)
                    with open(down_data_file, "rb") as f:
                        while True:
                            data = f.read(4096)
                            if not data:
                                break
                            self.write(data)
        self.finish()
        status = True
        # 删除服务器文件
        down_obj = Down(
            user_id=user['id'],
            book_id=id,
            status=status
        )
        down_obj.save()
        obj.push_down_count = obj.push_down_count + 1
        obj.save()
        os.remove(os.path.join(tmp_path, key))

    @auth.authenticated
    def post(self):
        status = False
        data = ''
        id = self.get_argument('id',None)
        type = self.get_argument('type',None)
        # 下载七牛文件到本地
        if id and type:
            obj = File_Map.objects.get(id=id)
            sta, url, key = up_qiniu.get_file_on_qiniu(obj.qiniu_key)  # 获取七牛url
            tmp_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'tmp_file','download_file')
            down_status = up_qiniu.down_file(url, key, tmp_path)
            if down_status:
                if type == '2': # 推送
                    user = self.session.get('user_id')
                    email_status = send_mail.email_att(user['mail'], '', settings.EMAIL_PUSH_SUBJECT, settings.EMAIL_PUSH_SENDER, os.path.join(tmp_path,key), key)
                    if email_status:
                        status = True
                        data = u'邮件发送成功'
                    else:
                        data = u'邮件发送失败'
                else:
                    data = u'无效操作'
                # 删除服务器文件
                os.remove(os.path.join(tmp_path, key))
            else:
                data = u'文件获取失败'
            push_obj = Push(
                user_id = user['id'] ,
                book_id = id,
                status = status
            )
            push_obj.save()
            obj.push_down_count = obj.push_down_count+1
            obj.save()
            self.write_json(code=status, data=data)


class CiYuWordCloud(BaseHandler):

    def get(self):
        from pyecharts import WordCloud
        name = ['Sam S Club', 'Macys', 'Amy Schumer', 'Jurassic World', 'Charter Communications',
                'Chick Fil A', 'Planet Fitness', 'Pitch Perfect', 'Express', 'Home', 'Johnny Depp',
                'Lena Dunham', 'Lewis Hamilton', 'KXAN', 'Mary Ellen Mark', 'Farrah Abraham',
                'Rita Ora', 'Serena Williams', 'NCAA baseball tournament', 'Point Break']
        value = [10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112, 965, 847, 582, 555,
                 550, 462, 366, 360, 282, 273, 265]
        wordcloud = WordCloud(width='100%', height='100%')
        wordcloud.add("", name, value, word_size_range=[20, 100])
        wordcloud.render(path=os.path.join('template', 'render.html'))
        self.render('render.html')
