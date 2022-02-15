"""
The file contains the class Graph.
Documentation https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
"""
import csv
import sys


class Dijkstra:
    """
    This class will make the implementation of the algorithm more succinct
    """

    def __init__(self, nodes, csv_reader):
        self.nodes = nodes
        my_graph = self.init_graph(nodes, csv_reader)
        self.graph = self.construct_graph(nodes, my_graph)

    def init_graph(self, nodes, csvreader):
        my_graph = {}
        for city in nodes:
            my_graph[city] = {}
        next(csvreader)
        for row in csvreader:
            trajet = row[1].split(" - ")

            if not trajet[0].startswith("Gare de"):
                trajet[0] = "Gare de " + trajet[0]
            if not trajet[1].startswith("Gare de"):
                trajet[1] = "Gare de " + trajet[1]

            departure = trajet[0].split("Gare de ")[1]
            destination = trajet[1].split("Gare de ")[1]
            my_graph[departure][destination] = int(row[2])
        return my_graph

    def get_nodes(self):
        """Returns the nodes of the graph."""
        return self.nodes

    def get_outgoing_edges(self, node):
        """Returns the neighbors of a node."""
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False):
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        """Returns the value of an edge between two nodes."""
        return self.graph[node1][node2]


    def dijkstra_algorithm(self, graph, start_node):
        """
        This method implements the Dijkstra's algorithm.
        :param graph:
        :param start_node:
        :return:
        """

        unvisited_nodes = list(graph.get_nodes())
        shortest_path = {}
        previous_nodes = {}
        # We'll use max_value to initialize the "infinity" value of the unvisited nodes
        max_value = sys.maxsize
        for node in unvisited_nodes:
            shortest_path[node] = max_value
        # However, we initialize the starting node's value with 0
        shortest_path[start_node] = 0

        while unvisited_nodes:
            current_min_node = None
            # Iterate over the nodes and find the one with the lowest value
            for node in unvisited_nodes:
                if current_min_node is None:
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node
            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = graph.get_outgoing_edges(current_min_node)
            for neighbor in neighbors:
                tentative_value = shortest_path[current_min_node] + graph.value(current_min_node,
                                                                                neighbor)
                if tentative_value < shortest_path[neighbor]:
                    shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node
            unvisited_nodes.remove(current_min_node)
        return previous_nodes, shortest_path


    def print_result(self, previous_nodes, shortest_path, start_node, target_node):
        """
        This method prints the result of the algorithm.
        :param previous_nodes:
        :param shortest_path:
        :param start_node:
        :param target_node:
        :return:
        """

        path = []
        node = target_node

        while node != start_node:
            path.append(node)
            node = previous_nodes[node]

        # Add the start node manually
        path.append(start_node)

        print("Meilleur itinéraire avec un temps de : {} minutes.".format(shortest_path[target_node]))
        print(" -> ".join(reversed(path)))


    def construct_graph(self, nodes, init_graph):
        """
        This method makes sure that the graph is symmetrical. In other words, if there's a path from
        node A to B with a value V, there needs to be a path from node B to node A with a value V.
        """
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if not graph[adjacent_node].get(node, False):
                    graph[adjacent_node][node] = value

        return graph