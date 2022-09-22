# -*- coding: utf-8 -*-

"""
@Time    : 2022/9/22 10:27 上午
@Author  : hcai
@Email   : hua.cai@unidt.com
"""
import re
from config.config import question_path
# queries = ["Python", "Python web", "Python开发", "Python web开发视频教程"]

def clean_space(text):
  """"
  处理多余的空格
  """
  match_regex = re.compile(u'[\u4e00-\u9fa5。\.,，:：《》、\(\)（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z]+')
  should_replace_list = match_regex.findall(text)
  order_replace_list = sorted(should_replace_list,key=lambda i:len(i),reverse=True)
  for i in order_replace_list:
    if i == u' ':
      continue
    new_i = i.strip()
    text = text.replace(i,new_i)
  return text

class Trie(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = {}
        self.end = -1
        self.load_question()

    def load_question(self):
        with open(question_path, 'r') as fr:
            for item in fr.readlines():
                if not item.strip():
                    continue
                self.insert(item.strip())

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        word = word.lower()
        curNode = self.root
        for c in word:
            if not c in curNode:
                curNode[c] = {}
            curNode = curNode[c]
        curNode[self.end] = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        curNode = self.root
        for c in word:
            if not c in curNode:
                return False
            curNode = curNode[c]

        # Doesn't end here
        if not self.end in curNode:
            return False

        return True

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        curNode = self.root
        for c in prefix:
            if not c in curNode:
                return False
            curNode = curNode[c]

        return True

    def get_start(self,prefix):
        '''
        给出一个前辍，打印出所有匹配的字符串
        :param prefix:
        :return:
        '''
        def get_key(pre,pre_node):
            result = []
            if pre_node.get(self.end):
                result.append(pre)
            for key in pre_node.keys():
                if key != self.end:
                    result.extend(get_key(pre+key,pre_node.get(key)))
            return result


        if not self.startsWith(prefix):
            return []
        else:
            node = self.root
            for p in prefix:
                node = node.get(p)
            else:
                return get_key(prefix,node)

if __name__ == "__main__":
    trie = Trie()
    print(trie.search("Python"))
    print(trie.search("Perl 算法 源码"))
    print((trie.get_start('P')))
    print((trie.get_start('Python web')))
    print((trie.get_start('Python 算')))
    print(clean_space('中国的首都是beijing，apple is an 中国的new product'))
