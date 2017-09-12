# --coding:utf-8--

from models.model import *
from common.log_utils import getLogger
import sys
import argparse
from utils import auth

log = getLogger('init_user.py')


def init_user():
    user = User(
        name=u'rex_yan',
        mail=u'rs.yan@kindle.com',
        password=auth.sec_pass('123456789'),
    )
    user.save()
    log.debug('user %s added.' % user.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--forceclean", type=bool,
                        help="force clean old data", default=False)
    args = parser.parse_args()

    if User.objects.count() > 0:
        if args.forceclean:
            if 'y' != raw_input('Try to delete all user. Continue? (y/n)'):
                log.info('User canceled.')
                sys.exit(0)

            User.objects.all().delete()
            log.info('All user deleted.')
        else:
            log.info('User already initialized, skip.')
            sys.exit(1)

    init_user()
