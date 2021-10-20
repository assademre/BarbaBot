import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import csv
import codecs
import urllib.request
from tensorflow.keras.models import load_model
import os

base_url =os.getenv("base_url")
base_url_currency1 = os.getenv("base_url_currency1")
base_url_currency2 = os.getenv("base_url_currency2")

ERROR_THRESHOLD = 0.25
RESULT_THRESHOLD = 0.5

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pk1', 'rb'))
classes = pickle.load(open('classses.pk1', 'rb'))
model = load_model('chatbot_model.model')

bot_name = "BarbaBot"


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    global results, currency_list
    currency_list = [words for words in sentence.split(" ") if words in ["eur","try","usd","pln","cad","jpy","gbp","czk","cny","sek"]]
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    print(results)
    if len(results) == 0:
        append_new_intents("improving_intents.json", sentence, sentence, sentence)
        return [{'intent': 'not_understand', 'probability': '0.9999999'}]
    elif results[0][1] < RESULT_THRESHOLD:
        append_new_intents("improving_intents.json", sentence, sentence, sentence)
        return [{'intent': 'not_understand', 'probability': '0.9999999'}]
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
        print(return_list)
    return return_list


def weather_report():
    CSVBytes = urllib.request.urlopen(base_url)
    CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))
    for Row in CSVText:
        FirstRow = Row
    return FirstRow[9][13:-2] + " and it is " + FirstRow[14][5:] + " degree"


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            if result == "weather_report":
                result = weather_report()
            elif result == "currency":
                result = currency(currency_list)
            break
    return result

def append_new_intents(filepath, tag, patterns, responses):
    with open(filepath, 'r') as fp:
        new_intent = json.load(fp)
        new_intent["intents"].append({
            "tag": tag,
            "pattern": [patterns],
            "responses": [responses]
        })

    with open(filepath, 'w') as fp:
        json.dump(new_intent, fp, indent=2)

def currency(cur_list):
    link = base_url_currency1 + f"{cur_list[0]}_{cur_list[1]}" + base_url_currency2
    CSVBytes = urllib.request.urlopen(link)
    CSVText =  csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))
    for Row in CSVText:
        FirstRow = Row
    return "1 " + FirstRow[0][2:5] + " is " + FirstRow[0][11:-1] + " " + FirstRow[0][6:9]
print("START")
# while True:
#     message = input("")
#     ints = predict_class(message.lower())
#     res = get_response(ints, intents)
#     print(res)
