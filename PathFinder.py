# to find all flights between cities
import copy
import sqlite3

import itertools


class PathFinder(object):
    cursor = None

    def __init__(self, connection):
        self.cursor = connection.cursor()

    def __findCityAirports(self, fromCity, toCity):
        fromAirportIds = []
        toAirportIds = []

        # find all the airportId of fromCity from database
        for fro in self.cursor.execute(
                "SELECT a.id FROM airports AS a LEFT JOIN cities AS b ON a.cityId=b.id WHERE b.city=?",
                [fromCity]).fetchall():
            fromAirportIds.append(fro[0])
        # find all the airportId of toCity from database
        for to in self.cursor.execute(
                "SELECT a.id FROM airports AS a LEFT JOIN cities AS b ON a.cityId=b.id WHERE b.city=?",
                [toCity]).fetchall():
            toAirportIds.append(to[0])
        print "the", fromCity, "has airports:", fromAirportIds
        print "the", toCity, "has airports:", toAirportIds

        cartesian = []  # Cartesian product
        for x in itertools.product(fromAirportIds, toAirportIds):
            cartesian.append(x)
        print "between", fromCity, "and", toCity, "all start and end is:", cartesian

        return cartesian

    def __findAllPath(self, fromAirportId, toAirportId, temp=[], path=[], result=[]):
        # initial param
        if temp == None or temp == []:
            temp = [fromAirportId]
        if path == None or path == []:
            path = [fromAirportId]

        # next connect airport_id
        reachIds = self.cursor.execute(
            "SELECT to_airport_id from airlines WHERE from_airport_id=? AND to_airport_id NOT IN ({});".format(
                ','.join([str(i) for i in temp])), [fromAirportId]).fetchall()

        # recursion
        for reachId in reachIds:
            innerTemp = copy.copy(temp)
            innerTemp.append(reachId[0])
            innerPath = copy.copy(path)
            innerPath.append(reachId[0])
            if reachId[0] == toAirportId:
                print innerPath
                result.append(innerPath)
                break
            else:
                self.__findAllPath(reachId[0], toAirportId, list(set(innerTemp)), innerPath, result)

    def findAllPathBetweenCities(self, startCity, endCity):
        startEndList = self.__findCityAirports(startCity, endCity)
        result = []

        for startEnd in startEndList:
            print
            print "start from:", startEnd[0], "to:", startEnd[1], "has following paths:"
            self.__findAllPath(startEnd[0], startEnd[1], result=result)
            print

        print "from  ", startCity, "  to  ", endCity, "  has", len(result), "airlines in total"
        print
        self.cursor.close()
        return result


# for test
if __name__ == '__main__':
    startCity = "Salt Lake City"
    endCity = "New York"
    connection = sqlite3.connect("dbFile/Graph.db")
    result = PathFinder(connection).findAllPathBetweenCities(startCity, endCity)
    print result
