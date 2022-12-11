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
    operation: callable  = lambda x: x

    def add_item(self,item):
        self.items.append(item)

    def process_item(self, item: int, monkey_list: list[type('Monkey')]):
        item = operation(item)
        item = item//3
        if item % test_divisible == 0:
            monkey_list[throw_to_true].add_item(item)
        else:
            monkey_list[throw_to_false].add_item(item)

    def take_my_turn(self, monkey_list: list[type('Monkey')]):
        while self.items():
            item_current = self.items.popleft()
            self.process_item(item_current, monkey_list)

    def __str__(self):
        return f"Monkey {self.index}, {self.items}"

    def __repr__(self):
        return self.__str__()


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
            operation = lambda x: x + num
        if oper == "*": 
            operation = lambda x: x * num
        test = int(lines.popleft().split(" ")[-1])
        throw_true = int(lines.popleft().split(" ")[-1])
        throw_false = int(lines.popleft().split(" ")[-1])
        try:
            lines.popleft()
        except: pass
        monkey = Monkey(
            index=monkey_ix,
            items=items,
            test_divisible=test,
            throw_to_true=throw_true,
            throw_to_false=throw_false,
            operation=operation)
        monkey_list.append(monkey)
    return monkey_list


if __name__ == "__main__":
    monkeys = get_monkeys_from_file(TEST_NAME)
    for monkey in monkeys:
        print(monkey)



