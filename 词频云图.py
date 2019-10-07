import itertools
import os
import re

import jieba
import wordcloud


def get_rhyme(f_name):
    f = open('./lyrics/' + f_name, 'r', encoding='UTF-8')
    print(f_name + '写入开始')
    text = f.readlines()
    f.close()

    # 处理开头
    for m, n in enumerate(text):
        if '编曲：' in n:
            lyric_drop_head = text[m + 1:]
        elif '评论数' in n:
            lyric_drop_head = text[m + 1:]

    # 处理结尾
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

    # 处理中间段
    lyric_text = []
    re_text = r'（[\u4E00-\u9FA5\w]+）|\([\u4E00-\u9FA5\w]+\)|（[\u4E00-\u9FA5\w]+\)'
    re_brackets = re.compile(re_text)
    if '\n' in lyric_text_tail:
        while '\n' in lyric_text_tail:
            lyric_text_tail.remove('\n')
    for i in lyric_text_tail:
        i = i.replace('\n', '')
        j = re.split(re_brackets, i)
        while '' in j:
            j.remove('')
        j = ''.join(itertools.chain(j))
        for k in j.split(' '):
            lyric_text.append(k)
    for x1, x2 in enumerate(lyric_text):
        if '：' in x2:
            del lyric_text[x1]

    # 分词写入文件
    for words_cut in lyric_text:
        words = list(jieba.cut(words_cut, cut_all=False))
        if words != []:
            with open('rhyme_word.txt', 'a', encoding='UTF-8') as f:
                f.write(words[-1] + ',')
    print(f_name + '写入完成')

def word_wind
for f_name in os.listdir('./lyrics'):
    get_rhyme(f_name)