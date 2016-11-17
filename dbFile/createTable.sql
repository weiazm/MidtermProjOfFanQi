drop table if exists airlines;
drop table if exists airports;
drop table if exists cities;
drop table if exists flights;

CREATE TABLE `airlines` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `from_airport_id` INTEGER NOT NULL ,
  `to_airport_id` INTEGER NOT NULL,
  UNIQUE(`from_airport_id`,`to_airport_id`)
);

CREATE TABLE `airports` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `cityId` INTEGER NOT NULL ,
  `airport` varchar(45) NOT NULL ,
  `longitude` decimal(20,4) NOT NULL,
  `latitude` decimal(20,4) NOT NULL,
  `x` decimal(20,12) NOT NULL,
  `y` decimal(20,12) NOT NULL,
  UNIQUE(`airport`,`longitude`,`latitude`)
);

CREATE TABLE `cities` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `city` varchar(45) NOT NULL ,
  `state` varchar(45) NOT NULL,
  UNIQUE(`city`,`state`)
);

CREATE TABLE `flights` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `flightNumber` varchar(45) NOT NULL UNIQUE ,
  `operator` varchar(45) NOT NULL,
  `airlineId` INTEGER NOT NULL ,
  `depart` decimal(20,12) NOT NULL ,
  `arrival` decimal(20,12) NOT NULL,
  UNIQUE (`flightNumber`,`operator`)
);