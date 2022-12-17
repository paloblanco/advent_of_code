from dataclasses import dataclass,field
from collections import deque
from typing import Union

TEST_NAME = "day16input_test.txt"
INPUT_NAME = "day16input.txt"

"""
This one sounds hard. Need to take some notes.

Assume that the best path will move from non0 valve to the next, 
stopping when time is up or every valve is turned.

We can reduce the size of the graph to only non0 nodes ( + the start),
where each edge has a length of the shortest distance between the two.
Doing this will make a brute force search more feasible. Test problem only has 
6 nodes then, full is ~ 15.

Steps:
1. read in data, build raw graph
2. create reduced graph with weighted edges
3. brute force for maximum
    - adjustment here: there is a logical "next best move", try these first.
"""

@dataclass
class Queue:
    
    def __init__(self,start=None):
        if start:
            self._container = deque(start)
        else:
            self._container = deque()

    def push(self, val: Union[int,list]):
        self._container.append(val)

    def pop(self) -> Union[int,list]:
        return self._container.popleft()

    @property
    def empty(self) -> bool:
        return not self._container

    def __str__(self) -> str:
        return f"{self._container}"

    def __repr__(self) -> str:
        return self.__str__()

@dataclass
class Node:
    name: str
    value: int
    neighbors: dict[str,list[int,'Node']] = field(default_factory=dict)

    def add_neighbor(self,other: 'Node', distance: int = 1) -> None:
        self.neighbors[other.name] = [other, distance]

    def __str__(self):
        return f"{self.name}: v={self.value}   n={[(k,v[1]) for k,v in self.neighbors.items()]}"

    def __repr__(self):
        return self.__str__()


@dataclass
class Graph:
    raw: list[list[str,int,list[str]]]
    nodes: dict[str,Node] = field(default_factory=dict)
    nodes_reduced: dict[str,Node] = field(default_factory=dict)

    def __post_init__(self):
        for each in self.raw:
            node = Node(each[0],each[1])
            self.nodes[node.name] = node
        for each in self.raw:
            for neighbor in each[2]:
                self.nodes[each[0]].add_neighbor(self.nodes[neighbor],1)

    def get_times_to_nodes(self, name, all_names):
        frontier = Queue()
        current_node = self.nodes[name]
        explored = dict()
        # distances = dict()
        for n,dd in current_node.neighbors.values():
            frontier.push([n,dd]) # second number is distance
        while not frontier.empty:
            current_node,current_distance = frontier.pop()
            current_name = current_node.name
            if current_name not in explored or current_distance < explored[current_name]:
                for n,_ in current_node.neighbors.values():
                    frontier.push([n,1+current_distance]) # second number is distance
                explored[current_name] = current_distance
        distances = {name_neighbor:distance for name_neighbor,distance in explored.items() if ((name_neighbor in all_names) and (name_neighbor != name))}
        return distances

    def reduce_graph(self):
        nonzero_names = [self.raw[0][0],]
        for n in self.nodes.values():
            if n.value > 0: nonzero_names.append(n.name)
        for name in nonzero_names:
            oldnode = self.nodes[name]
            newnode = Node(oldnode.name,oldnode.value)
            self.nodes_reduced[name] = newnode
        for name in nonzero_names:
            print(f"============{name}===========")
            travel_times = self.get_times_to_nodes(name, nonzero_names)
            print(travel_times)
            for newname,dist in travel_times.items():
                self.nodes_reduced[name].add_neighbor(self.nodes_reduced[newname],dist)

    def printme_reduced(self):
        for i,v in self.nodes_reduced.items():
            print(f"{str(v)}")
    
    def printme(self):
        for i,v in self.nodes.items():
            print(f"{str(v)}")


def read_data(fname=TEST_NAME):
    node_list = []
    with open(fname) as input_file:
        for line in input_file:
            line = line.strip().split(' ')
            name = line[1]
            value = int(line[4][5:-1])
            neighbors = [each.replace(',','') for each in line[9:]]
            node_list.append([name,value,neighbors])
    return node_list

def part1(fname=TEST_NAME):
    node_data = read_data(fname)
    graph0 = Graph(node_data)
    # graph0.printme()
    graph0.reduce_graph()
    graph0.printme_reduced()
    # todo: reduce graph0
    # todo: exhaustively search reduced graph
    

if __name__ == "__main__":
    part1()






