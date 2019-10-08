import itertools
import os
import re

import jieba
from wordcloud import WordCloud


def get_rhyme(f_name):
    f = open('./lyrics/' + f_name, 'r', encoding='UTF-8')
    text = f.readlines()
    f.close()

    '''处理开头'''
    for m, n in enumerate(text):
        if '编曲：' in n:
            lyric_drop_head = text[m + 1:]
        elif '评论数' in n:
            lyric_drop_head = text[m + 1:]

    '''处理结尾'''
    for o, p in enumerate(lyric_drop_head):
        if '制作人：陈令韬/欧智\n' in p:
            lyric_text_tail = lyric_drop_head[:o]
            break
        elif '音乐监制：' in p:
            lyric_text_tail = lyric_drop_head[:o]
            break
        elif '混音：' in p:
            lyric_text_tail = lyric_drop_head[:o]
            break
        elif '收起' in p:
            lyric_text_tail = lyric_drop_head[:o]
            break
        else:
            lyric_text_tail = lyric_drop_head

    '''处理中间段'''
    # 处理掉空列表
    if '\n' in lyric_text_tail:
        while '\n' in lyric_text_tail:
            lyric_text_tail.remove('\n')
    # 处理掉演唱者及冒号的行列
    del_list = []
    for a in lyric_text_tail:
        if '：' in a:
            del_list.append(a)
        elif ':' in a:
            del_list.append(a)
    lyric_text_tail = list(set(lyric_text_tail) - set(del_list))
    # 处理掉换行符、特殊符号, 并分行
    lyric_text = []
    re_text = r'（[\u4E00-\u9FA5\w\s]+）|\([\u4E00-\u9FA5\w\s]+\)|（[\u4E00-\u9FA5\w\s]+\)|\([\u4E00-\u9FA5\w\s]+）'
    re_brackets = re.compile(re_text)
    for i in lyric_text_tail:
        i = i.replace('\n', '')
        j = re.sub(re_brackets, '《', i)
        # while '' in j:
        #     j.remove('')
        j = ''.join(itertools.chain(j))
        if '《' in j:
            j = j.replace('《', '').replace('》', '')
        if '”' in j:
            j = j.replace('“', '').replace('”', '')
        lyric_text.append(j)
    #设置分词动态字典
    cut_dict = ('飙翻', 'A等货')
    for cut in cut_dict:
        jieba.add_word(cut, freq=100)
    # 分词写入文件
    for words_cut in lyric_text:
        words = list(jieba.cut(words_cut, cut_all=False))
        if words != []:
            with open('rhyme_word.txt', 'a', encoding='UTF-8') as f:
                f.write(words[-1] + ',')
    print(f_name + '写入完成')


def word_cloud():
    f = open('rhyme_word.txt', 'r', encoding='UTF-8').read()
    # f = [i for i in f if i != ' ']
    wordcloud = WordCloud(background_color='white',
                          width=800,
                          height=600,
                          margin=2,
                          font_path='simsun.ttc')
    wordcloud.generate(f)
    wordcloud.to_file('rhyme_word.png')
# for f_name in os.listdir('./lyrics'):
#     get_rhyme(f_name)
word_cloud()