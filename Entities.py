# contains PO entities
import time


class Airline(object):
    def __init__(self, id, from_airport_id, to_airport_id):
        self.id = id
        self.from_airport_id = from_airport_id
        self.to_airport_id = to_airport_id

    id
    from_airport_id = ""
    to_airport_id = ""


class Airport(object):
    def __init__(self, id, cityId, airport, longitude, latitude, x, y):
        self.id = id
        self.cityId = cityId
        self.airport = airport
        self.longitude = longitude
        self.latitude = latitude
        self.x = x
        self.y = y

    id
    cityId = 0
    airport = ""
    longitude = 0.0
    latitude = 0.0
    x = 0.0
    y = 0.0


class City(object):
    def __init__(self, id, city, state):
        self.id = id
        self.city = city
        self.state = state

    id
    city = ""
    state = ""


class Flight(object):
    def __init__(self, id, flightNumber, operator, airlineId, depart, arrival):
        self.id = id
        self.flightNumber = flightNumber
        self.operator = operator
        self.airlineId = airlineId
        self.depart = depart
        self.arrival = arrival

    id
    flightNumber = ""
    operator = ""
    airlineId = 0
    depart = 0.0
    arrival = 0.0


class FligthPath(object):
    def __init__(self, path, timeCosting):
        self.path = path
        self.timeCosting = timeCosting

    path = []
    timeCosting = 0.0
