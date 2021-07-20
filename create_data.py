import pandas as pd
import json



def create_DataFrame(data):
    data_pd = pd.DataFrame(columns=['team', 'map_1', 'map_2', 'map_3', 'map_4', 'score_1', 'score_2', 'score_3', 'score_4', 'res'])
    for index in data:
        if isinstance(data[index], dict):
            team = list(data[index].keys())[0]
            maps = []
            scores = []
            for game in data[index][team]:
                maps.append(game)
                scores.append(data[index][team][game])
            res = sum([int(x>0) for x in scores]) - sum([int(x<0) for x in scores])
            if res >= 1:
                res = 1
            elif res < 0:
                res = -1
            else:
                res = 0
            maps += [0]*(4 - len(maps))
            scores += [0] * (4 - len(scores))
            data_pd = data_pd.append({'team': team, 'map_1': maps[0], 'map_2': maps[1], 'map_3': maps[2], 'map_4': maps[3],
                                      'score_1': scores[0], 'score_2': scores[1], 'score_3': scores[2], 'score_4': scores[3],
                                      'res' : res
                                      }, ignore_index=True)

    return  data_pd


def main():
    data_json = read_json()
    data = create_DataFrame(data_json)
    data.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()