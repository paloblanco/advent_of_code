from heapq import heappush,heappop
from collections import deque
from dataclasses import dataclass, field
from typing import Any


INPUT_NAME = r"day12input.txt"
TEST_NAME = r"day12input_test.txt"

@dataclass
class Node:
    height: int
    row: int
    column: int
    heuristic: callable
    next_steps: list['Node'] = field(default_factory=list)
    to_me: 'Node' = None # path taken to me

    @property
    def weight(self):
        return self.heuristic(self.row,self.column)

    def __lt__(self, other):
        return self.weight < other.weight

    def check_and_add_next_step(self, other: 'Node'):
        if self.height + 1 >= other.height:
            self.next_steps.append(other)

    def __str__(self):
        return f"N: {self.row}, {self.column}, {self.height}"

    def __repr__(self):
        return self.__str__()


@dataclass
class PQueue:
    _container: list[Node] = field(default_factory=list)

    def push(self, node: Node):
        heappush(self._container, node)

    def pop(self) -> Node:
        return heappop(self._container)

@dataclass
class Queue:

    _container: deque[Node] = field(default_factory=deque)

    def push(self, node: Node):
        self._container.append(node)

    def pop(self) -> Node:
        return self._container.popleft()


@dataclass
class MapGraph:
    _map: list[list[int]]
    start: tuple[int, int]
    end: tuple[int, int]

    def __post_init__(self):
        self.nodes = []
        heuristic = return_heuristic_calc(self.start, self.end)
        # make map of nodes
        for r,row in enumerate(self._map):
            node_row = []
            for c,height in enumerate(row):
                node_here = Node(height, r, c, heuristic)
                node_row.append(node_here)
            self.nodes.append(node_row)
        # connect nodes
        for r,row in enumerate(self.nodes):
            for c, node in enumerate(row):
                other_nodes = []
                if r > 0: other_nodes.append(self.nodes[r-1][c])
                if r < len(self.nodes) - 1: other_nodes.append(self.nodes[r+1][c])
                if c > 0: other_nodes.append(self.nodes[r][c - 1])
                if c < len(row) - 1: other_nodes.append(self.nodes[r][c + 1])
                for other_node in other_nodes:
                    node.check_and_add_next_step(other_node)

    def print_map(self):
        for row in self._map:
            print(''.join([chr(each) for each in row]))

    def astar(self):
        frontier = Queue()
        explored = []
        self.path = []
        start_node = self.nodes[self.start[0]][self.start[1]]
        explored.append(start_node)
        end_node = self.nodes[self.end[0]][self.end[1]]
        current_node = start_node
        for node in current_node.next_steps:
            frontier.push(node)
            node.to_me = current_node
            explored.append(node)
        while frontier._container:
            current_node = frontier.pop()
            if current_node is end_node:
                print("success")
                return current_node
            else:
                for node in current_node.next_steps:
                    if node in explored: continue
                    frontier.push(node)
                    node.to_me = current_node
                    explored.append(node)
        return None

    def _print_solution(self, last_node: Node):
        empty_map = [['.' for each in self._map[0]] for each in self._map]
        parent = last_node
        empty_map[parent.row][parent.column] = "E"
        parent = parent.to_me
        while parent:
            empty_map[parent.row][parent.column] = "@"
            parent = parent.to_me
        pretty_map = [''.join(row) for row in empty_map]
        for r in pretty_map:
            print(r)

    def solve_problem(self, show=False):
        finish = self.astar()
        if finish:
            parent = finish.to_me
            steps=0
            while parent:
                parent = parent.to_me
                steps+=1
            if show:
                self._print_solution(finish)
            return steps
        else:
            return None


def return_heuristic_calc(start: tuple[int,int],end: tuple[int,int]) -> callable:
    startrow = start[0]
    startcol = start[1]
    endrow = end[0]
    endcol = end[1]
    def heuristic_calc(row,column) -> int:
        manhattan_0 = abs(row - startrow) + abs(column - startcol)
        manhattan_1 = abs(endrow - row) + abs(endcol - column)
        return manhattan_0 + manhattan_1    
    return heuristic_calc


def return_map_from_file(fname=TEST_NAME):
    with open(fname,"r") as map_file:
        map_lines = [each.strip() for each in map_file.readlines()]
    map = []
    for l, line in enumerate(map_lines):
        row = list(line)
        for i in range(len(row)):
            val = row[i]
            if val=="S":
                start = (l,i)
                val='a'
            if val=="E":
                end = (l,i)
                val='z'
            row[i] = ord(val)
        map.append(row)
    return map, start, end




if __name__ == "__main__":
    map_test, start_test, end_test = return_map_from_file()
    mapg_test = MapGraph(map_test,start_test,end_test)
    steps_test = mapg_test.solve_problem(show=True)
    assert steps_test == 31

    map, start, end = return_map_from_file(INPUT_NAME)
    mapg = MapGraph(map,start,end)
    steps = mapg.solve_problem(show=True)
    print(f"Part 1: {steps =}")


