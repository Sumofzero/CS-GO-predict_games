import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pandas as pd


def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    a_s = soup.find('section', id='matches_s2_loader').find_all('a')
    links = []
    for a in a_s:
        a = a.get('href')
        link = 'https://escorenews.com' + a
        links.append(link)
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        results = soup.find('main', class_='match-page').find('div', class_='teams-on-live')
        a_s = results.find_all('a')
        q = []
        for a in a_s:
            q.append(a.get('href').split('/')[-1])
        q = (' '.join(q))
        ended = results.find('span', class_='live ended').text.split(':')
        if ended:
            if int(ended[0]) - int(ended[1]) == 0:
                ended = 0
            else:
                ended = ended.index(max(ended)) + 1
        return [q, ended]
    except Exception as ex:
        print(ex)


def multi_parse(url):
    stage = None
    res = [None, None]
    try:
        stage = url.split('/')[-2]
        res = get_page_data(get_html(url))
    except Exception as exp:
        print(exp)
    return [stage, res[0], res[1]]



def main():
    url = 'https://escorenews.com/ru/csgo/matches'
    all_links = get_all_links(get_html(url))
    result = pd.DataFrame(columns=['stage', 'teams', 'result'])
    #print(all_links)

    try:
        with Pool(8) as pool:
            cross = pool.map(multi_parse, all_links)
    finally:
        pool.join()
    for row in cross:
        result = result.append({'stage': row[0], 'teams': row[1], 'result': row[2]}, ignore_index=True)
    result.to_csv('parser_pred.csv', index=False)

    print('DONE!')

if __name__ == '__main__':
    main()