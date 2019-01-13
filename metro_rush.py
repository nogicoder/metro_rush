#!/usr/bin/env python3
from metro import *
from PathFinder import *


class Turn:

    def __init__(self, idx, stations, metro):
        self.name = 'turn' + str(idx)
        self.idx = idx
        self.stations = stations
    
    def __str__(self):
        return self.name
    
    __repr__ = __str__

def move_it(metro, converted_path):
    for idx, train in metro.trains.items():
        for i in range(1, len(converted_path)):
            station_1 = converted_path[i - 1]
            station_2 = converted_path[i]
            move = MoveTrain(train, station_1, station_2)
            move.execute()
            break
        break


def run_it(metro):
    counter = 0
    while len(metro.stop.trains) != len(metro.trains):
        turns = []
        counter += 1
        occupied_station = []
        for idx, line in metro.lines.items():
            for station in line._stationtoidx:
                    if station.trains:
                        occupied_station.append(station)
        turn = Turn(counter, occupied_station, metro)
        turns.append(turn)
        break
    return turns


def main():
    metro = Metro('Delhi')
    metro.build_graph('delhi')
    path, cost = PathFinding(metro).path, PathFinding(metro).cost
    converted_path = PathFinding(metro).converted_path
    station_list = []
    for station, line in converted_path:
        station_list.append(station)
    move_it(metro, station_list)
    run_it(metro)


main()
