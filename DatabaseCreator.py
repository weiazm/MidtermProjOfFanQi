import sqlite3
import xlrd  # this is third party package, need to install.
import Entities
import time

#  to create Graph.db from excel file.

EXCEL_FILE_PATH = "excelFile/RawData_update3.xlsx"
SQLITE3_DB_FILE_PATH = "dbFile/Graph.db"
CREATE_TABLE_SQL_FILE_PATH = "dbFile/createTable.sql"


# to create dbFile from createTable.sql
def createTable(sqlPath, connection):
    try:
        cursor = connection.cursor()
        # read file and execute by line
        for sql in open(sqlPath, "r").read().split(";"):
            cursor.execute(sql)
        cursor.close()
        connection.commit()
    except:
        print "create table failed! please check."
    else:
        print "drop old table and create new table from sql done!"
        print


# to read from excel and insert into db
def readDataAndInsert(excelPath, connection):
    file = xlrd.open_workbook(excelPath)
    airportData = file.sheet_by_name("Airport Data")
    flightData = file.sheet_by_name("Flight Data")

    for i in range(airportData.nrows):
        if i == 0: continue
        __insertCity(connection, airportData.row_values(i))

    for i in range(airportData.nrows):
        if i == 0: continue
        __insertAirport(connection, airportData.row_values(i))

    for i in range(flightData.nrows):
        if i == 0: continue
        __insertAirline(connection, flightData.row_values(i))

    for i in range(flightData.nrows):
        if i == 0: continue
        __insertFlight(connection, flightData.row_values(i))

    print
    print "insert all data done!"
    print


def __insertCity(connection, line):
    try:
        city = Entities.City(None, line[1], line[2])
        cur = connection.cursor()
        cur.execute("insert into cities (id, city , state) VALUES (?,?,?)", [city.id, city.city, city.state])
        cur.close()
    except sqlite3.IntegrityError:
        print "duplicate city find, pass :----------", city.city
        pass
    else:
        connection.commit()
        print "insert city done:   ", city.city


def __insertAirport(connection, line):
    try:
        city = Entities.City(None, line[1], line[2])
        cur = connection.cursor()
        cur.execute("select id from cities WHERE city=? and state=?", [city.city, city.state])
        cityId = cur.fetchall()[0][0]
        airport = Entities.Airport(None, cityId, line[0], line[3], line[4], line[5], line[6])
        cur.execute("insert into airports (id, cityId, airport, longitude, latitude, x, y) VALUES (?,?,?,?,?,?,?)",
                    [airport.id, airport.cityId, airport.airport, airport.longitude, airport.latitude, airport.x,
                     airport.y])
        cur.close()
    except sqlite3.IntegrityError:
        print "duplicate airport find, pass :----------", airport.airport
        pass
    else:
        connection.commit()
        print "insert airport done:   ", airport.airport


def __insertAirline(connection, line):
    try:
        cur = connection.cursor()
        from_airport_id = cur.execute("select id from airports where airport=?", [line[2]]).fetchall()[0][0]
        to_airport_id = cur.execute("select id from airports where airport=?", [line[3]]).fetchall()[0][0]
        airline = Entities.Airline(None, from_airport_id, to_airport_id)
        cur.execute("insert into airlines (id, from_airport_id , to_airport_id) VALUES (?,?,?)",
                    [airline.id, airline.from_airport_id, airline.to_airport_id])
        cur.close()
    except sqlite3.IntegrityError:
        print "duplicate airline find, pass :----------", airline.from_airport_id, airline.to_airport_id
        pass
    else:
        connection.commit()
        print "insert airline done:   ", airline.from_airport_id, airline.to_airport_id


def __insertFlight(connection, line):
    try:
        cur = connection.cursor()
        airlineId = \
            cur.execute("select id from airlines where from_airport_id=(select id from airports where airport=?) " +
                        "and to_airport_id=(select id from airports where airport=?)", [line[2], line[3]]).fetchall()[
                0][0]
        flight = Entities.Flight(None, line[0], line[1], airlineId, line[4], line[5])
        cur.execute("insert into flights (id, flightNumber, operator, airlineId, depart, arrival) VALUES (?,?,?,?,?,?)",
                    [flight.id, flight.flightNumber, flight.operator, flight.airlineId,
                     flight.depart * 25.0 / 12.5 * 12.0, flight.arrival * 25.0 / 12.5 * 12.0])
        # FIXME  here convert excel_decimal into hour_decimal      convert rule: hour_decimal = excel_decimal * 25/12.5*12
        cur.close()
    except sqlite3.IntegrityError:
        print "duplicate flight find, pass :----------", flight.flightNumber
        pass
    else:
        connection.commit()
        print "insert flight done:   ", flight.flightNumber


if __name__ == '__main__':
    # db connection
    connection = sqlite3.connect(SQLITE3_DB_FILE_PATH)
    # read sql file and create database
    createTable(CREATE_TABLE_SQL_FILE_PATH, connection)
    # read excel file and insert data into database
    readDataAndInsert(EXCEL_FILE_PATH, connection)

    connection.close()
