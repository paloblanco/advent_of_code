from dataclasses import dataclass
from collections import deque

TEST_NAME = "day11inputtest.txt"
INPUT_NAME = "day11input.txt"


@dataclass
class Monkey:
    index: int
    items: deque[int]
    test_divisible: int
    throw_to_true: int
    throw_to_false: int
    operation: callable
    inspections: int = 0

    def add_item(self,item):
        self.items.append(item)

    def process_item(self, item: int, monkey_list: list[type('Monkey')]):
        item = self.operation(item)
        item = item//3
        self.inspections += 1
        if item % self.test_divisible == 0:
            monkey_list[self.throw_to_true].add_item(item)
        else:
            monkey_list[self.throw_to_false].add_item(item)

    def take_my_turn(self, monkey_list: list[type('Monkey')]):
        while self.items:
            item_current = self.items.popleft()
            self.process_item(item_current, monkey_list)

    def __str__(self):
        return f"Monkey {self.index}, {self.items}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self,other):
        return self.inspections < other.inspections


def get_monkeys_from_file(fname: str = INPUT_NAME) -> list[Monkey]:
    with open(fname, 'r') as input_file:
        lines = deque([each.strip() for each in input_file.readlines()])
    monkey_list=[]
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
            operation=operation)
        monkey_list.append(monkey)
    return monkey_list

def problem_one(fname=TEST_NAME, rounds=20):
    monkeys = get_monkeys_from_file(fname)
    for i in range(rounds):
        for m in range(len(monkeys)):
            monkeys[m].take_my_turn(monkeys)
    monkeys.sort()
    return monkeys[-1].inspections * monkeys[-2].inspections


if __name__ == "__main__":
    monkey_business_one_test = problem_one()
    assert monkey_business_one_test == 10605
    monkey_business_one = problem_one(INPUT_NAME)
    print(f"Monkey business part 1: {monkey_business_one}")



