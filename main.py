from nlp import Nlp
from voice_recognition import VoiceRecognition
import time
import csv
import random
import os
from dijkstra import Dijkstra


def buildDataset(cities):
    size = len(cities)
    dataset = open('dataset/dataset.csv')
    csvreader = csv.reader(dataset, delimiter=';')
    csv_escales = open('dataset/escales.csv')
    escales = csv.reader(csv_escales, delimiter=';')
    next(csvreader)
    sentences = []
    for row in csvreader:
        sentence = row[0]
        sentence_type = row[1]
        for i in range(50):
            city = cities[random.randrange(0, size, 1)]
            destination = cities[random.randrange(0, size, 1)]
            sentences.append([sentence.replace("first", city).replace("second", destination), sentence_type])
        print(sentence)
        for escale in escales:
            new_sentence_type = sentence_type + '_by'
            new_sentence = sentence + " " + escale[0]
            print(new_sentence)
            for j in range(50):
                city = cities[random.randrange(0, size, 1)]
                destination = cities[random.randrange(0, size, 1)]
                escale_name = cities[random.randrange(0, size, 1)]
                sentences.append(
                    [new_sentence.replace("first", city).replace("second", destination).replace("third", escale_name),
                     new_sentence_type])
        csv_escales.close()
        csv_escales = open('dataset/escales.csv')
        escales = csv.reader(csv_escales, delimiter=';')
    dataset.close()
    with open("second_built_dataset.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["sentence", "sentence_type"])
        csvwriter.writerows(sentences)


def main():
    nlp_IA = Nlp()
    stations = nlp_IA.get_station()
    # buildDataset(stations)
    voice = VoiceRecognition()

    first, second = [], []
    while (len(first) < 1 and len(second) < 1):
        while not os.path.exists("command.txt"):
            voice.call_me()
            time.sleep(2)
        first, second = nlp_IA.call_me()
        print(first, second)
        if (len(first) < 1 and len(second) < 1):
            print("Less than 2 cities found, Please retry\n\n")
            time.sleep(2)

    if len(first) > 1:
        print("\n\nThere is multiple possibilities for departure : ")
        for i, elem in enumerate(first):
            print(i + 1, " - ", elem)
        source_index = int(input("Choose source of the travel : ")) - 1
        source = first[source_index]
    else:
        source = first[0]
    if len(second) > 1:
        print("\n\nThere is multiple possibilities for destination : ")
        for i, elem in enumerate(second):
            print(i + 1, " - ", elem)
        destination_index = int(input("Choose source of the travel : ")) - 1
        destination = second[destination_index]
    else:
        destination = second[0]

    file = open('dataset/timetables.csv')
    csvreader = csv.reader(file, delimiter='\t')
    pf = Dijkstra(stations, csvreader)

    previous_nodes, shortest_path = pf.dijkstra_algorithm(graph=pf, start_node=source)
    pf.print_result(previous_nodes, shortest_path, start_node=source, target_node=destination)

    if os.path.exists("command.txt"):
        os.remove("command.txt")


if __name__ == "__main__":
    main()
