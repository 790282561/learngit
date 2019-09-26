import requests
import lxml
from bs4 import BeautifulSoup

# 爬取目标url为 https://music.163.com/#/playlist?id=2844653116
# 但是还是应该先考虑分析单个歌曲的页面状况

lyrics_url = 'https://music.163.com/playlist?id=2844653116'
headers = {'cookie': '_iuqxldmzr_=32; _ntes_nnid=2b0d4862a2bffcbf73d2e3f19a9d4af1,1569503248034; _ntes_nuid=2b0d4862a2bffcbf73d2e3f19a9d4af1; WM_TID=12sJbsU%2BXn5BRUVFUEMs3MRYeku47cpT; WM_NI=ksXECMQze9oEl9tv2lpvIJoNILKzRG4%2FGv3XGrzAnKhtY9fhqso7MdqFT8WAByFkCdGYiZpcTJkW54idFxi8iFJIrbgS1AXPdAQpVLXsV8ItKqMe%2BEjxhH3lJ9DoGZlZOVM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed5d44e888ac08dd84afcb08bb2c54e869b8bbaf234f2a7a38bcf798b9d8685fb2af0fea7c3b92aa9ad98a6c24793a6abdaee4fb0e7bc97b168b4aa87abee468b94859bd14df8f18997b25485aeb6a2ed41acac97dae564b3ada1d8d070b39a9cd9d64b82a78a8cc2708587a7bbf3699896a5b8b840abbc8a99ec34ab9a86aaf16aa58dffa2db5ca89f9f91d5489cad9ad9cc8089af8386aa4faaa8a8a9b2688ae78c90c652b08681b7d037e2a3; JSESSIONID-WYYY=YVtX8Z%2Bd9PZbGQMIrN8WH5tmuo4y5fN7k5%2F4Pwc9K86R%5C8YY1nZX3XCbBw2K4ErjR4zvPTnek5VcFr3PBgwvDnC6XN0TGvoNnUkPxyTn%2Fxfx59ge%2FSm8R4j%2B8fXN5A76yoqQabYUoqXF6C8OIR8EGVxQymI2sOp%2BhvdNT9jwa8hctkbc%3A1569516533619; __remember_me=true; ntes_kaola_ad=1; MUSIC_U=fbd048feb7ef3d8a3dd5c8a7a43b9b00b65253817a9101f24db293f2b925f7f6c67dc7dc4645b4c1966dea1fea362ec1f2f513a9c38b5dc7; __csrf=4b4a0ead35a76a35dad397e534195606',
           'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
          }


def get_music_lists(lyrics_url, headers):
    music_list = requests.get(lyrics_url, headers=headers)
    if music_list.status_code == 200:
        soup = BeautifulSoup(music_list.text, 'lxml')
        id_lists = soup.select('a.m-sgitem')
        for id_list in id_lists:
            print(id_list['href'])

get_music_lists(lyrics_url, headers)