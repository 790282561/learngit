import requests
import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 爬取目标url为 https://music.163.com/#/playlist?id=2844653116
# 但是还是应该先考虑分析单个歌曲的页面状况

lyrics_url = 'https://music.163.com/playlist?id=2844653116'
headers = {
    'cookie': 'iuqxldmzr_=32; _ntes_nnid=721b3dbafa146a4bd1db9646fbbb1df7,1569592522996; _ntes_nuid=721b3dbafa146a4bd1db9646fbbb1df7; WM_TID=12sJbsU%2BXn5BRUVFUEMs3MRYeku47cpT; WM_NI=FK2%2FcySR5Kri4xe70KnJjZeMtZDp5VY5dXjYKKHr08Sx60ri68FQijdzbAFu0EuoLDJLqvujOwJ2RnfZAF%2Bk9V15sveUsKAeIlvWrYKFETtBxgQsIwRiUNay0AIKlAerZUw%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed0b46f8ab88e95c17db7eb8fa7d54b828e9aafee7cafaca0b3db749b8ab7aacd2af0fea7c3b92a8695fed0e273918efbacf163f8a8abd8b341ae96a6bbe847b8868c91b85e9bebacb9e95389958893b33491a8fad1f163f6e88ab2ec62a8a6aea2c57ff49bbb90cf508a94bf97f8628da986d3d166a6868fa7aa61fb8affd6f27ea78bbdacc46f8bb4bab8f153899a8bb5f74abcb99f94cc7d92b79bafe473f49f87acef4ba7ae96b6f637e2a3; JSESSIONID-WYYY=X%2FugvjR63SqwT7Ef61B6z1pbcZE8FH7IXqgcsUXQuxTUMi01ZpVWjW0nd9%2FpU0ixbkoZsRnCJm%2Ftoka9A4WZHN9%5C1vMAUnRk9p7hfoaYV9a1lkfY2X%2B181cFY8hjOXyTv13dUFtZ3hcGNxoB24Vr4NznxqS2eWfx0TK1Wx8aXXxu9zpk%3A1569641640968; MUSIC_U=fbd048feb7ef3d8a3dd5c8a7a43b9b0087e980e4843aa76219630fa6d447e032fbbc58cce58988ef6609c51a433f02c17955a739ab43dce1; __remember_me=true; __csrf=595fd8abcb3bf11c05a01571ed127a66; ntes_kaola_ad=1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


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


def read_music_lists():
    f = open('music_lists.csv', encoding='UTF-8')
    data = f.read()
    f.close()

    url_lists = []
    name_lists = []
    lists = data.split(',')
    for i in range(len(lists) - 1):
        if i % 2 == 0:
            url_lists.append('https://music.163.com' + lists[i])
        if i % 2 != 0:
            name_lists.append(lists[i])
    return url_lists


def get_music_lyrics():
    one_lyric_url = 'https://music.163.com/song?id=1387615527'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options)

    time.sleep(5)
    browser.get(one_lyric_url)
    browser.switch_to.frame(browser.find_element_by_id('g_iframe'))
    browser.find_element_by_id('flag_ctrl').click()  # 对“展开”进行一次点击

    music_lyrics_part1 = browser.find_element_by_id('lyric-content').text
    music_lyrics_part2 = browser.find_element_by_id('flag_more').text
    music_comment_count = browser.find_element_by_id('cnt_comment_count').text
    music_name = browser.find_element_by_class_name('f-ff2').text[:-7]
    with open(music_name + '.txt', 'a', encoding='UTF-8') as f:
        f.write('评论数' + music_comment_count + '\n')
        f.write(music_lyrics_part1)
        f.write(music_lyrics_part2)


# get_music_lists(lyrics_url, headers)
# read_music_lists()
get_music_lyrics()
