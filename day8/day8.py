DAY8_FNAME = r"day8input.txt"

def return_list_of_lists_from_file(fname: str=DAY8_FNAME) -> list[list[int]]:
    with open(fname,"r") as day8_file:
        forest = [[int(i) for i in list(each.strip())] for each in day8_file.readlines()]
    return forest

def create_map_of_visibile_trees(forest: list[list[int]]) -> list[list[int]]:
    """
    Return a list[list[int]] where each entry is 1 or 0. 1 if visible.
    """
    height = len(forest)
    width = len(forest[0])
    forest_bin = [[0 for w in range(width)] for h in range(height)]
    # from the left looking right
    for r,row in enumerate(forest):
        height_max_current = -1
        for c,tree in enumerate(row):
            if tree > height_max_current:
                forest_bin[r][c]=1
                height_max_current=tree
            if height_max_current==9: break #save some time
    # from the right looking left
    for r,row in enumerate(forest):
        height_max_current = -1
        for c,tree in reversed(list(enumerate(row))):
            if tree > height_max_current:
                forest_bin[r][c]=1
                height_max_current=tree
            if height_max_current==9: break #save some time
    # from the top looking down
    for c in range(width):
        height_max_current = -1
        for r in range(height):
            tree = forest[r][c]
            if tree > height_max_current:
                forest_bin[r][c]=1
                height_max_current=tree
            if height_max_current==9: break #save some time
    # from the bottom looking up
    for c in range(width):
        height_max_current = -1
        for r in reversed(list(range(height))):
            tree = forest[r][c]
            if tree > height_max_current:
                forest_bin[r][c]=1
                height_max_current=tree
            if height_max_current==9: break #save some time
    return forest_bin

def sum_of_visible_trees(forest: list[list[int]]) -> int:
    rolling_sum=0
    for row in forest:
        rolling_sum += sum(row)
    return rolling_sum


if __name__ == "__main__":
    forest = return_list_of_lists_from_file()
    forest_bin = create_map_of_visibile_trees(forest)
    visible_count = sum_of_visible_trees(forest_bin)
    print(f"Total trees: {len(forest) * len(forest[0])}")
    print(f"Visible tree count: {visible_count}")

