import re
import itertools

import jieba

f = open('./lyrics/TIME.txt', 'r', encoding='UTF-8')
text = f.readlines()

# 处理开头
for m, n in enumerate(text):
    if '编曲：' in n:
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
        pass

# 处理中间段
lyric_text = []
re_text = r'（[\u4E00-\u9FA5\w]+）|\([\u4E00-\u9FA5\w]+\)|（[\u4E00-\u9FA5\w]+\)'
re_brackets = re.compile(re_text)
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
print(lyric_text)

# #分词
# rhyme = []
# for words in lyric_text:
#     word = jieba.cut(words, cut_all=False)
#     print(list(word))