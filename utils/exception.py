# coding=utf8
AJAX_SUCCESS = 0
AJAX_FAIL_NORMAL = 1
AJAX_FAIL_AUTH = 2
AJAX_FAIL_NOTLOGIN = 3


class CommonException(Exception):
    '''
        非常规错误, 自定义返回内容
    '''
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = errmsg or ""
        self.data = data

    def __str__(self):
        return self.message


class ValidateException(Exception):
    '''
        校验错误，字段错误
    '''
    def __init__(self, errmsg, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = u"{0}不合法".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message


class MultException(Exception):
    '''
        字段已存在
    '''
    def __init__(self, errmsg, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = u"{0}已存在".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message


class NotExistException(Exception):
    '''
        不存在
    '''
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = u"{0}不存在".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message


class PermException(Exception):
    '''
        权限错误
    '''
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_AUTH
        self.message = errmsg or u"权限错误"
        self.data = None

    def __str__(self):
        return self.message


class NotLoginException(Exception):
    '''
        用户未登录
    '''
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NOTLOGIN
        self.message = errmsg or '用户未登录'
        self.data = None

    def __str__(self):
        return self.message


class LackOfFieldException(Exception):
    """
        缺少字段
    """
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = u"缺少字段{0}".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message


class DeleteInhibitException(Exception):
    """
        禁止删除
    """
    def __init__(self, errmsg=None, data=None):
        self.code = AJAX_FAIL_NORMAL
        self.message = u"不可删除{0}".format(errmsg)
        self.data = data

    def __str__(self):
        return self.message


if __name__ == "__main__":
    try:
        raise DeleteInhibitException("data")
    except DeleteInhibitException as e:
        print(e.code, e.message)
