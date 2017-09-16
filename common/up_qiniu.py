#  --coding:utf-8--

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import settings
from common.log_utils import getLogger
import requests
import os
log = getLogger('qiniu.py')


def authentication_qiniu(access, secret):
    '''
    :param access:
    :param secret:
    :return:
    '''
    access_key = access
    secret_key = secret
    q = Auth(access_key, secret_key)
    log.debug('authentication_qiniu %s.' % q)
    return q


def upload_file_to_qiniu(file_path, new_name):
    '''
    :param file_path:
    :param new_name:
    :return:
    '''
    q = authentication_qiniu(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    bucket_name = settings.QINIU_BUCKET_NAME
    key = new_name
    token = q.upload_token(bucket_name, key, 3600)
    policy = {
        'fsizeLimit': 1,
        "mimeLimit": "image/png"
    }
    localfile = file_path
    ret, info = put_file(token, key, localfile, policy)
    log.debug('upload_file_to_qiniu', ret, info)
    return ret, info


def get_file_on_qiniu(key):
    '''
    :param key:
    :return:
    '''
    q = authentication_qiniu(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    base_url = settings.QINIU_USER_DOMAIN+'/'+key
    private_url = q.private_download_url(base_url, expires=3600)
    r = requests.get(private_url)
    log.debug('get_file_on_qiniu', r.status_code, private_url)
    return r.status_code == 200, private_url, key


def down_file(url, new_nama, file_path):
    res = requests.get(url)
    res.raise_for_status()
    playFile = open(os.path.join(file_path, new_nama), 'wb')
    for chunk in res.iter_content(100000):
        playFile.write(chunk)
    playFile.close()
    return True

if __name__=='__main__':
    '''
    七牛文件下载到本地例子
    '''
    sta, url, key = get_file_on_qiniu('1505581615.txt') #获取七牛url
    print sta, url, key
    tmp_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),'tmp_file', 'download_file')
    status = down_file(url, key, tmp_path) # 下载到本地
    print status