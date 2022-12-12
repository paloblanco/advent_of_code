from heapq import heappush,heappop
from collections import deque
from dataclasses import dataclass, field

import pyxel

INPUT_NAME = r"day12input.txt"
TEST_NAME = r"day12input_test.txt"

def init_pyxel():
    pyxel.init(200, 128, title="AdventOfCode, Day12", fps=60, capture_scale=3, capture_sec=60)
    pyxel.load("my_resource.pyxres")
    pyxel.cls(0)
    # draw_background()
    pyxel.colors.from_list([0x000000,
        0x0f1417,
        0x1c2023,
        0x282d30,
        0x363a3e,
        0x43484b,
        0x51565a,
        0x606568,
        0x6f7478,
        0x7e8387,
        0x8e9397,
        0x9da3a7,
        0xaeb3b7,
        0xbec4c8,
        0xcfd5d9,
        0xf1f11f,
        ])
    pyxel.flip()

def draw_background():
    pyxel.cls(0)
    pyxel.bltm(0,0,0,0,0,128,128,0)
    pyxel.text(40,16,"AoC Day 12", 1)
    pyxel.text(5,120,"NormGear -- CRT matrix display", 5)

    # pyxel.colors[0] = 0x000000
    # pyxel.colors[1] = 0x0f1417
    # pyxel.colors[2] = 0x1c2023
    # pyxel.colors[3] = 0x282d30
    # pyxel.colors[4] = 0x363a3e
    # pyxel.colors[5] = 0x43484b
    # pyxel.colors[6] = 0x51565a
    # pyxel.colors[7] = 0x606568
    # pyxel.colors[8] = 0x6f7478
    # pyxel.colors[9] = 0x7e8387
    # pyxel.colors[10] = 0x8e9397
    # pyxel.colors[11] = 0x9da3a7
    # pyxel.colors[12] = 0xaeb3b7
    # pyxel.colors[13] = 0xbec4c8
    # pyxel.colors[14] = 0xcfd5d9
    # pyxel.colors[15] = 0xf1f11f

def refresh(map,list_highlight,c=15,count=1, text = "Drawing A* Exploration Bound"):
    # draw_background()
    pyxel.rect(70,16,80,30,0)
    pyxel.text(70,16,"AoC Day 12", 14)
    pyxel.text(40,26,text, 15)
    colors = [0,1,2,5,3,13,11,15]
    startx=30
    starty=40
    h=len(map)
    w=len(map[0])
    pyxel.rectb(startx-1,starty-1,2*w+2,2*h+2,7)
    for r,row in enumerate(map):
        for col,val in enumerate(row):
            pyxel.rect(startx+col*2,starty+r*2,2,2,int((val-97)*8/15.1))
    for x,y in list_highlight:
        pyxel.rect(startx+x*2,starty+y*2,2,2,c)
    for i in range(count): pyxel.flip()

@dataclass
class Node:
    height: int
    row: int
    column: int
    heuristic: callable
    next_steps: list['Node'] = field(default_factory=list)
    to_me: 'Node' = None # path taken to me
    steps_to_me: int = 0

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
        self.heuristic = return_heuristic_calc(self.end)

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
            possible_steps.append(self.make_node_from_map(r-1,c))
        if r < len(self._map)-1 and self._map[r+1][c] <= current_node.height + 1:
            possible_steps.append(self.make_node_from_map(r+1,c))
        if c > 0 and self._map[r][c-1] <= current_node.height + 1:
            possible_steps.append(self.make_node_from_map(r,c-1))
        if c < len(self._map[0])-1 and self._map[r][c+1] <= current_node.height + 1:
            possible_steps.append(self.make_node_from_map(r,c+1))
        for n in possible_steps:
            n.steps_to_me = current_node.steps_to_me + 1
        return possible_steps
    
    def astar(self):
        frontier = PQueue()
        explored = dict()
        self.path = []
        start_node = self.make_node_from_map(self.start[0],self.start[1])#self.nodes[self.start[0]][self.start[1]]
        explored[start_node.index] = start_node.steps_to_me
        current_node = start_node
        for node in self.get_next_steps(current_node):
            frontier.push(node)
            node.to_me = current_node
            explored[node.index] = node.steps_to_me
        if DRAW: refresh(self._map,[],7,count=20)
        while frontier._container:
            if DRAW: 
                draw_list = [(each.column, each.row) for each in frontier._container]
                refresh(self._map,draw_list,c=15)
            current_node = frontier.pop()
            if current_node.index == self.end:
                return current_node
            else:
                for node in self.get_next_steps(current_node):
                    if node.index not in explored or explored[node.index] > node.steps_to_me:
                        frontier.push(node)
                        node.to_me = current_node
                        explored[node.index] = node.steps_to_me
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
            path=[]
            path.append((parent.column,parent.row))
            if DRAW: refresh(self._map,path,c=15, count=20, text="Drawing optimal Solution")
            while parent:
                if DRAW:
                    refresh(self._map,path,c=15, text="Drawing optimal Solution")
                parent = parent.to_me
                steps+=1
                if parent: path.append((parent.column,parent.row))
            if show:
                self._print_solution(finish)
            if DRAW: pyxel.show()
            return steps
        else:
            return None


def return_heuristic_calc(end: tuple[int,int]) -> callable:
    endrow = end[0]
    endcol = end[1]
    def heuristic_calc(row,column,steps) -> int:
        manhattan_1 = abs(endrow - row) + abs(endcol - column)
        return steps + manhattan_1    
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
    # assert part_1() == 31

    DRAW = True
    if DRAW:
        init_pyxel()
    steps_1 = part_1(INPUT_NAME)
    print(f"{steps_1 =}")

    # part2test = part_2()
    # assert part2test == 29

    # steps_2 = part_2(INPUT_NAME)
    # print(f"{steps_2 =}")

    


