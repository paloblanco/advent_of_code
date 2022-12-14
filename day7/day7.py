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

    def get_all_extra_info(self):
        self.size = self.calc_size()
        self.width = self.calc_width()
        self.depth = self.calc_depth()
        self.position = self.get_position()
        for child in self.children:
            if type(child) != Directory: continue
            child.get_all_extra_info()
        self.max_depth = self.calc_max_depth()

    def get_position(self):
        position=0
        if self.parent:
            position = self.parent.children.index(self)
            if self.parent.position:
                position += self.parent.position
            else:
                position += self.parent.get_position()
        return position


    def calc_size(self):
        size = 0
        for child in self.children:
            try:
                size += child.size
            except:
                size += child.calc_size()
        return size

    def calc_width(self):
        width = 0
        child_dirs = 0
        for child in self.children:
            if type(child) != Directory: continue
            width += child.calc_width()
        if width==0: return 1
        return width

    def calc_max_depth(self):
        # must come after depth calc
        max_depth = self.depth
        for child in self.children:
            if type(child) != Directory: continue
            max_depth = max(max_depth,child.depth)
        return max_depth

    def calc_depth(self):
        if not self.parent:
            return 0
        depth=1
        depth += self.parent.calc_depth()
        return depth

    def check_if_child_exists(self,name):
        for child in self.children:
            if name == child.name:
                return True
        return False

    def __str__(self):
        # return f"- Dir: {self.name}"
        return self.name[0]

    def __repr__(self):
        return self.__str__()

    def pretty_print(self, indent: str = '', last_child: bool = True) -> None:
        # Print the current node
        print(indent + ('???' if last_child else '???') + ' ' + str(self))
        
        # If the node has children, print them each on their own line with a
        #  deeper indentation level
        if self.children:
            for i, child in enumerate(self.children):
                if type(child) != Directory: continue
                child.pretty_print(indent + ('   ' if last_child else '???  '), i == len(self.children) - 1)
    
    def pprint_old(self, indent=0):
        structure=f"{'  '*indent}{self} :"
        children_dir = []
        children_file = []
        for child in self.children:
            if type(child) == Directory:
                children_dir.append(child)
            else:
                children_file.append(child)
        for child in children_file:
            structure += "*"
        for child in children_dir:
            structure += "\n"
            structure += child.pprint(indent=indent+1)
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

def create_graph_from_text(lines,draw=False):
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
        if draw:
            clear()
            root.get_all_extra_info()
            print(root.pprint())
            sleep(0.01)
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

def smallest_directory_to_delete(size_total=70000000, size_needed=30000000):
    lines = get_inputs_from_file()
    root = create_graph_from_text(lines)
    size_occupied = root.calc_size()
    size_extra_needed = size_needed - (size_total - size_occupied)
    directories = return_every_directory_as_list(root)
    candidate=size_needed
    for directory in directories:
        size = directory.calc_size()
        if size > size_extra_needed:
            if size < candidate:
                candidate=size
    return candidate


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
    smallest_directory_size_to_delete = smallest_directory_to_delete()
    print(f"Smallest directory size to delete: {smallest_directory_size_to_delete}")
    # lines = get_inputs_from_file()
    # root = create_graph_from_text(lines,draw=False)
    # root.pretty_print()