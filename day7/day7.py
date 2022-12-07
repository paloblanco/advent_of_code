import os
from time import sleep

DAY7_FILENAME = r"day7input.txt"

def clear():
    os.system('cls')

class Node:
    
    def __init__(self, name: str):
        self.parent = None
        self.name = name


class Directory(Node):

    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def calc_size(self):
        size = 0
        for child in self.children:
            try:
                size += child.size
            except:
                size += child.calc_size()
        return size

    def check_if_child_exists(self,name):
        for child in self.children:
            if name == child.name:
                return True
        return False

    def __str__(self):
        return f"- Dir: {self.name}"

    def __repr__(self):
        return self.__str__()

    def pprint(self, indent=0):
        structure=f"{'  '*indent}{self}\n"
        for child in self.children:
            try:
                structure += child.pprint(indent=indent+1)
            except:
                structure += f"{'  '*(indent+1)}{child}\n"
        return structure


class File(Node):

    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

    def __str__(self):
        return f"- File: {self.name}, size: {self.size}"

    def __repr__(self):
        return self.__str__()


def get_inputs_from_file(fname=DAY7_FILENAME):
    with open(fname,"r") as day7_file:
        day7_lines = [each.strip() for each in day7_file.readlines()]
    return day7_lines

def cd(parent,child_name,root):
    if child_name == "/":
        current_node = root
    elif child_name == "..":
        current_node = parent.parent
    else:
        for child in parent.children:
            if child.name == child_name:
                current_node = child
    return current_node

def create_graph_from_text(lines):
    root = Directory('/')
    current_node = root
    for line in lines:
        output = line.split(" ")
        if output[0] == "$": #command
            if output[1] == "cd":
                current_node = cd(current_node,output[2],root)
        elif output[0] == "dir":
            child_name = output[1]
            child_present = current_node.check_if_child_exists(child_name)
            if not child_present:
                current_node.add_child(Directory(child_name))
        else:
            size = int(output[0])
            child_name = output[1]
            child_present = current_node.check_if_child_exists(child_name)
            if not child_present:
                current_node.add_child(File(child_name, size))
        # print(root.pprint())
        # sleep(0.025)
        # clear()
    return root

def return_every_directory_as_list(root):
    if type(root) != Directory: return []
    directories = [root,]
    for child in root.children:
        if type(child) == Directory:
            directories = directories + return_every_directory_as_list(child)
    return directories
        

def get_sum_of_small_directories():
    lines = get_inputs_from_file()
    root = create_graph_from_text(lines)
    running_sum = 0
    directories = return_every_directory_as_list(root)
    for directory in directories:
        size = directory.calc_size()
        if size <= 100000:
            running_sum += size
    return running_sum


    print(root.pprint())

def test_graph():
    a = Directory('a')
    b = File('b',123)
    c = File('c',123)
    d = Directory('d')
    e = File('e',1000)

    a.add_child(b)
    a.add_child(c)
    a.add_child(d)
    d.add_child(e)

    print(a.pprint())
    print(a.calc_size())

if __name__ == "__main__":
    running_sum = get_sum_of_small_directories()
    print(f"Sum small directories: {running_sum}")