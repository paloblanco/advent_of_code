from dataclasses import dataclass, field

TEST_NAME  = r"day20input_test.txt"
INPUT_NAME  = r"day20input.txt"


@dataclass
class Link:
    value: int
    to: 'Link' = None
    prev: 'Link' = None

    def add_to(self,other: 'Link'):
        self.to = other
        other.prev = self

    def move_ahead(self,moves:int):
        self.prev.add_to(self.to)
        if moves >= 0:
            new_to = self.to
            for i in range(moves):
                new_to = new_to.to
            new_prev = new_to.prev
        else:
            new_prev = self.prev
            for i in range(-moves):
                new_prev = new_prev.prev
            new_to = new_prev.to
        new_prev.add_to(self)
        self.add_to(new_to)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class LinkList:
    
    def __init__(self,nums: list[int]):
        self._container = [Link(each) for each in nums]
        for i,link in enumerate(self._container[:-1]):
            link.add_to(self._container[i+1])
            if link.value==0:
                self.zero = link
        self._container[-1].add_to(self._container[0])
        self.root = self._container[0]

    def mix(self):
        for link in self._container:
            link.move_ahead(link.value)

    def return_val_after_zero(self,position):
        target = self.zero
        for i in range(position):
            target = target.to
        return target.value

    def __str__(self):
        _print_list = []
        link = self.root
        _print_list.append(str(link))
        link = link.to
        while link != self.root:
            _print_list.append(str(link))
            link = link.to
        return str(_print_list)

    def __repr__(self):
        return self.__str__()


def return_numbers_from_file(fname=TEST_NAME):
    with open(fname) as f:
        nums = [int(num.strip()) for num in f]
    return nums


def part1(fname=TEST_NAME):
    nums = return_numbers_from_file(fname)
    ll = LinkList(nums)
    # print(str(ll))
    ll.mix()
    p0 = ll.return_val_after_zero(1000)
    p1 = ll.return_val_after_zero(2000)
    p2 = ll.return_val_after_zero(3000)
    return p0+p1+p2

if __name__ == "__main__":
    test1 = part1() # there are repeat nums in true set
    print(f"{test1=}")

    part1_solution = part1(INPUT_NAME)
    print(f"{part1_solution=}")