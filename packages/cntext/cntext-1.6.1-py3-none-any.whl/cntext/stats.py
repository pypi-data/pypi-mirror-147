import re
import jieba
from collections import Counter
import numpy as np
import pathlib
import pickle
import os

def cn_seg_sent(text):
    #中文分句函数
    text = re.sub('([。！；？;\?])([^”’])', "[[end]]", text)  # 单字符断句符
    text = re.sub('([。！？\?][”’])([^，。！？\?])', "[[end]]", text)
    text = re.sub('\s', '', text)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    return text.split("[[end]]")


def load_pkl_dict(file, is_builtin=True):
    """
    导入pkl词典文件,
    :param file: pkl词典文件路径
    :param is_builtin: 是否为cntext的内置pkl文件。默认True
    """
    if is_builtin==True:
        pathchain = ['files',file]
        dict_file_path = pathlib.Path(__file__).parent.joinpath(*pathchain)
        dict_f = open(dict_file_path, 'rb')
    else:
        dict_f = open(file, 'rb')
    dict_obj = pickle.load(dict_f)
    return dict_obj




def dict_pkl_list():
    """
    获取cntext内置词典列表(pkl格式)
    """
    dict_file_path = pathlib.Path(__file__).parent.joinpath('files')
    return [f for f in os.listdir(dict_file_path) if 'pkl' in f]



STOPWORDS_zh = load_pkl_dict(file='STOPWORDS.pkl')['STOPWORDS']['chinese']
STOPWORDS_en = load_pkl_dict(file='STOPWORDS.pkl')['STOPWORDS']['english']
ADV_words = load_pkl_dict(file='ADV_CONJ.pkl')['ADV']
CONJ_words = load_pkl_dict(file='ADV_CONJ.pkl')['CONJ']



def term_freq(text, language='chinese'):
    """
    计算词频
    :param text: 文本字符串数据
    :param language: 语言类型，"chinese"或"english"，默认"chinese"
    """
    if language=='chinese':
        text = ''.join(re.findall('[\u4e00-\u9fa5]+', text))
        words = list(jieba.cut(text))
        words = [w for w in words if w not in STOPWORDS_zh]
    else:
        words = text.lower().split(" ")
        words = [w for w in words if w not in STOPWORDS_en]
    return Counter(words)



def readability(text, zh_adjconj=None, language='chinese'):
    """
    文本可读性，指标越大，文章复杂度越高，可读性越差。
    :param text: 文本字符串数据
    :param zh_adjconj 中文连词与副词词表，接收列表数据类型。默认使用cntext自带的词典
    :param language: 语言类型，"chinese"或"english"，默认"chinese"
    ------------
    【英文可读性】公式 4.71 x (characters/words) + 0.5 x (words/sentences) - 21.43；
    【中文可读性】  参考自   【徐巍,姚振晔,陈冬华.中文年报可读性：衡量与检验[J].会计研究,2021(03):28-44.】
                 readability1 ---每个分句中的平均字数
                 readability2  ---每个句子中副词和连词所占的比例
                 readability3  ---参考Fog Index， readability3=(readability1+readability2)×0.5
                 以上三个指标越大，都说明文本的复杂程度越高，可读性越差。

    """
    if language=='english':
        text = text.lower()
        #将浮点数、整数替换为num
        text = re.sub('\d+\.\d+|\.\d+', 'num', text)
        num_of_characters = len(text)
        #英文分词
        rgx = re.compile("(?:(?:[^a-zA-Z]+')|(?:'[^a-zA-Z]+))|(?:[^a-zA-Z']+)")
        num_of_words = len(re.split(rgx, text))
        #分句
        num_of_sentences = len(re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text))
        ari = (
                4.71 * (num_of_characters / num_of_words)
                + 0.5 * (num_of_words / num_of_sentences)
                - 21.43
        )

        return {"readability": ari}
    if language=='chinese':
        if zh_adjconj:
            adv_conj_words = zh_adjconj
        else:
            adv_conj_words = set(ADV_words + CONJ_words)
        zi_num_per_sent = []
        adv_conj_ratio_per_sent = []
        text = re.sub('\d+\.\d+|\.\d+', 'num', text)
        #【分句】
        sentences = cn_seg_sent(text)
        for sent in sentences:
            adv_conj_num = 0
            zi_num_per_sent.append(len(sent))
            words = list(jieba.cut(sent))
            for w in words:
                if w in adv_conj_words:
                    adv_conj_num+=1
            adv_conj_ratio_per_sent.append(adv_conj_num/(len(words)+1))
        readability1 = np.mean(zi_num_per_sent)
        readability2 = np.mean(adv_conj_ratio_per_sent)
        readability3 = (readability1+readability2)*0.5
        return {'readability1': readability1,
                'readability2': readability2,
                'readability3': readability3}




def sentiment(text, diction, language='chinese'):
    """
    使用diy词典进行情感分析，计算各个情绪词出现次数，未考虑强度副词、否定词对情感的复杂影响，
    :param text:  待分析中文文本
    :param diction:  情感词字典；
    :param language: 语言类型，"chinese"或"english"，默认"chinese"

    {'category1':  'category1 词语列表',
     'category2': 'category2词语列表',
     'category3': 'category3词语列表',
     ...
    }
    :return:
    """
    result_dict = dict()
    senti_categorys = diction.keys()

    stopword_num = 0
    for senti_category in senti_categorys:
        result_dict[senti_category+'_num'] = 0

    #sentence_num = len(re.split('[。！!？\?;；]+', text))-1

    
    if language=='chinese':
        sentence_num = len(cn_seg_sent(text))
        words = list(jieba.cut(text))
        word_num = len(words)
        for word in words:
            if word in STOPWORDS_zh:
                stopword_num+=1
            for senti_category in senti_categorys:
                if word in diction[senti_category]:
                    result_dict[senti_category+'_num'] +=  1

    else:
        sentence_num = len(re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text))
        rgx = re.compile("(?:(?:[^a-zA-Z]+')|(?:'[^a-zA-Z]+))|(?:[^a-zA-Z']+)")
        words = re.split(rgx, text)
        word_num = len(words)
        for word in words:
            if word in STOPWORDS_en:
                stopword_num+=1
            for senti_category in senti_categorys:
                if word in diction[senti_category]:
                    result_dict[senti_category+'_num'] +=  1

    result_dict['stopword_num'] = stopword_num
    result_dict['word_num'] = word_num
    result_dict['sentence_num'] = sentence_num
    return result_dict






