# Installer la librairie SpaCy
# pip install spacy OU pip3 install spacy

# Télécharger les modèles français.
# python3 -m spacy download fr_core_news_sm

import csv

import numpy as np
import spacy
from nltk.corpus import stopwords

from sklearn.utils import Bunch
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import os
from os.path import isfile, join, dirname, realpath
import pandas as pd

from os import listdir
import re


class Nlp:
    spacy_french_model = spacy.load("fr_core_news_sm")

    count_vector = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    clf = MultinomialNB()
    label_classes = []

    def call_me(self):
        text = self.read_from_file()
        return self.launch_nlp(text)

    def read_from_file(self):
        file = open('command.txt')
        text = file.read()
        file.close()
        return text

    def get_station(self):
        file = open('dataset/timetables.csv')
        csvreader = csv.reader(file, delimiter='\t')
        next(csvreader)
        rows = []
        for row in csvreader:
            trajet = row[1].split(" - ")

            if not trajet[0].startswith("Gare de"):
                trajet[0] = "Gare de " + trajet[0]
            if not trajet[1].startswith("Gare de"):
                trajet[1] = "Gare de " + trajet[1]

            departure = trajet[0].split("Gare de ")[1]
            destination = trajet[1].split("Gare de ")[1]

            rows.append(departure)
            rows.append(destination)

        return list(set(rows))

    def train_from_loc(self, sentence):
        data_test = pd.read_csv(open('third_built_dataset.csv'), sep=',')
        data = pd.read_csv(open('built_dataset.csv'), sep=',')

        # print(data['sentence'])
        # print(data['sentence_type'])

        train_counts = self.count_vector.fit_transform(data['sentence'])
        train_tfidf = self.tfidf_transformer.fit_transform(train_counts)
        self.clf.fit(train_tfidf, data['sentence_type'])

        # print(self.count_vector.get_feature_names_out())

        train_tfidf_test = self.count_vector.transform(data_test['sentence'])
        print("Accuracy score : ", self.clf.score(train_tfidf_test, data_test['sentence_type']))

        simple_test = [sentence]
        simple_test_dtm = self.count_vector.transform(simple_test)
        simple_test_dtm.toarray()

        return self.clf.predict(simple_test_dtm)

    def launch_nlp(self, text):

        print("Command received : " + text)

        # Reconnaissance d’entités nommées (NER)
        spacyText = self.spacy_french_model(text)
        location = []

        # Récupération des gares existantes
        stations = self.get_station()

        # déterminer via une IA si c'est départ/arriver ou bien arriver/départ
        predicted = self.train_from_loc(text)
        print("result : ", predicted[0])

        stopWords = set(stopwords.words('french'))
        clean_words = []
        for token in [X.text for X in spacyText]:
            if token not in stopWords:
                clean_words.append(token)

        for word in clean_words:
            text = self.spacy_french_model(word)
            for ent in text.ents:
                if ent.label_ == 'LOC':
                    location.append(ent.text)

        if len(location) < 2:
            return [], []

        # récupére la bonne gare en fonction de la ville
        first = []
        second = []
        for station in stations:
            if location[0] in station and (
                    location[0] == station or (location[0] + "-") in station or (location[0] + ".") in station or (
                    location[0] + " ") in station):
                first.append(station)

            if location[1] in station and (
                    location[1] == station or (location[1] + "-") in station or (location[1] + ".") in station or (
                    location[1] + " ") in station):
                second.append(station)

        if predicted[0] == 'from_to':
            departure = first
            destination = second
        else:
            departure = second
            destination = first

        return departure, destination
