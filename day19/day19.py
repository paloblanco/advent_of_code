from dataclasses import dataclass

TEST_NAME = "day19input_test.txt"
INPUT_NAME = "day19input.txt"

@dataclass
class Inventory:
    ID: int
    ore_robot: int = 1
    clay_robot: int = 0
    obsidian_robot: int = 0
    geode_robot: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    ore_robot_cost_ore: int = 1
    clay_robot_cost_ore: int = 1
    obsidian_robot_cost_ore: int = 1
    obsidian_robot_cost_clay: int = 1
    geode_robot_cost_ore: int = 1
    geode_robot_cost_obsidian: int = 1

    def assign_blueprint(self, blueprint: list[int]):
        ore_robot_cost_ore = blueprint[0]
        clay_robot_cost_ore = blueprint[1]
        obsidian_robot_cost_ore = blueprint[2]
        obsidian_robot_cost_clay = blueprint[3]
        geode_robot_cost_ore = blueprint[4]
        geode_robot_cost_obsidian = blueprint[5]


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



if __name__ == "__main__":
    print(return_blueprint_list())

