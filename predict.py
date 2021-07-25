import pandas as pd
import numpy as np
import keras
import json


def load_tokenizer():
    with open('tokens.json', 'r') as f:
      tokens_dict = json.load(f)
    return tokens_dict


def change_data(data, tokens_dict):
  ress = []
  for row in data:
    row = row.split(' ')
    res = []
    for x in row:
      try:
        res.append(tokens_dict[x])
      except Exception as exp:
        res.append(None)
    ress.append(res)
  return np.array(ress)


def encoding(data, tokens_dict):
  res2 = []
  for row in data:
    res1 = []
    for char in row:
      for key in tokens_dict:
        if char == tokens_dict[key]:
          res1.append(key)
    res2.append(' '.join(res1))
  return np.asarray(res2)


def preprocess_data(data_pred, tokens_dict):
    X_pred = change_data(data_pred.X.values, tokens_dict)
    res = []
    for x in X_pred:
        if None not in x:
            res.append(list(x))
    res = np.asarray(res)
    return  res


def show_pred(res, res_encode, embedding_model):
    indexes = []
    res_dict = dict()
    for i, x in enumerate(res):
        x = x.reshape(1, -1)
        y_pred = embedding_model(x).numpy()
        index = int(np.argmax(y_pred, axis=1))
        indexes.append(index)
        if y_pred[0][index] >= 0.6:
            res_dict[res_encode[i]] = str(index) + ' ' + str(y_pred[0][index]) + ' ' + str(y_pred[0])
    return res_dict


def laod_model():
    model = keras.models.load_model('model_cs-go/model_cs-go')
    return model


def write_result(res):
    with open('predict.json', 'w') as f:
        json.dump(res, f, indent=4)


def predict_csv(tokens_dict, model):
    data_pred = pd.read_csv('parser_pred.csv')
    res = preprocess_data(data_pred, tokens_dict)
    res_encode = encoding(res, tokens_dict)
    res_dict = show_pred(res, res_encode, model)
    write_result(res_dict)


def test_pred(tokens_dict, model):
    data_pred = pd.read_csv('parser_test.csv')
    res = preprocess_data(data_pred, tokens_dict)
    res_encode = encoding(res, tokens_dict)
    res_dict = show_pred(res, res_encode, model)
    write_result(res_dict)


def predict_one_game(tokens_dict, model, url):
    stage, teams = url.split('/')
    teams = ' '.join(teams.split('-vs-'))
    X_pred_test = [stage + ' ' + teams]
    X_pred_tokens = change_data(X_pred_test, tokens_dict)
    y_pred = model(X_pred_tokens).numpy()[0]
    index = np.argmax(y_pred, axis=0)
    print(index, y_pred[index], y_pred)


def main():
    tokens_dict = load_tokenizer()
    model = laod_model()
    choise = 1
    if choise == 0:  #pred about futures
        predict_csv(tokens_dict, model)
    elif choise == 1:   #one pred
        url = 'online-stage/young-ninjas-vs-furia-academy'
        predict_one_game(tokens_dict, model, url)
    elif choise == 2:   #predict from page
        test_pred(tokens_dict, model)


if __name__ == '__main__':
    main()