from dataclasses import dataclass,field

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
class Node:
    name: str
    value: int
    neighbors: dict[str,list[int,'Node']] = field(default_factory=dict)

    def add_neighbor(self,other: 'Node', distance: int = 1) -> None:
        self.neighbors[other.name] = [distance,other]

    def __str__(self):
        return f"{self.name}: v={self.value}   n={[(k,v[0]) for k,v in self.neighbors.items()]}"

    def __repr__(self):
        return self.__str__()


@dataclass
class Graph:
    raw: list[list[str,int,list[str]]]
    nodes: dict[str,Node] = field(default_factory=dict)

    def __post_init__(self):
        for each in self.raw:
            node = Node(each[0],each[1])
            self.nodes[node.name] = node
        for each in self.raw:
            for neighbor in each[2]:
                self.nodes[each[0]].add_neighbor(self.nodes[neighbor])

    def reduce_graph(self):
        # reduction code here
        pass

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
    graph0.printme()
    # todo: reduce graph0
    # todo: exhaustively search reduced graph
    

if __name__ == "__main__":
    part1()






