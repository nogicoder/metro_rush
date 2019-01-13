#!/usr/bin/env python3 
from collections import OrderedDict # """UPDATE"""
from sys import stderr


class Station:
    def __init__(self, name, line, max_trains=1):
        self.name = name
        self.lines = {line}
        self.max_trains = max_trains
        self.trains = set()

    def add_train(self, train):
        if len(self.trains) < self.max_trains:
            self.trains.add(train)
        else:
            raise ValueError('The {} station already reach its capacity '
                             'limit {}'.format(self.name,
                                               self.max_trains))

    def remove_train(self, train):
        try:
            self.trains.remove(train)

        except KeyError:
            pass

    def add_line(self, line):
        self.lines.add(line)

    def find_adjacent_nodes(self, line):
        if line not in self.lines:
            raise KeyError('The {} station is not in {}'.format(self.name,
                                                                line.name))

        station_id = line.get_station_idx(self)

        if len(line) == 1:
            return []

        if station_id == 1:
            if len(line) >= 2:
                return [line[station_id + 1]]

        if station_id == len(line):
            return [line[station_id - 1]]

        return [line[station_id - 1], line[station_id + 1]]

    """
    assuming that line name is unique (We will expand duplicated station names
    feature later)
    """

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    __repr__ = __str__


class Train:
    def __init__(self, train_id, line, station_id):
        self.id = train_id
        self.line = line
        self.station = line[station_id]

    def set_station(self, station):
        self.station = station

    def move_station(self, station):
        if station in self.line:
            self.station = station

    def switch_line(self, newline):
        if newline in self.station.lines:
            self.line = newline
        else:
            raise ValueError("{} does not pass through "
                             "station {}".format(self.line, self.station))

    def __str__(self):
        return 'Train #{}: {} station, {}'.format(self.id, self.station, self.line)


class Line:

    def __init__(self, name):
        self.name = name
        self._stationtoidx = OrderedDict()
        self._idxtostation = {}
        self.stations = self._stationtoidx

    def get_station_idx(self, station):
        return self._stationtoidx[station]

    def add_station(self, station):
        if station not in self._stationtoidx:
            next_idx = len(self._stationtoidx) + 1
            self._stationtoidx[station] = next_idx
            self._idxtostation[next_idx] = station

    def print_stations(self):
        for idx, station in self._idxtostation.items():
            print('{}: {}'.format(idx, station))

    def __getitem__(self, idx):
        return self._idxtostation[idx]

    def __contains__(self, station):
        return station in self._stationtoidx

    def __iter__(self):
        return self._stationtoidx

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self._stationtoidx)

    """
    assuming that line name is unique (We will expand duplicated line names
    feature later)
    """

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    __repr__ = __str__


class Metro:

    def __init__(self, name):
        self.name = name
        self.trains = {}
        self.lines = {}
        self.stations = {}
        self.transferpoints = {}
        self.turns = 0
        self.start = None
        self.stop = None
        
    def build_graph(self, filename):
        try:
            line = None
            with open(filename, 'r') as f:
                for row in f:
                    row = row.rstrip()

                    # get name of Line and create a Line instance
                    if row.startswith('#'):
                        line_name = row[1:]
                        if line_name not in self.lines:
                            line = Line(line_name)
                            self.lines[line_name] = line

                        else:
                            line = self.lines[line_name]

                    # get the starting station's line name and id
                    elif row.startswith('START='): # if line start with 'START'
                        s_line, s_id = [arg.strip() for arg in row[6:].split(':')]
                        self.start = self.lines[s_line][int(s_id)]
                        self.start.max_trains = float('inf')

                    # get the ending station's line name and id
                    elif row.startswith('END='):
                        e_line, e_id = [arg.strip() for arg in row[4:].split(':')]
                        self.stop = self.lines[e_line][int(e_id)]
                        self.stop.max_trains = float('inf')

                    # get number of maximum trains
                    elif row.startswith('TRAINS='):
                        num_trains = int(row[7:].strip())

                    # get the station name and create a Station instance
                    elif len(row) != 0:
                        args = [arg.strip() for arg in row.split(':')]

                        # set condition only if id is a number
                        if args[0].isdigit():

                            # set condition only if name is available also
                            if len(args) == 2:
                                station_id, station_name = args
                                station = Station(station_name, line)
                                line.add_station(station)
                                self.stations[station_name] = station

                                # check station id in case the given id in the
                                # file do not obey the indexing rule
                                if line.get_station_idx(station) != int(station_id):
                                    raise ValueError("invalid station id")

                            # in case of transfer point
                            elif len(args) == 4:
                                station_id, station_name, _, line_2_name = args

                                if station_name in self.stations:
                                    station = self.stations[station_name]
                                else:
                                    station = Station(station_name, line)
                                    self.stations[station_name] = station

                                line.add_station(station)

                                # check station id in case the given id in the
                                # file do not obey the indexing rule
                                if line.get_station_idx(station) != int(station_id):
                                    raise ValueError("invalid station id")

                                self.transferpoints[station_name] = station

                                # if line_2 not in list yet -> add to list
                                if line_2_name not in self.lines:
                                    self.lines[line_2_name] = Line(line_2_name)

                                station.add_line(self.lines[line_2_name])

            # Based on max_train number
            for i in range(num_trains):
                new_train = Train(i + 1, self.lines[s_line], int(s_id))
                self.start.add_train(new_train)
                self.trains[i + 1] = new_train

        except (FileNotFoundError, NameError, ValueError):
            stderr.write("Invalid File")

    def update(self, turn):
        """
        Execute all actions in one turn
        :param actionlist: list of actions
        """
        for action in turn:
            # print(action)
            action.execute()
        self.turns += 1

    def print_train_location(self, train_id):
        """
        train_id = -1, print all train
        otherwise, print train by its id
        """
        if train_id != -1:
            trains = [self.trains[train_id]]
        else:
            trains = list(self.trains.values())

        for train in trains:
            train_id = train.id
            line = train.line
            station = train.station
            station_id = line.get_station_idx(station)
            print("{}({}:{})-T{}".format(station.name,
                                         line.name, station_id, train_id))


class SwitchLine:
    def __init__(self, train: Train, line_1: Line, line_2: Line):
        self.train = train
        self.line_1 = line_1
        self.line_2 = line_2

    def execute(self):
        # check pre-conditions
        if not self.train.line == self.line_1:
            raise ValueError("The train number {} not "
                             "at line_1 ({})".format(self.train.id,
                                                     self.line_1.name))

        # update train state
        self.train.switch_line(self.line_2)

    def __str__(self):
        return '[Switch line] train {} from {} to {}'.format(self.train.id,
                                                             self.line_1.name,
                                                             self.line_2.name)


class MoveTrain:

    def __init__(self, train: Train, station_1: Station, station_2: Station):
        self.train = train
        self.station_1 = station_1
        self.station_2 = station_2

    def execute(self):

        # update train state
        self.train.move_station(self.station_2)

        # update station state
        self.station_1.remove_train(self.train)
        self.station_2.add_train(self.train)

    def __str__(self):
        return '[move] train {} from {} to {}'.format(self.train.id,
                                                      self.station_1.name,
                                                      self.station_2.name)
