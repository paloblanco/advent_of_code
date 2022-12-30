from heapq import heappush,heappop
from dataclasses import dataclass, field
from collections import deque, defaultdict


TEST_NAME = r"day24input_test.txt"
INPUT_NAME = r"day24input.txt"

DIRECTIONS = [
    [-1,0],
    [1,0],
    [0,-1],
    [0,1]
]

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


class Map:

    def __init__(self,fname=TEST_NAME):
        with open(fname) as f:
            valley = [list(e.strip()) for e in f.readlines()]
        self._map = valley
        self.start = (0,1)
        self.goal = (len(valley[0])-2,len(valley)-1)
        self.width = len(valley[0])
        self.height = len(valley)
        self.storms_left = set()
        self.storms_right = set()
        self.storms_up = set()
        self.storms_down = set()
        for r,row in enumerate(valley):
            for c,val in enumerate(row):
                match val:
                    case "<":
                        self.storms_left.add((c,r))
                    case ">":
                        self.storms_right.add((c,r))
                    case "^":
                        self.storms_up.add((c,r))
                    case "v":
                        self.storms_down.add((c,r))

    def mget(self,x,y,turns=0):
        # return bool if space is available
        if (x,y) == self.start:
            return True
        if x<1 or x>=self.width or y<1 or y>=self.height:
            if ((x,y) != self.goal) and ((x,y) != self.start):
                return False # easy way out
        xleft = x+turns
        while xleft > self.width-2:
            xleft = xleft - (self.width - 2)
        if (xleft,y) in self.storms_left:
            return False

        xright = x-turns
        while xright < 1:
            xright = xright + self.width - 2
        if (xright,y) in self.storms_right:
            return False

        yup = y+turns
        while yup > self.height - 2:
            yup = yup - (self.height - 2)
        if (x,yup) in self.storms_up:
            return False

        ydown = y-turns
        while ydown < 1:
            ydown = ydown + self.height - 2
        if (x,ydown) in self.storms_down:
            return False

        return True # space is free

    def return_score(self,x,y):
        xgoal,ygoal = self.goal
        return abs(x-xgoal) + abs(y-ygoal)

    def get_next_states(self,state: 'State'):
        new_states = []
        for xadd,yadd in [[0,0],] + DIRECTIONS:
            newturns = state.turns + 1
            newx = state.x + xadd
            newy = state.y + yadd
            if self.mget(newx,newy,newturns):
                score_new = self.return_score(newx,newy)
                new_states.append(State(newx,newy,newturns,score_new))
        return new_states


@dataclass
class State:
    x: int
    y: int
    turns: int
    score: int

    @property
    def heuristic(self):
        return self.turns + self.score

    @property
    def state(self):
        return (self.x,self.y,self.turns)

    def __lt__(self,other):
        return self.heuristic < other.heuristic


@dataclass
class PQueue:
    _container: list = field(default_factory=list)

    def push(self, node):
        heappush(self._container, node)

    def pop(self):
        return heappop(self._container)

    @property
    def empty(self) -> bool:
        return len(self._container) <= 0


def part1(fname=TEST_NAME):
    storm_map = Map(fname)
    frontier = PQueue()
    explored = set() # tuples of x,y,turns
    x0,y0 = storm_map.start
    xf,yf = storm_map.goal
    score0 = storm_map.return_score(x0,y0)
    state0 = State(x0,y0,0,score0)
    explored.add(state0.state)
    frontier.push(state0)
    turns=0
    while not frontier.empty:
        state = frontier.pop()
        for new_state in storm_map.get_next_states(state):
            print(f"{new_state.state=}")
            if (new_state.x, new_state.y) == storm_map.goal:
                return new_state.turns
            if new_state.state not in explored:
                explored.add(new_state.state)
                frontier.push(new_state)
    return False


if __name__ == "__main__":
    t1 = part1()
    print(f"{t1=}")





        




