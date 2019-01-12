from collections import deque, namedtuple


class PathFinding:  # """UPDATE"""

    def __init__(self, metro, alt=0):
        self.edges = self.make_edges(metro.edges, alt)
        self.start = metro.start
        self.stop = metro.stop
        self.path = self.find_shortest_path()

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

        cost = costs[path[-1]]
        return (path, cost)
