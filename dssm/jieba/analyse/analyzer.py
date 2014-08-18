#encoding=utf-8
from whoosh.analysis import RegexAnalyzer,LowercaseFilter,StopFilter,StemFilter
from whoosh.analysis import Tokenizer,Token 
from whoosh.lang.porter import stem

import jieba
import re

STOP_WORDS = frozenset(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can',
                        'for', 'from', 'have', 'if', 'in', 'is', 'it', 'may',
                        'not', 'of', 'on', 'or', 'tbd', 'that', 'the', 'this',
                        'to', 'us', 'we', 'when', 'will', 'with', 'yet',
                        'you', 'your',u'的',u'了',u'和',
                        ' ', '!', '\"', '.', '\'', '\\', '*', ',', '/', '(', ')', '^',
                        '-', '+','=', '_', '%', '..', '...', '<', '>', ':', '\'', '\"', '`',
                        '&', '#', '$', '|','{', '}', '[', ']', ';','?',
                        u'（', u'）', u'！', u'，', u'。', u'？', u'～', u'－',u'+', u'／', u'?',
                        u'】', u'【', u'＝',u' ',u'‘',u'’',u'…',u'［',u'］',u'＿',u'＋',u'＂',
                        u'〈', u'〉',
                        u'“', u'”', u'＃', u'％', u'．', u'：', u'；', u'＜', u'＞', u'＊'))

accepted_chars = re.compile(ur"[\u4E00-\u9FA5]+")

class ChineseTokenizer(Tokenizer):
    def __call__(self,text,**kargs):
        words = jieba.tokenize(text,mode="search")
        token  = Token()
        for (w,start_pos,stop_pos) in words:
            if not accepted_chars.match(w):
                if len(w)>1:
                    pass
                else:
                    continue
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token

def ChineseAnalyzer(stoplist=STOP_WORDS,minsize=1,stemfn=stem,cachesize=50000):
    return ChineseTokenizer() | LowercaseFilter() | StopFilter(stoplist=stoplist,minsize=minsize)\
                                        |StemFilter(stemfn=stemfn, ignore=None,cachesize=cachesize)
