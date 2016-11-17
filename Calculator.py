import sqlite3
import PathFinder
import copy
from Entities import FligthPath


# to calculate the time spend between all paths

def createEntity(cursor, path):
    timeCosting = 0.0
    for x in range(len(path)):
        if x == 0:  # the first flight calculate specially
            fromDepartTime = cursor.execute("select depart from flights where id=?", [path[x]]).fetchall()[0][0]
            fromArrivalTime = cursor.execute("select arrival from flights where id=?", [path[x]]).fetchall()[0][0]
            timeCosting += fromArrivalTime - fromDepartTime
        else:  # if the next flight will go in a half hour you must wait for tomorrow
            fromArrivalTime = cursor.execute("select arrival from flights where id=?", [path[x - 1]]).fetchall()[0][0]
            toDepartTime = cursor.execute("select depart from flights where id=?", [path[x]]).fetchall()[0][0]
            toArrivalTime = cursor.execute("select arrival from flights where id=?", [path[x]]).fetchall()[0][0]
            if toDepartTime - fromArrivalTime > 0.5:
                timeCosting += toDepartTime - fromArrivalTime
            elif toDepartTime - fromArrivalTime <= 0.5:
                timeCosting += toDepartTime - fromArrivalTime + 24.0
            timeCosting += toArrivalTime - toDepartTime
    return FligthPath(path=path, timeCosting=timeCosting)


def convertToAirlineId(cursor, allPath):
    pathlineList = []
    for path in allPath:
        pathline = []
        for i in range(len(path) - 1):
            pathline.append(cursor.execute("select id from airlines where from_airport_id=? and to_airport_id=?",
                                           [path[i], path[i + 1]]).fetchall()[0][0])
        pathlineList.append(pathline)
    cursor.close()
    return pathlineList


def allFlightCartesianProd(cursor, pathlineList):
    result = []
    for pathline in pathlineList:
        cartesian = []
        for x in range(len(pathline)):
            if x == 0:
                for res in cursor.execute("select id from flights where airlineId=?", [pathline[x]]):
                    cartesian.append([res[0]])
            else:
                allFlights = []
                for res in cursor.execute("select id from flights where airlineId=?", [pathline[x]]):
                    allFlights.append(res[0])
                fuck = []
                for flightId in allFlights:
                    for car in cartesian:
                        temp = copy.copy(car)
                        temp.append(flightId)
                        fuck.append(temp)
                cartesian = fuck
        result.extend(cartesian)
    print len(result), "ways of flights you can choose in total"
    print
    return result


def printDetail(cursor, flightEntity):
    flights = []
    for id in flightEntity.path:
        numberAndOperator = cursor.execute("select flightNumber,operator from flights where id=?", [id]).fetchall()[0]
        flights.append(numberAndOperator[1] + ":" + numberAndOperator[0])
    print "cost", flightEntity.timeCosting, "hours", flights


if __name__ == '__main__':
    startCity = "Salt Lake City"
    endCity = "New York"
    connection = sqlite3.connect("dbFile/Graph.db")
    # airport paths
    allPath = PathFinder.PathFinder(connection).findAllPathBetweenCities(startCity, endCity)
    # airline paths
    pathlineList = convertToAirlineId(connection.cursor(), allPath)
    # fligth paths
    flightList = allFlightCartesianProd(connection.cursor(), pathlineList)
    # create flight entity
    flightPathEntities = []
    for flightPath in flightList:
        flightPathEntities.append(createEntity(connection.cursor(), flightPath))
    # sort by time costing
    print "all the sorted lines is:"
    sortedResult = sorted(flightPathEntities, key=lambda entity: entity.timeCosting)
    for flightEntity in sortedResult:
        printDetail(connection.cursor(), flightEntity)

    print
    print
    print "the costless flight plan is:"
    printDetail(connection.cursor(), sortedResult[0])
    print
    print "done!"
