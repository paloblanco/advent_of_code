from dataclasses import dataclass, field
from collections import deque
from itertools import product
from math import ceil

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

    def __post_init__(self):
        self.robots = [1,0,0,0]
        self.ores = [0,0,0,0]
        self.assign_blueprint()
    
    @property
    def true_score(self):
        return self.robots[3]*self.steps_left

    @property
    def best_possible_score(self):
        theoretical = self.steps_left*(self.steps_left)/2
        return self.true_score + theoretical

    def assign_blueprint(self):
        self.requirements[0] = [self.blueprint[0],0,0,0]
        self.requirements[1] = [self.blueprint[1],0,0,0]
        self.requirements[2] = [self.blueprint[2],self.blueprint[3],0,0]
        self.requirements[3] = [self.blueprint[4],0,self.blueprint[5],0]

    def try_to_take_next_step(self,next_step):
        needed = [req-have for req,have in zip(self.requirements[next_step], self.ores)]
        minutes_needed = max([ceil(need/rob) for need,rob in zip(needed,self.robots)]) + 1
        if minutes_needed >= self.steps_left:
            return None
        ores_new = [ore+rob*minutes_needed for ore,rob in zip(self.ores,self.robots)]
        ores_new = [ore-req for ore,req in zip(ores_new,self.requirements[next_step])]
        robots_new = [r for r in self.robots]
        robots_new[next_step] += 1
        steps_left_new = self.steps_left - minutes_needed
        path_new = self.path_to_me + (next_step,)
        state = State(steps_left_new, path_new,self.blueprint)
        state.requirements = self.requirements
        state.robots = robots_new
        state.ores = ores_new
        return state

    def return_new_states(self):
        # this will take a step and return the new states in a list
        options = [0,1]
        states = []
        if 1 in self.path_to_me:
            options.append(2)
        if 2 in self.path_to_me:
            options.append(3)
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


def search_recipe(bp):
    pass


def part1_search(fname=TEST_NAME):
    blueprints = return_blueprint_list(fname)
    for ID,bp in enumerate(blueprints):
        search_recipe(bp)

def part1(fname=TEST_NAME):
    blueprints = return_blueprint_list(fname)
    # for ID,bp in enumerate(blueprints):
    #     run_recipe_1(bp)
    run_recipe_1(blueprints[1])

if __name__ == "__main__":
    ores_test = part1()
    # print(f"{ores_test=}")

