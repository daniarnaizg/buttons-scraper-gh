from bs4 import BeautifulSoup
import requests
import json
import time

BASE_URL = "https://www.myinstants.com/es/index/es/"

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def get_pages(n_pages=3):
    pages = []
    for i in range(1, n_pages + 1):
        pages.append(BASE_URL + f'?page={str(i)}')
    return pages


def get_instants(content):
    url_list = []
    soup = BeautifulSoup(content, 'html.parser')
    instants = soup.find_all(class_="small-button")
    print(f'[INFO] {len(instants)} found')
    for item in instants:
        sound_title = str(item['title'].split(
            'Reproduce el sonido de ')[1].strip())
        media_url = str(item['onclick']).split('\'')[1].strip()
        url_list.append(
            {'url': f'https://www.myinstants.com{media_url}', 'title': sound_title})
    return url_list


# main
if __name__ == '__main__':
    pages = get_pages()

    final_dict = {}
    final_dict["timestamp"] = str(time.time()).split('.')[0]

    full_list = []
    for page in pages:
        print(f'[INFO] Getting page: {page}')
        content = requests.get(page, headers=HEADERS).content
        instants = get_instants(content)
        full_list = full_list + instants
    final_dict["data"] = full_list

    print(f'[INFO] {len(full_list)} total found')

    print(final_dict)

    # save to json file
    with open('./data/instants.json', 'w', encoding='UTF-8') as f:
        json.dump(final_dict, f)
