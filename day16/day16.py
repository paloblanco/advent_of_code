from dataclasses import dataclass,field
from itertools import permutations
from collections import deque, defaultdict
from typing import Union

TEST_NAME = "day16input_test.txt"
INPUT_NAME = "day16input.txt"

"""
This one sounds hard. Need to take some notes.

Assume that the best path will move from non0 valve to the next, 
stopping when time is up or every valve is turned.

We can reduce the size of the graph to only non0 nodes ( + the start),
where each edge has a length of the shortest distance between the two.
Doing this will make a brute force search more feasible. Test problem only has 
6 nodes then, full is ~ 15.

Steps:
1. read in data, build raw graph
2. create reduced graph with weighted edges
3. brute force for maximum
    - adjustment here: there is a logical "next best move", try these first.
"""

@dataclass
class Queue:
    
    def __init__(self,start=None):
        if start:
            self._container = deque(start)
        else:
            self._container = deque()

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

@dataclass
class Node:
    name: str
    value: int
    neighbors: dict[str,list[int,'Node']] = field(default_factory=dict)

    def add_neighbor(self,other: 'Node', distance: int = 1) -> None:
        self.neighbors[other.name] = [other, distance]

    def __str__(self):
        return f"{self.name}: v={self.value}   n={[(k,v[1]) for k,v in self.neighbors.items()]}"

    def __repr__(self):
        return self.__str__()


@dataclass
class Graph:
    raw: list[list[str,int,list[str]]]
    nodes: dict[str,Node] = field(default_factory=dict)
    nodes_reduced: dict[str,Node] = field(default_factory=dict)

    def __post_init__(self):
        for each in self.raw:
            node = Node(each[0],each[1])
            self.nodes[node.name] = node
        for each in self.raw:
            for neighbor in each[2]:
                self.nodes[each[0]].add_neighbor(self.nodes[neighbor],1)

    def get_times_to_nodes(self, name, all_names):
        frontier = Queue()
        current_node = self.nodes[name]
        explored = dict()
        # distances = dict()
        for n,dd in current_node.neighbors.values():
            frontier.push([n,dd]) # second number is distance
        while not frontier.empty:
            current_node,current_distance = frontier.pop()
            current_name = current_node.name
            if current_name not in explored or current_distance < explored[current_name]:
                for n,_ in current_node.neighbors.values():
                    frontier.push([n,1+current_distance]) # second number is distance
                explored[current_name] = current_distance
        distances = {name_neighbor:distance for name_neighbor,distance in explored.items() if ((name_neighbor in all_names) and (name_neighbor != name))}
        return distances

    def reduce_graph(self):
        nonzero_names = ['AA',]
        for n in self.nodes.values():
            if n.value > 0: nonzero_names.append(n.name)
        for name in nonzero_names:
            oldnode = self.nodes[name]
            newnode = Node(oldnode.name,oldnode.value)
            self.nodes_reduced[name] = newnode
        for name in nonzero_names:
            travel_times = self.get_times_to_nodes(name, nonzero_names)
            for newname,dist in travel_times.items():
                self.nodes_reduced[name].add_neighbor(self.nodes_reduced[newname],dist)

    def score_permutation(self,perm,startname,steps=30):
        steps_old = steps
        score=0
        old = startname
        return_perm=[]
        for name in perm:
            dist = self.nodes_reduced[old].neighbors[name][1]
            val = self.nodes_reduced[name].value
            steps += -(dist+1)
            if steps <= 0: 
                steps += (dist+1)
                break
            score += max(steps*val,0)
            old=name
            return_perm.append(name)
        return score,steps_old - steps, return_perm
    
    def crawl_graph_all(self,steps=30):
        current_node = self.nodes_reduced['AA']
        nodes_remaining: list[str] = [k for k in self.nodes_reduced.keys()]
        nodes_remaining.remove(current_node.name)
        startname = current_node.name
        best_score=0
        for perm in permutations(nodes_remaining):
            score, steps_needed, _ = self.score_permutation(perm,startname,steps)
            best_score = max(best_score,score)
        return best_score

    def crawl_graph_all_limit(self,steps=30,limit=6):
        current_node = self.nodes_reduced['AA']
        nodes_remaining: list[str] = [k for k in self.nodes_reduced.keys()]
        nodes_remaining.remove(current_node.name)
        startname = current_node.name
        # best_score=0
        record = []
        for perm in permutations(nodes_remaining, limit):
            score, steps_needed, perm_short = self.score_permutation(perm,startname,steps)
            record.append([score,perm_short,steps_needed])
        return record

    def crawl_graph_all_limit_ext(self,nodes_remaining,steps=26,limit=5,startname='AA'):
        record = []
        for perm in permutations(nodes_remaining, limit):
            score, steps_needed, perm_short = self.score_permutation(perm,startname,steps)
            record.append([score,perm_short,steps_needed])
        return record

    def crawl_all2(self, steps=26, limit=5):
        all_perms_1 = self.crawl_graph_all_limit(steps=steps,limit=limit)
        all_perms_1 = [(score,tuple(perm),steps) for score,perm,steps in all_perms_1]
        all_perms_1 = set(all_perms_1)
        all_nodes = {k for k in self.nodes_reduced.keys() if k != 'AA'}
        max_score = 0
        print(f"{len(all_perms_1)}")
        print(f"{all_nodes=}")
        for i,(score, perm, steps) in enumerate(all_perms_1):
            startname = 'AA'
            nodes_remaining = all_nodes - set(perm)
            records = self.crawl_graph_all_limit_ext(nodes_remaining,steps=26,limit=5,startname=startname)
            best_score = max([x[0] for x in records])
            max_score = max(max_score,score+best_score)
            print(f"{i=}   {max_score=}")
        return max_score

    def check_combos(self,start_name,nodes_remaining,steps=30,chunksize=3,perm_count=3):
        return_scores = []
        if len(nodes_remaining) <= chunksize:
            for perm in permutations(nodes_remaining):
                score, steps_needed, endperm = self.score_permutation(perm,start_name,steps)
                return_scores.append((score,endperm,steps_needed))
            return_scores = sorted(return_scores,key= lambda x: x[0],reverse=True)[:perm_count]
            return return_scores
        else:
            for perm in permutations(nodes_remaining, r=chunksize):
                score, steps_needed, endperm = self.score_permutation(perm,start_name,steps)
                return_scores.append([score,endperm,steps_needed])
            return_scores = sorted(return_scores,key= lambda x: x[0],reverse=True)[:perm_count]
            return_scores_deep = []
            for score, perm, steps_needed, in return_scores:
                if len(perm) < 3:
                    return_scores_deep.append([score,perm,steps_needed])
                    continue
                nodes_remaining_sub = [each for each in nodes_remaining if each not in perm]
                start_sub = perm[-1]
                steps_remaining = steps - steps_needed
                sub_returns = self.check_combos(start_sub,nodes_remaining_sub,steps=steps_remaining,chunksize=chunksize,perm_count=perm_count)
                for subscore,subperm,substepsneeded in sub_returns:
                    appendscore = subscore + score
                    appendperm = list(perm) + list(subperm)
                    appendstepsneeded = steps_needed + substepsneeded
                    if appendstepsneeded < steps: return_scores_deep.append([appendscore, appendperm, appendstepsneeded])
            return return_scores_deep

    def crawl_graph_chunked(self,steps=30,chunksize=3,perm_count=3):
        # return the best n=permcount combos for a chunk
        current_node = self.nodes_reduced['AA']
        nodes_remaining: list[str] = [k for k in self.nodes_reduced.keys()]
        nodes_remaining.remove(current_node.name)
        start_name = current_node.name
        possible_sequences = self.check_combos(start_name,nodes_remaining,steps=steps,chunksize=chunksize,perm_count=perm_count)
        return possible_sequences

    def crawl_graph_chunked2(self,steps=26,chunksize=5,perm_count=3):
        # return the best n=permcount combos for a chunk
        current_node = self.nodes_reduced['AA']
        nodes_remaining: list[str] = [k for k in self.nodes_reduced.keys()]
        nodes_remaining.remove(current_node.name)
        start_name = current_node.name
        possible_sequences = self.check_combos(start_name,nodes_remaining,steps=steps,chunksize=chunksize,perm_count=perm_count)
        return possible_sequences

    def depth_first_graph(self, steps=30):
        current_node = self.nodes['AA']
        frontier = []
        explored = set()
        for n,dd in current_node.neighbors.values():
            frontier.append([n,dd,0]) # second number is distance. 3 is score        
        while not frontier.empty:
            current_node,distance,score = frontier.pop()
            pass


    def bfs_reduced_graph(self,steps=30):
        current_node = self.nodes_reduced['AA']
        frontier = Queue()
    
    def crawl_graph_best_next(self, steps=30):
        current_node = self.nodes_reduced['AA']
        nodes_visited: list[str] = [current_node.name,]
        nodes_remaining: list[str] = [k for k in self.nodes_reduced.keys()]
        nodes_remaining.remove(current_node.name)
        valves_total: list[list[int,int]] = [] #valve + starttime
        score = 0
        while nodes_remaining or steps > 0:
            best_new_score=0
            new_name=None
            for name,(node,dist) in current_node.neighbors.items():
                if name in nodes_visited: continue
                new_score = node.value*(steps-dist-1)
                if new_score > best_new_score:
                    best_new_score = new_score
                    new_name=name
            if new_name:
                print(new_name)
                nodes_remaining.remove(new_name)
                nodes_visited.append(new_name)
                new_node = self.nodes_reduced[new_name]
                steps += - (current_node.neighbors[new_name][1] + 1) # add 1 for turn on time
                score += new_node.value*steps
                current_node=new_node
            else:
                break
        return score

    def printme_reduced(self):
        for i,v in self.nodes_reduced.items():
            print(f"{str(v)}")
    
    def printme(self):
        for i,v in self.nodes.items():
            print(f"{str(v)}")


def read_data(fname=TEST_NAME):
    node_list = []
    with open(fname) as input_file:
        for line in input_file:
            line = line.strip().split(' ')
            name = line[1]
            value = int(line[4][5:-1])
            neighbors = [each.replace(',','') for each in line[9:]]
            node_list.append([name,value,neighbors])
    return node_list

def part1(fname=TEST_NAME):
    node_data = read_data(fname)
    graph0 = Graph(node_data)
    # graph0.printme()
    graph0.reduce_graph()
    graph0.printme_reduced()
    # return graph0.crawl_graph_best_next()
    # return graph0.crawl_graph_all()
    print(f"Bestnext: {graph0.crawl_graph_best_next()}")
    # sequences = graph0.crawl_graph_chunked(steps=30,chunksize=6,perm_count=6)
    sequences = graph0.crawl_graph_all_limit(steps=30,limit=6)
    return sorted(sequences,key=lambda x: x[0],reverse=True)[:100]

def part2(fname=TEST_NAME):
    node_data = read_data(fname)
    graph0 = Graph(node_data)
    graph0.reduce_graph()
    graph0.printme_reduced()
    best_score = graph0.crawl_all2(steps=26,limit=5)
    return best_score

if __name__ == "__main__":
    # score_test = part1()
    # print(f"{score_test=}")

    # seq_test = part1()
    # for each in seq_test:
    #     print(each) # 1647 to high, 1457 too low

    # seq_test = part1(INPUT_NAME)
    # for each in seq_test:
    #     print(each) # 1647 to high, 1457 too low

    score2 = part2(INPUT_NAME)
    print(f"{score2=}") # 2118 too low
    




