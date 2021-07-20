import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
from multiprocessing import Pool
import time


links_count = 0


def get_html(url):
    response = requests.get(url)
    return response.text



def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    #score_end = soup.find('main', class_='match-page').find('div', class_='teams-on-live').\
    #    find('div', class_='score').find('span', class_='live ended').text.split(':')
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



def write_txt(row):
    with open('parser_result_all_games.txt', 'a') as f:
        f.write(row[0]+' '+row[1]+' '+row[2]+'\n')


def read_txt():
    links = []
    with open('parser_all_links.txt', 'r') as f:
        for row in f:
            if row != '\n':
                links.append(row[:-1])
    return np.unique(links)



def multi_parse(url):
    stage = None
    res = [None, None]
    #global links_count
    #links_count += 8
    #print(links_count/50511*100)
    try:
        stage = url.split('/')[-2]
        res = get_page_data(get_html(url))
    except Exception as exp:
        print(exp)
    return [stage, res[0], res[1]]


def main():
    urls = read_txt()
    #print(len(urls))

    start = time.time()

    for i in tqdm(range(6,17)):
        result = pd.DataFrame(columns=['stage', 'teams', 'result'])
        try:
            with Pool(8) as pool:
                cross = pool.map(multi_parse, urls[(i-1)*3156 + 1 : i*3156])
        finally:
            pool.join()
        for row in cross:
            result = result.append({'stage': row[0], 'teams': row[1], 'result': row[2]}, ignore_index=True)
        result.to_csv(f'parser_result_all_games/parser_result_all_games_{i}.csv', index=False)
        del result
        del cross
    print("DONE!")
    print(time.time() - start)


if __name__ == '__main__':
    main()