from dataclasses import dataclass, field
from collections import deque, defaultdict
from itertools import product
from math import ceil
from heapq import heappush,heappop

TEST_NAME = "day19input_test.txt"
INPUT_NAME = "day19input.txt"

"""
Notes:
Production can be specified by a sequence of produced robots, since you are just waiting between robots.
This means that you have 4**n-1 possible combinations, where n is robot number (-1 since you start with ore).
Until you have certain robots, you don't even have certain options.
4**8 = 65_536
4**9 = 260_000
4**10 = 1_048_576

4**10
"""

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

@dataclass
class Stack:
    _container: list = field(default_factory=list)

    def push(self, node):
        self._container.append(node)

    def pop(self):
        return self._container.pop()

    @property
    def empty(self) -> bool:
        return len(self._container) <= 0



ORE         = 0
CLAY        = 1
OBSIDIAN    = 2
GEODE       = 3


@dataclass
class Inventory:
    ID: int
    robots: list = field(default_factory=list)
    ores: list = field(default_factory=list)
    requirements: list = field(default_factory=list)

    def __post_init__(self):
        self.robots = [1,0,0,0]
        self.ores = [1,0,0,0]
        self.requirements = [1,0,0,0]
    
    def assign_blueprint(self, blueprint: list[int]):
        self.requirements[0] = [blueprint[0],0,0,0]
        self.requirements[1] = [blueprint[1],0,0,0]
        self.requirements[2] = [blueprint[2],blueprint[3],0,0]
        self.requirements[3] = [blueprint[4],0,blueprint[5],0]

    def return_results_from_plan(self,plan:list[int],steps=24):
        plan = deque(plan)
        plan.append(3)
        steps_executed = []
        next_step = plan.popleft()
        ores = [0,0,0,0]
        robots = [1,0,0,0]
        # print("=======")
        # print(f"{self.requirements}")
        while steps > 0:
            # print(f"Time: {25-steps}   {ores=}")
            make_robot=False
            if next_step == None:
                try:
                    next_step=plan.popleft()
                except:
                    next_step=None
            if next_step != None:
                reqs = self.requirements[next_step]
                if all([ore>=req for ore,req in zip(ores,reqs)]):
                    for i,_ in enumerate(ores):
                        ores[i] += -reqs[i]
                    make_robot = True
            for i,count in enumerate(robots):
                ores[i] += count
            if make_robot:
                robots[next_step] += 1
                steps_executed.append(next_step)
                next_step=None
            steps += -1
        early_cut = len(plan) > 0
        return ores[3], steps_executed, early_cut

@dataclass
class State:
    steps_left: int
    path_to_me: tuple[int]
    blueprint: list[int]
    true_score: int = 0

    def __str__(self):
        return f"Steps2go: {self.steps_left}   Rob: {self.robots}   Ores: {self.ores}   TS: {self.true_score}"

    def __repr__(self):
        return self.__str__()

    def __post_init__(self):
        self.robots = [1,0,0,0]
        self.ores = [0,0,0,0]
        self.assign_blueprint()

    def __lt__(self, other):
        return -self.best_possible_score < -other.best_possible_score
    
    @property
    def state(self):
        return tuple(self.robots) + tuple(self.ores)

    def add_true_score(self):
        self.true_score += self.steps_left

    @property
    def best_possible_score(self):
        theoretical = self.steps_left*(self.steps_left)/2
        return self.true_score + theoretical

    def assign_blueprint(self):
        self.requirements=[[],[],[],[],]
        self.requirements[0] = [self.blueprint[0],0,0,0]
        self.requirements[1] = [self.blueprint[1],0,0,0]
        self.requirements[2] = [self.blueprint[2],self.blueprint[3],0,0]
        self.requirements[3] = [self.blueprint[4],0,self.blueprint[5],0]
        self.maxes = []
        for i in range(4):
            self.maxes.append(max([each[i] for each in self.requirements]))

    def try_to_take_next_step(self,next_step):
        needed = [req-have for req,have in zip(self.requirements[next_step], self.ores)]
        minutes_needed = 0
        for need,rob in zip(needed,self.robots):
            try:
                minutes_needed = max(minutes_needed,ceil(need/rob))
            except ZeroDivisionError:
                pass
        minutes_needed += 1
        if minutes_needed >= self.steps_left:
            return None
        ores_new = [ore+rob*minutes_needed for ore,rob in zip(self.ores,self.robots)]
        ores_new = [ore-req for ore,req in zip(ores_new,self.requirements[next_step])]
        robots_new = [r for r in self.robots]
        robots_new[next_step] += 1
        steps_left_new = self.steps_left - minutes_needed
        path_new = self.path_to_me + (next_step,)
        state = State(steps_left_new, path_new,self.blueprint, true_score=self.true_score)
        state.requirements = self.requirements
        state.maxes = self.maxes
        state.robots = robots_new
        state.ores = ores_new
        if next_step == GEODE: state.add_true_score()
        return state

    def return_new_states(self):
        # this will take a step and return the new states in a list
        options = [0,1]
        states = []
        if 1 in self.path_to_me:
            options.append(2)
        if 2 in self.path_to_me:
            options.append(3)
        for i in range(3):
            if self.robots[i] >= self.maxes[i]:
                try:
                    options.remove(i)
                except:
                    pass
        for next_step in options:
            new_state = self.try_to_take_next_step(next_step)
            if new_state: states.append(new_state)
        return states


def return_blueprint_list(fname=TEST_NAME) -> list:
    blueprints = []
    with open(fname) as blueprint_file:
        for line in blueprint_file:
            line=line.strip().split(" ")
            ore_ore = line[6]
            clay_ore = line[12]
            obs_ore = line[18]
            obs_clay = line[21]
            geo_ore = line[27]
            geo_obs = line[30]
            this_blueprint = [ore_ore,clay_ore,obs_ore,obs_clay,geo_ore,geo_obs]
            this_blueprint = [int(e) for e in this_blueprint]
            blueprints.append(this_blueprint)
    return blueprints

def make_permutations():
    perms = set()
    perms.add((1,2))
    for prange in range(3,12):
    # for prange in [13,]:
        for p in product([0,1,2,3],repeat=prange):
            # must have a 1 and a 2
            if 2 not in p: continue
            # 2 must be preceded by 1
            if 1 not in p[:p.index(2)]: continue
            # if there is a 3, must be preceded by 2
            if (3 in p) and (2 not in p[:p.index(3)]): continue
            perms.add(p)
    return perms
    
def run_recipe_1(bp):
    inv = Inventory(0)
    inv.assign_blueprint(bp)
    print(f"{inv.requirements=}")
    perms = make_permutations()
    print(f"{len(perms)=}")
    best_score = 0
    winner=[0,1,2,3]
    for p in perms:
        s, p_final, cut = inv.return_results_from_plan(p)
        best_score = max(best_score,s)
        if best_score==s:
            winner=p_final
    print(f"{best_score=}")
    print(f"{winner=}")


def search_recipe(bp, timeremaining=24):
    frontier = PQueue()
    explored = dict()
    best_true_score = 0
    state_current = State(timeremaining,(0,),bp)
    state_current.assign_blueprint()
    explored[state_current.state] = state_current.best_possible_score
    frontier.push(state_current)
    best_true_score = max(best_true_score,state_current.true_score)
    while not frontier.empty:
        state_current: State = frontier.pop()
        for new_state in state_current.return_new_states():
            if new_state.best_possible_score <= best_true_score: continue
            if new_state.state in explored:
                if new_state.best_possible_score <= explored[new_state.state]:
                    continue
            frontier.push(new_state)
            explored[new_state.state] = new_state.best_possible_score
            best_true_score = max(best_true_score,new_state.true_score)
    return best_true_score

def part2_search(fname=TEST_NAME):
    blueprints = return_blueprint_list(fname)[:3]
    best_scores = []
    for ID,bp in enumerate(blueprints):
        best_scores.append(search_recipe(bp,timeremaining=32))
    return best_scores

def part1_search(fname=TEST_NAME):
    blueprints = return_blueprint_list(fname)
    best_scores = []
    for ID,bp in enumerate(blueprints):
        best_scores.append(search_recipe(bp))
    return sum([(i+1)*bs for i,bs in enumerate(best_scores)])

def part1(fname=TEST_NAME):
    blueprints = return_blueprint_list(fname)
    # for ID,bp in enumerate(blueprints):
    #     run_recipe_1(bp)
    run_recipe_1(blueprints[1])

def test_making_children():
    blueprints = return_blueprint_list()
    state_current = State(24,(0,),blueprints[0])
    state_current.assign_blueprint()
    states = []
    print(state_current)
    for each in state_current.return_new_states():
        print(each)
        for e in each.return_new_states():
            print(e)
            for c in e.return_new_states():
                print(c)
                for d in c.return_new_states():
                    print(d)
                    for f in d.return_new_states():
                        print(f)


if __name__ == "__main__":
    test_1 =  part1_search()
    print(f"{test_1=}")

    # part_1 =  part1_search(INPUT_NAME)
    # print(f"{part_1=}")
        
    test_2 = part2_search()
    for e in test_2:
        print(e)

    part2 = part2_search(INPUT_NAME)
    print(f"{part2[0]*part2[1]*part2[2]=}")
    
