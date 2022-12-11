from dataclasses import dataclass
from collections import deque
import pyxel

TEST_NAME = "day11inputtest.txt"
INPUT_NAME = "day11input.txt"

def init_pyxel():
    pyxel.init(128, 128, title="AdventOfCode, Day11", fps=60, capture_scale=3, capture_sec=60)
    pyxel.load("my_resource.pyxres")
    pyxel.cls(0)
    draw_background()
    pyxel.flip()

def draw_background():
    pyxel.cls(0)
    pyxel.bltm(0,0,0,128,0,128,128,0)
    pyxel.bltm(0,0,0,0,0,128,128,0)
    pyxel.text(40,16,"AoC Day 11", 1)
    pyxel.text(5,120,"NormGear -- CRT matrix display", 5)

def refresh(monkey_list, from_ix, to_ix, throw=False):
    draw_background()
    for m in monkey_list:
        xp = 16+8*m.index + 8*(m.index//2)
        yp = 7*8 + (m.index%2) * 16
        for ix,e in enumerate(m.items):
            pyxel.text(xp,yp+ ix*6,str(e),1)
    for i in range(10): 
        pyxel.flip()
    if not throw: 
        return
    xball = 16+8*from_ix + 8*(from_ix//2)
    yball = 6*8 + (from_ix%2) * 16
    xto = 16+8*to_ix + 8*(to_ix//2)
    yto = 6*8 + (to_ix%2) * 16
    dy = -2.25
    dx = (xto-xball)/60
    pyxel.circ(xball,yball,3,6)
    pyxel.circb(xball,yball,3,1)
    pyxel.flip()
    loopcount=0
    while abs(xball-xto) + abs(yball-yto) > 6:
        xball += dx
        yball += dy
        dy += 0.075
        loopcount+=1
        draw_background()
        for m in monkey_list:
            xp = 16+8*m.index + 8*(m.index//2)
            yp = 7*8 + (m.index%2) * 16
            for ix,e in enumerate(m.items):
                pyxel.text(xp,yp+ ix*6,str(e),1)
        pyxel.circ(xball,yball,3,6)
        pyxel.circb(xball,yball,3,1)
        pyxel.flip()


@dataclass
class Monkey:
    index: int
    items: deque[int]
    test_divisible: int
    throw_to_true: int
    throw_to_false: int
    operation: callable
    inspections: int = 0
    worry_reduction: int = 3
    common_factor: int = 1000000

    def add_item(self,item):
        self.items.append(item)

    def process_item(self, item: int, monkey_list: list[type('Monkey')]):
        item = self.operation(item)
        item = item // self.worry_reduction
        self.inspections += 1
        item = item%self.common_factor
        throw_to = self.throw_to_true if item % self.test_divisible else self.throw_to_false
        if DRAW: refresh(monkey_list,self.index,throw_to,throw=True)
        monkey_list[throw_to].add_item(item)
        if DRAW: refresh(monkey_list,self.index,throw_to,throw=False)

    def take_my_turn(self, monkey_list: list[type('Monkey')]):
        while self.items:
            if DRAW: refresh(monkey_list,self.index,-1,throw=False)
            item_current = self.items.popleft()
            self.process_item(item_current, monkey_list)

    def __str__(self):
        return f"Monkey {self.index}, {self.items}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self,other):
        return self.inspections < other.inspections


def get_monkeys_from_file(fname: str = INPUT_NAME, worry_factor: int=3) -> list[Monkey]:
    with open(fname, 'r') as input_file:
        lines = deque([each.strip() for each in input_file.readlines()])
    monkey_list=[]
    common_factors = []
    while lines:
        monkey_ix = int(lines.popleft().split(" ")[1][:-1])
        items_line = lines.popleft().split(":")[1]
        items = [int(each) for each in items_line.split(",")]
        oper, num = lines.popleft().split(" ")[-2:]
        if oper == "+": 
            if num == 'old':
                operation = lambda x: x + x
            else:
                operation = (lambda num: (lambda x: x + int(num)))(num)
        if oper == "*": 
            if num == "old":
                operation = lambda x: x * x
            else:
                operation = (lambda num: (lambda x: x * int(num)))(num)
        test = int(lines.popleft().split(" ")[-1])
        common_factors.append(test)
        throw_true = int(lines.popleft().split(" ")[-1])
        throw_false = int(lines.popleft().split(" ")[-1])
        try:
            lines.popleft()
        except: pass
        monkey = Monkey(
            index=monkey_ix,
            items=deque(items),
            test_divisible=test,
            throw_to_true=throw_true,
            throw_to_false=throw_false,
            operation=operation,
            worry_reduction=worry_factor)
        monkey_list.append(monkey)
    lcd = 1
    for f in common_factors:
        lcd *= f
    for m in monkey_list:
        m.common_factor = lcd
    return monkey_list

def problem_one(fname=TEST_NAME, rounds=20):
    monkeys = get_monkeys_from_file(fname)
    for i in range(rounds):
        for m in range(len(monkeys)):
            monkeys[m].take_my_turn(monkeys)
    monkeys.sort()
    return monkeys[-1].inspections * monkeys[-2].inspections

def problem_two(fname=TEST_NAME, rounds=10000):
    monkeys = get_monkeys_from_file(fname, worry_factor=1)
    for i in range(rounds):
        for m in range(len(monkeys)):
            monkeys[m].take_my_turn(monkeys)
    monkeys.sort()
    return monkeys[-1].inspections * monkeys[-2].inspections

def main():
    monkey_business_one_test = problem_one()
    assert monkey_business_one_test == 10605, f"{monkey_business_one_test =}"
    monkey_business_one = problem_one(INPUT_NAME)
    print(f"Monkey business part 1: {monkey_business_one}")

    monkey_business_two_test = problem_two()
    assert monkey_business_two_test == 2713310158, f"{monkey_business_two_test =}"

    monkey_business_two = problem_two(INPUT_NAME)
    print(f"Monkey business part 2: {monkey_business_two}")

def main_draw():
    monkey_business_one = problem_one(INPUT_NAME)
    print(f"Monkey business part 1: {monkey_business_one}")

if __name__ == "__main__":
    DRAW=True

    if not DRAW:
        main()
    
    else:
        init_pyxel()
        main_draw()
        


