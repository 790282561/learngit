import os

import matplotlib.pyplot as plt
import pandas as pd


def discuss():
    discuss_dict = {}
    for i in os.listdir('./lyrics'):
        with open('./lyrics/' + i, 'r', encoding='UTF-8') as f:
            discuss_dict[i[:-4]] = f.readline()[3:].replace('\n', '')
    discuss_data = pd.Series(discuss_dict)
    discuss_data = pd.to_numeric(discuss_data, errors='coerce').sort_values(ascending=False)
    discuss_data.index.name = '歌名'
    return discuss_data[discuss_data > 10000]


def plot_discuss(data):
    # 显式设置
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.rcParams['figure.figsize'] = (10.0, 8.0)

    fig, ax = plt.subplots(1, 1)
    ax.bar(data.index, data.values, color='r', alpha=0.6, label='评论数')
    ax.set_xticklabels(data.index, rotation=90)
    for x, y in enumerate(data):
        plt.text(x, y, int(y), ha='center', va='bottom')
    plt.xlabel = '歌名'
    plt.ylabel = '评论数'
    plt.title = '中国新说唱2019歌曲评论数10000+的歌曲排名'
    plt.savefig('中国新说唱2019歌曲评论数10000+的歌曲排名.jpg', dpi=600, bbox_inches='tight')
    plt.show()


def main():
    data = discuss()
    plot_discuss(data)


if __name__ == '__main__':
    main()