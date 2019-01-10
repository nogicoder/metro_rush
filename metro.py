#!/usr/bin/env python3 
 
from collections import OrderedDict, deque, namedtuple # """UPDATE"""
from sys import stderr


"""
Modeling system by using GRAPH-PLAN method

Key concepts:
- The system is defined by its environment and states.
- The environment is a set of predefined rules that modeling the system.
- The state of a system is a set of parameters that from it, we can fully
indicate the status / state of the system given its environment.
- There's a predefined action list that will change the system state
- Each action will have a set of pre-condition. An action is only allow to
execute if the current state satisfied the pre-conditions.
"""


# define environment
class Station:
    def __init__(self, name, line, max_trains=1):
        self.name = name
        self.lines = {line} # store as set with 1 item
        self.max_trains = max_trains
        self.trains = set() # store as set with no item yet

    def add_train(self, train):
        if len(self.trains) < self.max_trains:
            self.trains.add(train)
        else:
            raise ValueError('The station already reach its capacity '
                             'limit {}'.format(self.max_trains))

    def remove_train(self, train):
        try:
            self.trains.remove(train)

        except KeyError:
            pass

    def add_line(self, line):
        self.lines.add(line) # add new line to the lines set

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


class PathFinding: # """UPDATE"""

    def __init__(self, edges, start, stop):
        self.edges = self.make_edges(edges)
        self.start = start
        self.stop = stop

    @property
    def nodes(self):
        return set(sum(([start, end] for start, end, _ in self.edges), []))

    def make_edges(self, edges):
        edge_list = []
        Edge = namedtuple('Edge', 'start, end, weight')
        for start, end, weight in edges:
            edge_list.append(Edge(start, end, weight))
            edge_list.append(Edge(end, start, weight))
        return edge_list

    def remove_edge(self, start, end):
        pairs = [[start, end], [end, start]]
        for edge in self.edges:
            if [edge.start, edge.end] in pairs:
                self.edges.remove(edge)

    @property
    def neighbors(self):
        neighbors = {node: set() for node in self.nodes}
        for edge in self.edges:
            neighbors[edge.start].add((edge.end, edge.weight))
        return neighbors

    def find_shortest_path(self):  # """UPDATE"""
        unvisited_nodes = self.nodes.copy()
        costs = {node: float('inf') for node in self.nodes}
        costs[self.start] = 0
        prior_nodes = {node: None for node in self.nodes}

        # Iterate through a list of unvisited nodes
        while unvisited_nodes:

            # choose the next current_node based on node with the lowest cost
            current_node = min(
                unvisited_nodes, key=lambda node: costs[node])

            # remove it from the unvisited node list
            unvisited_nodes.remove(current_node)

            # break if the min cost is infinity
            if costs[current_node] == float('inf'):
                break

            # build a graph of connected nodes
            for neighbor, weight in self.neighbors[current_node]:
                new_cost = costs[current_node] + weight
                if new_cost < costs[neighbor]:

                    # set the cost of the neighbor as the min cost
                    costs[neighbor] = new_cost

                    # set the node prior to the neighbor the node with the min cost
                    prior_nodes[neighbor] = current_node

        path, current_node = deque(), self.stop

        # while there are a connected node to the current node
        while prior_nodes[current_node]:

            # append the ending point first
            path.appendleft(current_node)

            # set the next node to be added as the prior node
            current_node = prior_nodes[current_node]

        # loops break when current_node is the start node (no prior node)
        # append the start node
        if path:
            path.appendleft(current_node)

        return path


class Metro:

    def __init__(self, name):
        self.name = name # name of the Metro System
        self.trains = {} # dict that contain trains
        self.lines = {} # dict that contain lines
        self.stations = {} # dict that contain all stations of a line
        self.transferpoints = {} # dict that contain all the transfer points
        self.turns = 0 # counter for each turn
        self.start = None # starting station
        self.stop = None # ending station

        self.build_graph('delhi')
        self.edges = self.get_edges()
        self.path = PathFinding(self.edges, self.start, self.stop).find_shortest_path()

    def build_graph(self, filename):
        try:
            
            # set initial value for a line
            line = None

            # open the file
            with open(filename, 'r') as f:

                # iterate through each line in file
                for row in f:

                    # strip whitespace to the right
                    row = row.rstrip()

                    # get name of Line and create a Line instance
                    if row.startswith('#'):
                        line_name = row[1:] # get line name
                        if line_name not in self.lines: # if line not added yet
                            line = Line(line_name) # create a Line instance
                            self.lines[line_name] = line # set key/value binding as line_name/ Line object
                        else: # if line already added beforehand (in the case of transfer point below)
                            line = self.lines[line_name] # set line as the previous added Line object 

                    # get the starting station's linename and id   
                    elif row.startswith('START='): # if line start with 'START'
                        s_line, s_id = [arg.strip() for arg in row[6:].split(':')] # get the 1st and 2nd item from the list excluded 'START=' and split at ':'
                        self.start = self.lines[s_line][int(s_id)] # get the Station object based on its id (as the key of the sub-dict)
                        self.start.max_trains = float('inf') # set max_trains of starting station to infinity

                    # get the ending station's linename and id - Same with above block
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
                        if args[0].isdigit(): # set condition only if id is a number
                            if len(args) == 2:  # set condition only if name is available also
                                station_id, station_name = args
                                new_station = Station(station_name, line) # create a Station instance with its Line object
                                line.add_station(new_station) # add the Station object to the Line object
                                self.stations[station_name] = new_station # add the Station object to the stations dict

                                # check station id in case the given id in the file do not obey the indexing rule (skipping or re-index the station)
                                if line.get_station_idx(new_station) != int(station_id):
                                    raise ValueError("invalid station id")


                            elif len(args) == 4: # in case of transfer point
                                station_id, station_name, _, line_2_name = args
                                new_station = Station(station_name, line)
                                line.add_station(new_station)
                                self.stations[station_name] = new_station

                                self.transferpoints[station_name] = new_station # add the station to transferpoints dict

                                # if line_2 not in list yet -> add to list
                                if line_2_name not in self.lines:
                                    self.lines[line_2_name] = Line(line_2_name)

                                # add the Line object represents the 2nd line of the transfer point to the Station object
                                new_station.add_line(self.lines[line_2_name])

            # Based on max_train number
            for i in range(num_trains):
                new_train = Train(i + 1, self.lines[s_line], int(s_id)) # create Train object
                self.start.add_train(new_train) # add trains to the starting station
                self.trains[i + 1] = new_train # add trains to the train dict based on id

        except (FileNotFoundError, NameError, ValueError) as e:
            # print(e)
            stderr.write("Invalid File")

    def get_edges(self):  # """UPDATE"""
        nodes = self.transferpoints.copy()
        edges = []
        if self.start.name not in nodes:
            nodes[self.start.name] = self.start
        if self.stop.name not in nodes:
            nodes[self.stop.name] = self.stop
        for line_name, line_object in self.lines.items():
            temp = []
            for name, station in nodes.items():
                if station in line_object._stationtoidx:
                    temp.append(station)
            temp = sorted(
                temp, key=lambda station: line_object._stationtoidx[station])
            for i in range(1, len(temp)):
                weight = abs(line_object._stationtoidx[temp[i - 1]] -
                             line_object._stationtoidx[temp[i]])
                edges.append((temp[i - 1], temp[i], weight))
        return edges
        
    def update(self, actionlist):
        """
        Execute all actions in one turn
        :param actionlist: list of actions
        """
        for action in actionlist:
            action.execute()
        self.turns += 1


    def print_train_location(self, train_id):
        """
        train_id = -1, print all train
        otherwise, print train by its id
        """
        """
        <station_name>(<line_name>:<station_id>)-<train_label>
        Tagore Garden(Blue Line:18)-T15
        """
        # if train_id != -1:
        #     print(self.trains[train_id])
        # else:
        #     for train in self.trains.values():
        #         print(train)

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


# define action
# Note:
# The pre-conditions checking is partially handled in targeted objects (Train,
# Station, etc.)
# May consider moving all pre-condition checking task to action classes then
# make the associated method in targeted object private. The convention should
# be only using action class to change the environment states.

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
        # check pre-conditions

        # update train state
        self.train.move_station(self.station_2)

        # update station state
        self.station_1.remove_train(self.train)
        self.station_2.add_train(self.train)

    def __str__(self):
        return '[move] train {} from {} to {}'.format(self.train.id,
                                                      self.station_1.name,
                                                      self.station_2.name)


if __name__ == '__main__':
    metro = Metro('Delhi')
    print(metro.path)
