#  --coding:utf-8--

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import settings
from common.log_utils import getLogger
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
    import requests
    q = authentication_qiniu(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    base_url = settings.QINIU_USER_DOMAIN+'/'+key
    private_url = q.private_download_url(base_url, expires=3600)
    r = requests.get(private_url)
    log.debug('get_file_on_qiniu', r.status_code, private_url)
    return r.status_code == 200, private_url