#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import deque


class TakeArgs:

    def __init__(self):
        args = self.get_args()
        # set attribute
        self.filename = args.filename
        self.algorithm = args.algo
    
    def get_args(self):
        algo_choice = ['1', '2']
        parser = ArgumentParser(description='Solution for Metro Rush')
        parser.add_argument('filename', type=str)
        parser.add_argument('-a', '--algo',
                            metavar='algorithm',
                            nargs='?',
                            const='1',
                            default='1',
                            choices=algo_choice,
                            help="choose from " + str(algo_choice))
        args = parser.parse_args()
        return args


class Line:

    def __init__(self, line_name, stations):

        self.name = line_name
        self.stations = stations

    def __str__(self):
        return self.name

    __repr__ = __str__


class Station:

    def __init__(self, name, line_name1, line_name2=None):
        self.name = name
        self.line_name1 = line_name1
        self.line_name2 = line_name2
    
    def __str__(self):
        return self.name

    __repr__ = __str__


class Graph:
    def __init__(self, filename):
        self.line_list, self.start, self.end, self.train_numbers = self.get_data(filename)
        self.lines = self.build_lines()
        self.node_list = self.build_node_list()

    def get_data(self, filename):

        try:

            with open(filename) as file:

                line_list = []
                stations = {}

                for line in file:

                    if line.startswith('#'):

                        if stations:
                            line_list.append(Line(line_name, stations))
                            stations = {}

                        line_name = line[1:].strip()

                    elif line.split(':', 1)[0].strip().isdigit():

                        if int(line.split(':', 1)[0].strip()) is 1 and stations:
                            print('Invalid file')
                            exit(1)

                        station_id = int(line.split(':', 1)[0].strip())
                        station_name = line.split(':', 1)[1].strip()
                        stations[station_id] = station_name

                    elif line.startswith('START'):
                        starting_line = line.split('=', 1)[1].split(':')[0].strip()
                        starting_station_id = line.split('=', 1)[1].split(':')[1].strip()

                        if starting_station_id.isdigit():
                            start = (starting_line, int(starting_station_id))

                    elif line.startswith('END'):

                        ending_line = line.split('=', 1)[1].split(':')[0].strip()
                        ending_station_id = line.split('=', 1)[1].split(':')[1].strip()

                        if ending_station_id.isdigit():
                            end = (ending_line, int(ending_station_id))

                    elif line.startswith('TRAINS'):
                        train_number = line.split('=', 1)[1].strip()

            return line_list, start, end, int(train_number)

        except Exception:
            print('Invalid file')
            exit(1)
        
        def find_path(self):
            pass

    def build_lines(self):

        lines = {}
        for line in self.line_list:
            nodes = []
            for id, name in line.stations.items():
                if line.name == self.start[0] and id == self.start[1]:
                    nodes.append(Station(name, line.name))
                elif line.name == self.end[0] and id == self.end[1]:
                    nodes.append(Station(name, line.name))
                elif 'Conn' in name and id not in (self.start[0], self.end[0]):
                    nodes.append(
                        Station(name.split(':')[0], line.name, name.split(':')[2]))
            lines[line] = nodes

        return lines

    def calculate_weight(self, nodeA, nodeB):

        weight = float('inf')
        for line in self.line_list:
            if nodeA.line_name1 == line.name and nodeB.line_name1 == line.name:
                for id, name in line.stations.items():
                    if nodeA.name in name:
                        id1 = id
                    elif nodeB.name in name:
                        id2 = id
        weight = abs(id1 - id2)

        return weight

    def build_node_list(self):

        node_list = []
        for line in self.lines:
            weight_list = []
            nodes = self.lines[line]
            for i in range(1, len(nodes)):
                weight = self.calculate_weight(nodes[i - 1], nodes[i])
                temp = sorted((nodes[i].name, nodes[i - 1].name))
                weight_list.append((temp[0], temp[1], weight))
        
            node_list += weight_list

        return node_list


class Edge:
    def __init__(self, start, end, weight=1):
        self.start = start
        self.end = end
        self.weight = weight


class PathFinding(Graph):

    def __init__(self, filename):
        super().__init__(filename)
        edges = self.transform_pair(self.node_list)
        self.edges = [Edge(start, end, weight) for start, end, weight in edges]
        self.source = self.get_station_name(self.start)
        self.dest = self.get_station_name(self.end)
        
    # get the name of the starting and ending station 
    def get_station_name(self, station):
        for line in self.line_list:
            if line.name == station[0]:
                for id, station_name in line.stations.items():
                    if id == station[1]:
                        return station_name

    # get list of nodes
    @property
    def nodes(self):

        result = []
        for edge in self.edges:
            result += [edge.start, edge.end]
        return set(result)

    # add alternative pairs for undirected graph
    def transform_pair(self, edges):

        result = []
        for n1, n2, weight in edges:
            result.append((n1, n2, weight))
            result.append((n2, n1, weight))
        return result

    # remove edge from edge list
    def remove_edge(self, n1, n2):

        node_pairs = [[n1, n2], [n2, n1]]
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    # add edge to edge list
    def add_edge(self, n1, n2, weight):

        self.edges += [Edge(start=n1, end=n2, weight=weight),
                       Edge(start=n2, end=n1, weight=weight)]

    # Find the neighbour of a node
    @property
    def neighbours(self):

        neighbours = {node: set() for node in self.nodes}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.weight))

        return neighbours

    def dijkstra(self):
        
        # get a copy of node list as unvisited list 
        nodes = self.nodes.copy()
        
        # initial value of distance is infinity for all nodes
        distances = {node: float('inf') for node in self.nodes}
        
        # total distance is zero for the starting node
        distances[self.source] = 0
        
        # initial edge of all nodes
        previous_nodes = {node: None for node in self.nodes}

        # run loops until unvisited node list is empty
        while nodes:

            # choose the node with minimum distance
            current_node = min(
                nodes, key=lambda node: distances[node])
            
            # remove the chosen node from unvisited node list
            nodes.remove(current_node)

            # if minimum distance is infinity -> skip  
            if distances[current_node] == float('inf'):
                break

            # Find neighbour of the current node
            # Calculate distance to that neighbour
            for neighbour, weight in self.neighbours[current_node]:
                alternative_route = distances[current_node] + weight

                # set the distance to the neighbour as 
                # the minimum distance from current node to all its neighbours
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route

                    # show way from the current_node to the neighbour node
                    previous_nodes[neighbour] = current_node


        path, current_node = deque(), self.dest

        # get the path 
        while previous_nodes[current_node] is not None:
            path.appendleft(current_node)
            current_node = previous_nodes[current_node]

        # add the end node
        if path:
            path.appendleft(current_node)

        return path


class Algo1:
    def __init__(self, filename):
        path = PathFinding(filename)
        self.shortest_path = path.dijkstra()
    
    def execution(self):
        print(self.shortest_path)


class Algo2(Graph):
    def execution(self):
        pass


class MetroRush:

    def execution(self):

        args = TakeArgs()
        algo = {'1': Algo1, '2': Algo2}
        algorithm = algo[args.algorithm](args.filename)
        algorithm.execution()
        

if __name__ == '__main__':
    metro = MetroRush()
    metro.execution()
