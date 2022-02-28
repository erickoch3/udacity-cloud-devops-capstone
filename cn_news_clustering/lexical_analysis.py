""" Conduct NLP Pre-Processing """
import jieba
import re
# TODO: The following two libraries speed up parsing
# import lxml
# import cchardet

def tokenize(sentence):
    """ Removes duplicates and punctuation from sentence. """
    without_duplicates = re.sub(r'(.)\1+', r'\1\1', sentence)
    without_punctuation = re.sub(r'[^\w]','',without_duplicates)
    return jieba.lcut(without_punctuation)

def is_chinese_char(char):
    """ Confirms that a given utf-8 is a Chinese Character """
    if u'\u4e00' <= char <= u'\u9fff':
        return True
    return False

