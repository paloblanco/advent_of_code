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
    def steps_to_me(self):
        steps_here = 0
        parent = self.to_me
        while parent:
            steps_here+=1
            parent=parent.to_me
        return steps_here

    @property
    def index(self):
        return (self.row,self.column)

    @property
    def weight(self):
        return self.heuristic(self.row,self.column, self.steps_to_me)

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
        self.heuristic = return_heuristic_calc(self.start, self.end)
        # make map of nodes
        # for r,row in enumerate(self._map):
        #     node_row = []
        #     for c,height in enumerate(row):
        #         node_here = Node(height, r, c, self.heuristic)
        #         node_row.append(node_here)
        #     self.nodes.append(node_row)
        # # connect nodes
        # for r,row in enumerate(self.nodes):
        #     for c, node in enumerate(row):
        #         other_nodes = []
        #         if r > 0: other_nodes.append(self.nodes[r-1][c])
        #         if r < len(self.nodes) - 1: other_nodes.append(self.nodes[r+1][c])
        #         if c > 0: other_nodes.append(self.nodes[r][c - 1])
        #         if c < len(row) - 1: other_nodes.append(self.nodes[r][c + 1])
        #         for other_node in other_nodes:
        #             node.check_and_add_next_step(other_node)

    def print_map(self):
        for row in self._map:
            print(''.join([chr(each) for each in row]))

    def make_node_from_map(self, row,col):
        height = self._map[row][col]
        return Node(height,row,col,self.heuristic)

    def get_next_steps(self,current_node):
        r,c = current_node.index
        possible_steps = []
        if r > 0 and self._map[r-1][c] <= current_node.height + 1:
            possible_steps.append(Node(self._map[r-1][c],r-1,c,self.heuristic))
        if r < len(self._map)-1 and self._map[r+1][c] <= current_node.height + 1:
            possible_steps.append(Node(self._map[r+1][c],r+1,c,self.heuristic))
        if c > 0 and self._map[r][c-1] <= current_node.height + 1:
            possible_steps.append(Node(self._map[r][c-1],r,c-1,self.heuristic))
        if c < len(self._map[0])-1 and self._map[r][c+1] <= current_node.height + 1:
            possible_steps.append(Node(self._map[r][c+1],r,c+1,self.heuristic))
        return possible_steps
    
    def astar(self):
        frontier = Queue()
        explored = set()
        self.path = []
        start_node = self.make_node_from_map(self.start[0],self.start[1])#self.nodes[self.start[0]][self.start[1]]
        explored.add(start_node.index)
        # end_node = self.nodes[self.end[0]][self.end[1]]
        current_node = start_node
        for node in self.get_next_steps(current_node):
            frontier.push(node)
            node.to_me = current_node
            explored.add(node.index)
        while frontier._container:
            current_node = frontier.pop()
            if current_node.index == self.end:
                return current_node
            else:
                for node in self.get_next_steps(current_node):
                    if node.index in explored: continue
                    frontier.push(node)
                    node.to_me = current_node
                    explored.add(node.index)
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
    def heuristic_calc(row,column,steps) -> int:
        manhattan_0 = abs(row - startrow) + abs(column - startcol)
        manhattan_1 = abs(endrow - row) + abs(endcol - column)
        # return manhattan_0 + manhattan_1    
        return steps #+ manhattan_1    
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

def part_1(fname=TEST_NAME):
    map, start, end = return_map_from_file(fname)
    mapg = MapGraph(map,start,end)
    steps = mapg.solve_problem(show=True)
    return steps

def part_2(fname=TEST_NAME):
    map, _s, end = return_map_from_file(fname)
    possible_starts = []
    for r,row in enumerate(map):
        for c,val in enumerate(row):
            if val==ord('a'):
                possible_starts.append((r,c))
    solutions = []
    for start in possible_starts:
        mapg = MapGraph(map,start,end)
        steps = mapg.solve_problem(show=False)
        if steps:
            solutions.append(steps)
    return min(solutions)


if __name__ == "__main__":
    assert part_1() == 31

    steps_1 = part_1(INPUT_NAME)
    print(f"{steps_1 =}")

    # part2test = part_2()
    # assert part2test == 29

    # steps_2 = part_2(INPUT_NAME)
    # print(f"{steps_2 =}")

    


