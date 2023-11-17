import requests
import json
import time
from bs4 import BeautifulSoup

BASE_URL = "https://tokchart.com/"

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def clean_string(string):
    return string.strip().replace('\n', ' ')


def scrape_filters(url):
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='bg-white shadow-xl rounded-xl flex p-4 sm:p-6')

    filters_output = []
    for item in items:
        data_id = item.get('data-id')
        img = item.find('img').get('src')
        title = item.find('h4').text
        title = clean_string(title)
        grow_number = item.find('p').find('span').text
        grow_number = clean_string(grow_number)
        tiktok_url = item.find('div', class_='flex items-center mt-3').find('a').get('href')

        filters_output.append({
            'id': data_id,
            'img': img,
            'title': title,
            'grow_number': grow_number,
            'tiktok_url': tiktok_url
        })

    return filters_output


# main
def scrape_hashtags(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='bg-white shadow-xl rounded-xl p-4 sm:p-6')

    hashtags_output = []
    for item in items:
        data_id = item.get('data-id')
        try:
            img = item.find('img').get('src')
        except:
            img = ''
        title = item.find('div', class_='md:mt-2').text
        title = clean_string(title)
        trending_number = item.find('p').find('span', class_='text-green-600 font-bold text-lg sm:text-2xl').text
        trending_number = clean_string(trending_number)
        tiktok_url = item.find('div', class_='md:mt-2').find('a').get('href')

        hashtags_output.append({
            'id': data_id,
            'img': img,
            'title': title,
            'trending_number': trending_number,
            'tiktok_url': tiktok_url
        })

    return hashtags_output


def scrape_songs(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='flex flex-col col-span-full sm:col-span-6 xl:col-span-4 bg-white rounded-xl')

    # songs_output = []
    for item in items:
        try:
            img = item.find('img').get('src')
            data_id = img.split('/')[-2]
        except:
            img = ''
            # last 6 number of timestamp
            data_id = str(int(time.time() * 1000000))[-6:]

        author = item.find('h3', class_='text-xs md:text-sm font-semibold text-slate-500 uppercase mb-1').find('span').text

        title = item.find('a', class_='text-2xl md:text-4xl font-brico font-bold text-slate-800 mb-1 hover:underline').text
        title = clean_string(title)

        growing_number = item.find('a', class_='border-b-2 border-mimi hover:border-b-3 font-medium text-cadet').text
        growing_number = clean_string(growing_number).split(' ')[0]

        tiktok_url = item.find('a', class_='text-sm flex items-center gap-1 text-slate-600 md:mr-2').get('href')

        songs_output = {
            'id': data_id,
            'img': img,
            'author': author,
            'title': title,
            'growing_number': growing_number,
            'tiktok_url': tiktok_url
        }

    return songs_output


def scrape_country_songs(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='bg-white rounded-xl flex p-4 sm:p-6')

    songs_output = []
    for item in items:
        data_id = item.get('data-id')
        img = item.find('img').get('src')
        author = item.find('div', class_='sm:mt-2').find('span').text
        author = clean_string(author)
        title = item.find('h4').text
        title = clean_string(title)
        tiktok_url = item.find('div', class_='flex items-center mt-3 gap-5').find('a').get('href')

        songs_output.append({
            'id': data_id,
            'img': img,
            'author': author,
            'title': title,
            'tiktok_url': tiktok_url
        })

    return songs_output


if __name__ == '__main__':

    ### FILTERS AND HASHTAGS ###

    # get filters
    filters_url = BASE_URL + 'filters'
    filters_output = scrape_filters(filters_url)

    # get hashtags
    hashtags_url = BASE_URL + 'hashtags'
    hashtags_output = scrape_hashtags(hashtags_url)

    combined_output = {
            'filters': filters_output,
            'hashtags': hashtags_output
        }

    # save combined output
    with open('./data/tokchart.json', 'w', encoding='UTF-8') as f:
        json.dump(combined_output, f, ensure_ascii=False, indent=4)

    ### SONGS ###

    # get global songs
    global_songs_url = BASE_URL
    global_songs_output = scrape_songs(global_songs_url)

    # get growing songs
    growing_songs_url = BASE_URL + 'growing'
    growing_songs_output = scrape_songs(growing_songs_url)

    # get spain songs
    spain_songs_url = BASE_URL + 'trending/ES'
    spain_songs_output = scrape_country_songs(spain_songs_url)

    # get usa songs
    usa_songs_url = BASE_URL + 'trending/US'
    usa_songs_output = scrape_country_songs(usa_songs_url)

    # get uk songs
    uk_songs_url = BASE_URL + 'trending/UK'
    uk_songs_output = scrape_country_songs(uk_songs_url)

    # get brazil songs
    brazil_songs_url = BASE_URL + 'trending/BR'
    brazil_songs_output = scrape_country_songs(brazil_songs_url)

    # get germany songs
    germany_songs_url = BASE_URL + 'trending/DE'
    germany_songs_output = scrape_country_songs(germany_songs_url)

    # get france songs
    france_songs_url = BASE_URL + 'trending/FR'
    france_songs_output = scrape_country_songs(france_songs_url)

    # get mexico songs
    mexico_songs_url = BASE_URL + 'trending/MX'
    mexico_songs_output = scrape_country_songs(mexico_songs_url)

    combined_country_songs_output = {
            'spain': spain_songs_output,
            'usa': usa_songs_output,
            'uk': uk_songs_output,
            'brazil': brazil_songs_output,
            'germany': germany_songs_output,
            'france': france_songs_output,
            'mexico': mexico_songs_output
        }

    combined_songs_output = {
            'global': global_songs_output,
            'growing': growing_songs_output,
            'countries': combined_country_songs_output
        }

    # save combined output
    with open('./data/tokchart_songs.json', 'w', encoding='UTF-8') as f:
        json.dump(combined_songs_output, f, ensure_ascii=False, indent=4)
