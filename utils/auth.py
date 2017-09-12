# --coding:utf-8--

from hashlib import md5
import settings


def sec_pass(new_passworld):
    '''
    :param new_passworld:
    :return:
    '''
    return md5(new_passworld + settings.SECRET_KEY).hexdigest()
