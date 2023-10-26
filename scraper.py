import requests
import json
import time
from bs4 import BeautifulSoup

BASE_URL = "https://www.myinstants.com"
GLOBAL_EN = "/en/best_of_all_time/us/"
TRENDING_EN = "/en/index/us/"
GLOBAL_ES = "/es/best_of_all_time/es/"
TRENDING_ES = "/es/index/es/"

TIKTOK_EN = "/en/categories/tiktok%20trends/"

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def get_pages(url=BASE_URL, n_pages=3):
    pages = []
    for i in range(1, n_pages + 1):
        pages.append(url + f'?page={str(i)}')
    return pages


def get_instants(content, lang='en'):
    url_list = []
    soup = BeautifulSoup(content, 'html.parser')
    instants = soup.find_all(class_="small-button")
    print(f'[INFO] {len(instants)} found')
    for item in instants:
        if lang == 'en':
            # "Play XXXXXX sound"
            sound_title = str(item['title'].split(
                'Play ')[1].split(' sound')[0])
        elif lang == 'es':
            # "Reproduce el sonido de XXXXXX"
            sound_title = str(item['title'].split(
                'Reproduce el sonido de ')[1].strip())
        media_url = str(item['onclick']).split('\'')[1].strip()
        url_list.append(
            {'url': f'https://www.myinstants.com{media_url}', 'title': sound_title})
    return url_list


def get_content(category, lang='en', n_pages=3):
    pages = get_pages(url=BASE_URL + category, n_pages = n_pages)
    current_list = []
    for page in pages:
        content = requests.get(page, headers=HEADERS).content
        instants = get_instants(content, lang=lang)
        current_list = current_list + instants
    print(f'[INFO] Total {category}: {len(current_list)}')
    return current_list


# main
if __name__ == '__main__':

    ############ GENERAL

    final_dict = {}

    print(f'[INFO] Timestamp: {str(time.time()).split(".")[0]}')
    final_dict["timestamp"] = str(time.time()).split('.')[0]

    print('[INFO] Getting global english')
    final_dict["global_en"] = get_content(GLOBAL_EN, lang='en')

    print('[INFO] Getting trending english')
    final_dict["trending_en"] = get_content(TRENDING_EN, lang='en')

    print('[INFO] Getting global spanish')
    final_dict["global_es"] = get_content(GLOBAL_ES, lang='es')

    print('[INFO] Getting trending spanish')
    final_dict["trending_es"] = get_content(TRENDING_ES, lang='es')

    # save to json file
    with open('./data/instants.json', 'w', encoding='UTF-8') as f:
        json.dump(final_dict, f)

    
    ############ TIKTOK 

    print('[INFO] Getting TikTok')
    tiktok_json = get_content(TIKTOK_EN, lang='en', n_pages=6)

    with open('./data/tiktok.json', 'w', encoding='UTF-8') as f:
        json.dump(tiktok_json, f)


