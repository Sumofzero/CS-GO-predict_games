import numpy as np

def read_csv():
    links = []
    with open('parser_all_links.txt', 'r') as f:
        for row in f:
            if row != '':
                links.append(row[:-1])
    return links


def get_teams(urls):
    teams = []
    for url in urls:
        url = url.split('-vs-')
        if len(url) == 2:
            url1, url2 = url
            n = ''
            while n != '-':
                n = url2[-1]
                url2 = url2[:-1]
            url1 = url1.split('/')[-1]
            teams.append(url1)
            teams.append(url2)
    return np.unique(teams)


def get_links(url, teams):
    links = []
    for team in teams:
        links.append(url+team)
    return links


def write_csv(links):
    with open('parser_all_teams.txt', 'a') as f:
        for link in links:
            f.write(link+'\n')


def main():
    url = 'https://escorenews.com/ru/csgo/team/'
    urls = read_csv()
    teams = get_teams(urls)
    #print(teams)
    #print(len(teams))
    links = get_links(url, teams)
    links.append(url)
    #print(len(links), links[0])
    write_csv(links)

if __name__ == '__main__':
    main()