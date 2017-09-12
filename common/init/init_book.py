# --coding:utf-8--

from models.model import *
from common.log_utils import getLogger
import sys
import argparse
from utils import auth

log = getLogger('init_book.py')


def init_book():
    book = Book(
        name=u'羊与钢的森林',
        subtitle=u'一个调音师的成长故事',
        publication='2012-3',
        isdb='9787508679181',
        introduction=u'外村自幼生长在北海道的深山小村庄，家境贫寒。刻板平凡的中学生活，一成不变的山居岁月，没有选择的迷茫前途，似乎都注定了他无论怎样努力也无法摆脱出身的困扰。↵偶然有一天，老师让他帮忙接待一位钢琴调音师，那架年久失修的钢琴经过调音师的妙手，竟发出宛如天籁的美妙音色。↵琴音就像一道微光，照亮外村的灰暗人生。↵从那一刻起，外村便立志成为一名调音师。↵然而，不得不承认，人与人的先天条件千差万别。他来自封闭落后的环境，此前从未接触过钢琴。纵然拼尽全力刻苦练习，反复聆听钢琴乐曲，诚惶诚恐地跟着前辈仔细观摩，在客户眼中，在神秘高贵的钢琴面前，他仍然是个畏缩羞怯，欠缺天赋的乡村青年。↵生来没有拿到一手好牌，那么努力是否有用？↵只有音乐生而平等，与自然、世界融为一体，被包容，被接纳，被一视同仁。说不出口的话，难以言尽的迷茫和挫折，或许可以让音乐，替你发声。↵外村，能否如愿告别大山，走进音乐的广袤森林呢？',
        down_key=u'羊与钢的森林.mobi',
        img_link='https://img1.doubanio.com/lpic/s29507149.jpg',
        douban_link='https://book.douban.com/subject/27094416/',
        score=8.6,
        integral=1,
    )
    book.save()
    log.debug('book %s added.' % book.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--forceclean", type=bool,
                        help="force clean old data", default=False)
    args = parser.parse_args()

    if Book.objects.count() > 0:
        if args.forceclean:
            if 'y' != raw_input('Try to delete all book. Continue? (y/n)'):
                log.info('Book canceled.')
                sys.exit(0)

            Book.objects.all().delete()
            log.info('All book deleted.')
        else:
            log.info('Book already initialized, skip.')
            sys.exit(1)

    init_book()
