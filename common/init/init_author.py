# --coding:utf-8--

from models.model import *
from common.log_utils import getLogger
import sys
import argparse
from utils import auth

log = getLogger('init_author.py')


def init_author():
    author = Author(
        name=u'[日] 宫下奈都',
        introduction=u'[日]宫下奈都（Miyashita Natsu）↵1967年生于日本福井县。毕业于日本上智大学人文学院哲学系。2004年凭借《静静的雨》入围“文学界新人奖”，登上文坛。2007年发表长篇小说《第四学校》大获好评。2011年出版的《有人不满足》获得“书店大奖”提名。其他作 品还包括《倾听远方的声音》《喜悦之歌》《太阳意大利面和豆子汤》《乡下男装店的模特老婆》《两个印记》《只有这么多》等。↵罗越（Luo Yue）↵1983年生于上海。毕业于南京大学中文系，辅修日语。曾为职杂志编辑、撰稿人，现为专职日文译者。酷爱影视剧与日本文化，自称“日剧爱好家”。翻译作品包括白石一文《这里是没有我们存在的地方》、冈田淳《在滑梯下躲雨》、大沼纪子“深夜面包房”系列等。↵（新浪微博@罗越的日剧人间／个人网站 luoyueblog.lofter.com）',
    )
    author.save()
    log.debug('author %s added.' % author.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--forceclean", type=bool,
                        help="force clean old data", default=False)
    args = parser.parse_args()

    if Author.objects.count() > 0:
        if args.forceclean:
            if 'y' != raw_input('Try to delete all author. Continue? (y/n)'):
                log.info('Author canceled.')
                sys.exit(0)

            Author.objects.all().delete()
            log.info('All Author deleted.')
        else:
            log.info('Author already initialized, skip.')
            sys.exit(1)

    init_author()
