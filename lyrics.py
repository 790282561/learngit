import requests
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import random
from concurrent.futures.thread import ThreadPoolExecutor
import time
import os

# 爬取目标url为 https://music.163.com/#/playlist?id=2844653116
# 但是还是应该先考虑分析单个歌曲的页面状况

lyrics_url = 'https://music.163.com/playlist?id=2844653116'
headers = {
    'cookie': 'iuqxldmzr_=32; _ntes_nnid=721b3dbafa146a4bd1db9646fbbb1df7,1569592522996; _ntes_nuid=721b3dbafa146a4bd1db9646fbbb1df7; WM_TID=12sJbsU%2BXn5BRUVFUEMs3MRYeku47cpT; WM_NI=FK2%2FcySR5Kri4xe70KnJjZeMtZDp5VY5dXjYKKHr08Sx60ri68FQijdzbAFu0EuoLDJLqvujOwJ2RnfZAF%2Bk9V15sveUsKAeIlvWrYKFETtBxgQsIwRiUNay0AIKlAerZUw%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed0b46f8ab88e95c17db7eb8fa7d54b828e9aafee7cafaca0b3db749b8ab7aacd2af0fea7c3b92a8695fed0e273918efbacf163f8a8abd8b341ae96a6bbe847b8868c91b85e9bebacb9e95389958893b33491a8fad1f163f6e88ab2ec62a8a6aea2c57ff49bbb90cf508a94bf97f8628da986d3d166a6868fa7aa61fb8affd6f27ea78bbdacc46f8bb4bab8f153899a8bb5f74abcb99f94cc7d92b79bafe473f49f87acef4ba7ae96b6f637e2a3; JSESSIONID-WYYY=X%2FugvjR63SqwT7Ef61B6z1pbcZE8FH7IXqgcsUXQuxTUMi01ZpVWjW0nd9%2FpU0ixbkoZsRnCJm%2Ftoka9A4WZHN9%5C1vMAUnRk9p7hfoaYV9a1lkfY2X%2B181cFY8hjOXyTv13dUFtZ3hcGNxoB24Vr4NznxqS2eWfx0TK1Wx8aXXxu9zpk%3A1569641640968; MUSIC_U=fbd048feb7ef3d8a3dd5c8a7a43b9b0087e980e4843aa76219630fa6d447e032fbbc58cce58988ef6609c51a433f02c17955a739ab43dce1; __remember_me=true; __csrf=595fd8abcb3bf11c05a01571ed127a66; ntes_kaola_ad=1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


# 获取“中国新说唱2019”全部歌单和歌名，并写入music_lists.csv
def get_music_lists(lyrics_url, headers):
    music_list = requests.get(lyrics_url, headers=headers)
    if music_list.status_code == 200:
        soup = BeautifulSoup(music_list.text, 'lxml')
        print(soup.prettify())
        id_lists = soup.select('ul.f-hide > li > a[href]')
        for id_list in id_lists:
            with open('music_lists.csv', 'a', encoding='UTF-8') as f:
                f.write(id_list['href'] + ',')
                f.write(id_list.get_text()[:-7] + ',')


# 提供免费代理proxy列表
def setting_proxies():
    proxies_pool_temp = []
    proxies_pool = []
    proxy_url = 'http://www.89ip.cn/index_1.html'
    re_proxy = re.compile('((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))')
    re_port = re.compile('\d{4,5}')
    user_agent = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    proxy_text = requests.get(proxy_url, headers=user_agent).text
    proxy_soup = BeautifulSoup(proxy_text, 'lxml')
    proxies = proxy_soup.select('tbody > tr > td')
    for i in proxies:
        j = re.search(re_proxy, i.text.replace('\t', '').replace('\n', ''))
        k = re.search(re_port, i.text.replace('\t', '').replace('\n', ''))
        if j != None:
            proxies_pool_temp.append(j.group(0))
        if k != None:
            if k.group(0) != '2019':
                proxies_pool_temp.append(':' + k.group(0))
    for m, n in enumerate(proxies_pool_temp):
        if '.' in n:
            proxy = n + proxies_pool_temp[m + 1]
            proxies_pool.append(proxy)
    return proxies_pool


# 提供需要爬取的歌曲url列表
def read_music_lists():
    f = open('music_lists.csv', encoding='UTF-8')
    data = f.read().split(',')
    f.close()

    music_lists = []
    for num, music_url in enumerate(data):
        if '/song?id=' in music_url:
            music_name = data[num + 1]
            music_lists.append((music_url, music_name))

    return music_lists
    # url_lists = []
    # name_lists = []
    # lists = data.split(',')
    # for i in range(len(lists) - 1):
    #     if i % 2 == 0:
    #         url_lists.append('https://music.163.com' + lists[i])
    #     if i % 2 != 0:
    #         name_lists.append(lists[i])
    # return [url_lists, name_lists]


# 爬取歌词，并保存为相应歌名的txt文件
def get_music_lyrics(url_list):
    one_lyric_url = url_list
    # proxy = proxies_pool[random.randint(0, len(proxies_pool))]
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--proxy-server=http://' + proxy)
    browser = webdriver.Chrome(options=chrome_options)

    time.sleep(1)
    browser.get(one_lyric_url)
    browser.switch_to.frame(browser.find_element_by_id('g_iframe'))


    try:
        target = browser.find_element_by_id('flag_ctrl')
        browser.execute_script('arguments[0].scrollIntoView();', target)
        target.click()  # 对“展开”进行一次点击
    except:
        pass

    music_lyrics_part1 = browser.find_element_by_id('lyric-content').text
    music_comment_count = browser.find_element_by_id('cnt_comment_count').text
    music_name = browser.find_element_by_class_name('f-ff2').text[:-7]
    if music_name == '':
        music_name = browser.find_element_by_class_name('f-ff2').text
    if '/' in music_name:
        music_name = music_name.replace('/', '_')
    try:
        with open('./lyrics/' + music_name + '.txt', 'a', encoding='UTF-8') as f:
            f.write('评论数' + music_comment_count + '\n')
            f.write(music_lyrics_part1)
            print('%s 爬取完成' % music_name)
    except:
        print(music_name + '未爬取')
    time.sleep(2)
    browser.close()


def main():
    # get_music_lists(lyrics_url, headers)
    # proxies_pool = setting_proxies()
    music_lists = read_music_lists()
    for one_music in music_lists:
        if (one_music[1] + '.txt') not in os.listdir('./lyrics'):
            get_music_lyrics('https://music.163.com' + one_music[0])
        else:
            pass
            #print(one_music[1] + ' 这首歌已经爬取过了')


main()
