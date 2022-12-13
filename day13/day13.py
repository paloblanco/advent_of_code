from collections import deque
from dataclasses import dataclass, field
from typing import Union

TEST_NAME = r"day13input_test.txt"
INPUT_NAME = r"day13input.txt"

class Queue:
    
    def __init__(self,start):
        self._container = deque(start)

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

def queue_from_line(line: str):
    return Queue(eval(line))

def get_inputs(fname: str=TEST_NAME):
    input_pairs = []
    with open(fname,"r") as input_file:
        for line in input_file:
            left = line.strip()
            line = next(input_file)
            right = line.strip()
            input_pairs.append([left,right])
            try:
                next(input_file).strip() # throw away blank
            except: 
                break  
    return input_pairs

def get_inputs_part2(fname: str=TEST_NAME):
    inputs = []
    with open(fname,"r") as input_file:
        for line in input_file:
            line = line.strip()
            if line:
                inputs.append(line)
    return inputs

def check_order(left: Union[int,Queue],right: Union[int,Queue], show=False) -> Union[bool,str]:
    while (not left.empty) and (not right.empty): #need to check every value
        left_val = left.pop()
        right_val = right.pop()
        if show: print(f"{left_val}    vs     {right_val}")
        left_type = type(left_val)
        right_type = type(right_val)
        if left_type==list: left_val = Queue(left_val)
        if right_type==list: right_val = Queue(right_val)
        if left_type==int and right_type==int:
            if left_val > right_val:
                return False
            elif left_val < right_val:
                return True
        else:
            if left_type==int:
                left_val = Queue([left_val,])
            if right_type==int:
                 right_val = Queue([right_val,])
            order_correct = check_order(left_val,right_val,show=show)
            if order_correct == 'continue':
                pass
            else:
                return order_correct
    if left.empty and right.empty:
        if show: print(f"Both sides ran out, continue")
        return 'continue'
    elif right.empty:
        if show: print(f"Right is empty, False")
        return False
    elif left.empty:
        if show: print(f"Left is empty, True")
        return True

@dataclass
class Packet:
    _str: str

    def __lt__(self,other):
        mypack = queue_from_line(self._str)
        otherpack = queue_from_line(other._str)
        if check_order(mypack,otherpack):
            return True
        else:
            return False

    def __str__(self):
        return self._str

    def __repr__(self):
        return self._str


def part2(fname=TEST_NAME) -> int:
    packets = get_inputs_part2(fname)
    packets.append('[[2]]')
    packets.append('[[6]]')
    packets = [Packet(each) for each in packets]
    packets.sort()
    ix_locs = []
    ix_needed = ['[[2]]','[[6]]']
    for i,P in enumerate(packets):
        if P._str in ix_needed:
            ix_locs.append(i+1)
    return ix_locs[0] * ix_locs[1]

def part1(fname=TEST_NAME) -> list[int]:
    packet_list = get_inputs(fname)
    correct_pairs = []
    for ix,(left,right) in enumerate(packet_list):
        printme=False
        # if ix+1 not in [2, 5, 9, 13, 14, 16, 19, 20, 23, 24, 25, 27, 30, 31, 32, 33, 34, 35, 43, 44, 50, 53, 55, 56, 58, 60, 63, 67, 68, 69, 70, 71, 72, 74, 75, 76, 80, 82, 86, 88, 89, 90, 94, 95, 96, 97, 104, 105, 106, 109, 110, 111, 112, 114, 115, 122, 125, 126, 127, 128, 129, 134, 135, 136, 139, 140, 146, 147, 148, 149]: printme=True
        if printme:
            print(f"------------------------------------------")
            print(f"INDEX: {ix}")
            print(left)
            print(right)
        if result := check_order(queue_from_line(left),queue_from_line(right),show=printme):
            correct_pairs.append(ix+1)
        if printme: print(result)
    return correct_pairs

if __name__ == "__main__":
   
    pairs_ok_test = part1()
    print(f"{pairs_ok_test =}")

    part1_pairs = part1(INPUT_NAME)
    part1_sum = sum(part1_pairs)
    # print(part1_pairs)
    print(f"{part1_sum =}")

    part2_test = part2()
    assert part2_test==140, f"{part2_test=}"

    part2_real = part2(INPUT_NAME)
    print(f"{part2_real=}")
