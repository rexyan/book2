# --coding:utf-8--

from hashlib import md5
import settings
import io
import re
import os
from models.model import *


def sec_pass(new_passworld):
    '''
    :param new_passworld:
    :return:
    '''
    return md5(new_passworld + settings.SECRET_KEY).hexdigest()


def check_pass_re(password):
    '''
    :param password:
    :return:
    '''
    pattern = re.compile(
        # ur'^(?:(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])|(?=.*[A-Z])(?=.*[a-z])(?=.*[^A-Za-z0-9])|(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])|(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9])).{8,}')
        ur'^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(.{8,})'
        # ur'^(.{8,})')
    )
    return pattern.search(password)


def check_email_re(email):
    '''
    :param email:
    :return:
    '''
    if len(email) >= 5:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False


def check_mail_exist(email):
    '''
    :param email:
    :return:
    '''
    obj = User.objects.filter(mail=email)
    if obj:
        return False
    else:
        return True


def randomstring(n):
    '''
    :param n:
    :return:
    '''
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(n))))[0:40]






if __name__ == '__main__':
    print randomstring(40)