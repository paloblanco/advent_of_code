from heapq import heappush,heappop
from dataclasses import dataclass, field


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



        




