#!/usr/bin/env python3
from collections import deque, namedtuple
from metro import MoveTrain, SwitchLine


class PathFinding:

    def __init__(self, metro, alt=0):
        self.metro = metro
        self.graph = self.get_graph(metro)
        self.edges = self.make_edges(self.graph, alt)
        self.start = metro.start
        self.stop = metro.stop
        self.lines = metro.lines
        self.path = self.find_shortest_path()

    def get_graph(self, metro):
        nodes = metro.transferpoints.copy()
        edges = []
        if metro.start.name not in nodes:
            nodes[metro.start.name] = metro.start
        if metro.stop.name not in nodes:
            nodes[metro.stop.name] = metro.stop
        for line_name, line in metro.lines.items():
            temp = []
            for station in nodes.values():
                if station in line:
                    temp.append(station)
            temp = sorted(temp,
                          key=lambda station: line.get_station_idx(station))
            for i in range(1, len(temp)):
                weight = abs(line.get_station_idx(temp[i - 1]) -
                             line.get_station_idx(temp[i]))
                edges.append((temp[i - 1], temp[i], weight))
        return edges

    @property
    def nodes(self):
        return set(sum(([start, end] for start, end, _ in self.edges), []))

    def make_edges(self, edges, alt):
        edge_list = []
        if alt == 1:
            temp = ('Kashmere Gate', 'Mandi House', 5)
            for i, item in enumerate(edges):
                if item[0].name == temp[0] and item[1].name == temp[1]:
                    edges[i] = (item[0], item[1], 7)
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

    def find_shortest_path(self):
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

        cost = costs[path[-1]]
        return (path, cost)

    def get_action_list_1(self):
        """
        All train move along single path
        """
        actionlist = []
        path = list(self.path[0])
        switch_turn = []
        start_turn = []

        # iterate through each train
        for train in self.metro.trains.values():
            line = train.line  # current line
            print(start_turn)
            if start_turn:  # if 2nd turn -> increase turn by 1
                turn = start_turn[-1] + 1
            else:  # if start_turn empty -> 1st turn, move the first train only
                turn = 0
            
            # increase counter during Switching line (special case)
            while turn in switch_turn:
                turn += 1
            start_turn.append(turn)

            for station_1, station_2 in zip(path[:-1], path[1:]):
                if station_2 not in line:
                    new_line = list(station_1.lines & station_2.lines)[0]
                    action = SwitchLine(train, line, new_line)
                    try:
                        actionlist[turn].append(action)
                    except IndexError:
                        actionlist.append([action])
                    switch_turn.append(turn)
                    turn += 1
                    line = new_line

                station_1_id = line.get_station_idx(station_1)
                station_2_id = line.get_station_idx(station_2)
                if station_2_id > station_1_id:
                    step = 1
                else:
                    step = -1
                for idx in range(station_1_id, station_2_id, step):
                    while turn in switch_turn:
                        turn += 1
                    action = MoveTrain(train, line[idx], line[idx + step])

                    try:
                        actionlist[turn].append(action)
                    except IndexError:
                        actionlist.append([action])
                    turn += 1

        return actionlist
