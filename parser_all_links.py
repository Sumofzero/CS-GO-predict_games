import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time
import numpy as np


errors_count = 0
links_count = 0

def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    a_s = soup.find('section', id='matches_s2_loader').find_all('a')
    #print(a_s)
    links = []
    for a in a_s:
        a = a.get('href')
        link = 'https://escorenews.com' + a
        links.append(link)
    return links


def read_csv():
    links = []
    with open('parser_all_teams.txt', 'r') as f:
        for row in f:
            if row != '':
                links.append(row[:-1])
    return links


def write_txt(data):
    with open('parser_all_links.txt', 'a') as f:
        for row in data:
            f.write(row+'\n')


def multi_parse(url):
    global errors_count
    global links_count
    links_count += 8
    print(links_count/1472*100)
    all_links = []
    for i in range(1,21):
        try:
            if i == 1:
                all_links += get_all_links(get_html(url))
            else:
                all_links += get_all_links(get_html(url+f'?s2={i}'))
        except Exception as exp:
            errors_count += 1
            break
    return all_links


def main():
    urls = read_csv()
    #print(len(urls), urls[:-2])
    all_links = []
    start = time.time()

    try:
        with Pool(8) as pool:
            cross = pool.map(multi_parse, urls[:-2])
    finally:
        pool.join()

    for games_links in cross:
        for game_link in games_links:
            all_links.append(game_link)
    write_txt(np.unique(all_links))
    #print(all_links)
    print(len(all_links))
    print('DONE!')
    print((time.time() - start)/60)

    del all_links
    del cross

if __name__ == '__main__':
    main()