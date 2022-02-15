import csv
import json

    # rows.append(row)
# print(rows)
class PathFinder:
    def __init__(self, departure, destination):
        self.departure = departure
        self.destination = destination
        self.parseTimeTable()



    def findFastest(self, trips):
        fastest = {"notFound" : True, "duree": 9999999}
        for trip in self.findEveryTrips():
            if int(trip["duree"]) <= int(fastest["duree"]):
                fastest = trip
                fastest["notFound"] = False
        return fastest

    def findEveryTrips(self):
        trips = self.findDirectTrips() + self.findPossibleEscale()
        return trips
        # return self.findDirectTrips().append(self.findPossibleEscale())

    def findDirectTrips(self):
        return [trip for trip in self.rows if (trip["departure"] == self.departure and trip["destination"] == self.destination)]

    def findDepartureTrips(self):
        return [trip for trip in self.rows if trip["departure"] == self.departure]
        
    def findDestinationTrips(self):
        return [trip for trip in self.rows if trip["destination"] == self.destination]

    def findPossibleEscale(self):
        possibleDeparture =  self.findDepartureTrips()
        possibleDestination = self.findDestinationTrips()

        possibles = []
        for depTrip in possibleDeparture:
            for desTrip in possibleDestination:
                if (depTrip["destination"] == desTrip["departure"]):
                    trip = {
                        "trip_ids": [depTrip["trip_id"], desTrip["trip_id"]],
                        "departure": depTrip["departure"],
                        "escale": depTrip["destination"],
                        "destination": desTrip["destination"],
                        "duree": str(int(desTrip["duree"]) + int(depTrip["duree"]))
                    }
                    possibles.append(trip)

        return possibles
        # return [trip for trip in  if ()]
    
    def parseTimeTable(self):
        file = open('dataset/timetables.csv')
        csvreader = csv.reader(file, delimiter='\t')
        headers = next(csvreader)
        rows = []
        for row in csvreader:
            trajet = row[1].split(" - ")

            if not trajet[0].startswith("Gare de"):
                trajet[0] = "Gare de " + trajet[0]
            if not trajet[1].startswith("Gare de"):
                trajet[1] = "Gare de " + trajet[1]

            departure = trajet[0].split("Gare de ")[1]
            destination = trajet[1].split("Gare de ")[1]

            row = {
                headers[0]: row[0],
                "departure": departure,
                "destination": destination,
                headers[2]: row[2],
            }
            rows.append(row)
        self.rows = rows

    def printJson(self, var, prependText=None):
        print(prependText, json.dumps(var, sort_keys=False, indent=4))
