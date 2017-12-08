# coding=utf8


class TrieNode(object):
    '''
    Trie 节点.
    '''
    def __init__(self):
        self.val = None
        self.trans = {}


class Trie(object):
    '''
    Trie: 实现脏词索引数据的生成, 以及提供脏词检测.
    为了减少Trie树的深度, 使用unicode字符编码构建, 而不使用'utf-8'编码.
    '''
    def __init__(self):
        # 初始化Trie树的根节点.
        self.root = TrieNode()
        self.word_set = set()

    def add(self, word):
        '''
        生成 Trie 字典树.
        @return: 暂无.
        @param word[type unicode]: 单个脏词, 必须是 unicode 类型.
        '''
        curr_node = self.root
        for ch in word:
            tmp_node = curr_node.trans.get(ch)
            if tmp_node is None:
                curr_node.trans[ch] = TrieNode()
                curr_node = curr_node.trans[ch]
            else:
                curr_node = tmp_node
        curr_node.val = word
        self.word_set.add(word)

    def __walk(self, trie_node, ch):
        '''
        检查当前节点中是否包含 unicode 字符.

        @return: 如果匹配, 返回 unicode 字符对应的节点.
            否则, 返回 None.
        '''
        if ch in trie_node.trans:
            trie_node = trie_node.trans.get(ch)
            return trie_node
        return None

    def __find_ch(self, sub_content):
        '''
        从 sub_content 中筛选出脏词.

        @return: 被命中的脏词.
        @rtype: list.
        @param sub_content[unicode]: 待检测内容.
        '''
        words = []
        limit = len(sub_content)
        curr_node = self.root
        for start in xrange(limit):
            ch = sub_content[start]
            curr_node = self.__walk(curr_node, ch)
            if curr_node is None:
                return words
            if curr_node.val:
                words.append(curr_node.val)
        return words

    def match_all(self, content):
        '''
        找出内容中的所有脏词.

        @return: 命中的脏词列表.
        @rtype: list.
        @param content[type unicode]: 待检测的 unicode 字符串.
        '''
        ret = []
        size = len(content)
        for index in xrange(size):
            val = self.__find_ch(content[index:size])
            if val:
                ret.extend(val)
        return ret

    @property
    def words(self):
        return self.word_set


if __name__ == '__main__':
    trie = Trie()
    # 危险词列表
    q_keywords_list = [u'虫', u'老鼠']
    if q_keywords_list:
        for keyword in q_keywords_list:
            trie.add(keyword)
    # 危险词
    content = u'老鼠'
    keywords = list(set(trie.match_all(content)))
    print keywords
