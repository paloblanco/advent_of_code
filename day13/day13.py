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


def get_inputs(fname: str=TEST_NAME):
    input_pairs = []
    with open(fname,"r") as input_file:
        for line in input_file:
            left = Queue(eval(line.strip()))
            line = next(input_file)
            right = Queue(eval(line.strip()))
            try:
                next(input_file).strip() # throw away blank
            except: 
                break
            input_pairs.append([left,right])
    return input_pairs

def check_order(left,right):
    order_correct = True # break out if this is false
    while (not left.empty) and (not right.empty): #need to check every value
        left_val = left.pop()
        right_val = right.pop()
        left_type = type(left_val)
        if left_type==list: left_val = Queue(left_val)
        right_type = type(right_val)
        if right_type==list: right_val = Queue(right_val)
        if left_type==Queue and right_type==Queue:
            order_correct = check_order(left_val,right_val)
            if order_correct=='continue':
                pass
            else:
                return order_correct
        elif left_type==int and right_type==int:
            if left_val > right_val:
                return False
            elif left_val < right_val:
                return True
            else:
                order_correct='continue'
        else:
            if left_type==int:
                left_val = Queue([left_val,])
            if right_type==int:
                 right_val = Queue([right_val,])
            order_correct = check_order(left_val,right_val)
            if order_correct=='continue':
                pass
            else:
                return order_correct
    if right.empty:
        if not left.empty:
            return False
        else:
            return 'continue'
    return True


def part1(fname=TEST_NAME) -> int:
    packet_list = get_inputs(fname)
    correct_pairs = []
    for ix,(left,right) in enumerate(packet_list):
        if check_order(left,right):
            correct_pairs.append(ix+1)
    return correct_pairs

if __name__ == "__main__":
    pairs_ok_test = part1()
    print(f"{pairs_ok_test =}")

    part1_pairs = part1(INPUT_NAME)
    part1_sum = sum(part1_pairs)
    print(f"{part1_sum =}")