import requests
from bs4 import BeautifulSoup


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


def write_csv(data):
    with open('parser_links.csv', 'w') as f:
        for row in data:
            f.write(row+'\n')


def main():
    url = 'https://escorenews.com/ru/csgo/team/navi'
    all_links = []
    for i in range(1,31):
        if i == 1:
            all_links += get_all_links(get_html(url))
        else:
            all_links += get_all_links(get_html(url+f'?s2={i}'))
    #print(all_links)
    print(len(all_links))
    write_csv(all_links)
    print('DONE!')

if __name__ == '__main__':
    main()