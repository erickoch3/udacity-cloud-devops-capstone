""" Conduct NLP Pre-Processing """
import jieba
import re
from googletrans import Translator


def tokenize(sentence):
    """ Removes duplicates and punctuation from sentence. """
    without_duplicates = re.sub(r'(.)\1+', r'\1\1', sentence)
    without_punctuation = re.sub(r'[^\w]','',without_duplicates)
    return jieba.lcut(without_punctuation)

def is_chinese_char(char):
    """ Confirms that a given utf-8 is a Chinese Character """
    if '\u4e00' <= char <= '\u9fff':
        return True
    return False

def translate_df_cn_to_en(df):
    """ Given a Pandas dataframe, translate from Chinese to English and return new dataframe """
    translator = Translator()
    t_df = df.copy(deep=True)
    for column in df.columns.values:
        t_df[column] = df[column].apply(translator.translate, src='zh-CN', dest='en').apply(getattr, args=('text',))
    return t_df