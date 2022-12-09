import pyxel
from time import sleep

DAY8_FNAME = r"day8input.txt"

pyxel

def refresh(x,y,text,text_h):
    pyxel.pset(x,y,7)
    pyxel.rect(1, text_h, 70, 10, 0)
    pyxel.text(1,text_h,text,7)
    pyxel.flip()

def return_list_of_lists_from_file(fname: str=DAY8_FNAME) -> list[list[int]]:
    with open(fname,"r") as day8_file:
        forest = [[int(i) for i in list(each.strip())] for each in day8_file.readlines()]
    return forest

def create_map_of_visibile_trees(forest: list[list[int]], draw=False) -> list[list[int]]:
    """
    Return a list[list[int]] where each entry is 1 or 0. 1 if visible.
    """
    height = len(forest)
    width = len(forest[0])
    if draw:
        pyxel.init(width, height+10, title="AdventOfCode, Day8", fps=60)
        pyxel.cls(0)
        pyxel.flip()
        sleep(3)
    forest_bin = [[0 for w in range(width)] for h in range(height)]
    # from the left looking right
    for r,row in enumerate(forest):
        height_max_current = -1
        for c,tree in enumerate(row):
            if tree > height_max_current:
                forest_bin[r][c]=1
                height_max_current=tree
                if draw: refresh(c,r,"LEFT TO RIGHT",height+2)
            if height_max_current==9: break #save some time
    # from the right looking left
    for r,row in enumerate(forest):
        height_max_current = -1
        for c,tree in reversed(list(enumerate(row))):
            if tree > height_max_current:
                forest_bin[r][c]=1
                if draw: refresh(c,r,"RIGHT TO LEFT",height+2)
                height_max_current=tree
            if height_max_current==9: break #save some time
    # from the top looking down
    for c in range(width):
        height_max_current = -1
        for r in range(height):
            tree = forest[r][c]
            if tree > height_max_current:
                forest_bin[r][c]=1
                if draw: refresh(c,r,"TOP TO BOTTOM",height+2)
                height_max_current=tree
            if height_max_current==9: break #save some time
    # from the bottom looking up
    for c in range(width):
        height_max_current = -1
        for r in reversed(list(range(height))):
            tree = forest[r][c]
            if tree > height_max_current:
                forest_bin[r][c]=1
                if draw: refresh(c,r,"BOTTOM TO TOP",height+2)
                height_max_current=tree
            if height_max_current==9: break #save some time
    if draw: pyxel.show()
    return forest_bin

def sum_of_visible_trees(forest: list[list[int]]) -> int:
    rolling_sum=0
    for row in forest:
        rolling_sum += sum(row)
    return rolling_sum

def get_score_in_direction(view: list[int]) -> int:
    if len(view)==1: 
        return 0
    my_tree = view[0]
    score=0
    for tree in view[1:]:
        score += 1
        if tree >= my_tree:
            break
    return score

def get_score_for_location(forest: list[list[int]], r: int, c: int) -> int:
    left_look = forest[r][c::-1]
    left_score = get_score_in_direction(left_look)

    right_look = forest[r][c::]
    right_score = get_score_in_direction(right_look)

    up_look = [forest[row_ix][c] for row_ix in range(r,-1,-1)]
    up_score = get_score_in_direction(up_look)

    height = len(forest)
    down_look = [forest[row_ix][c] for row_ix in range(r,height)]
    down_score = get_score_in_direction(down_look)

    score = left_score*right_score*up_score*down_score
    return score

def create_map_of_scenic_scores(forest: list[list[int]]) -> list[list[int]]:
    height = len(forest)
    width = len(forest[0])
    forest_scores = [[0 for w in range(width)] for h in range(height)]
    
    for r in range(height):
        for c in range(width):
            score = get_score_for_location(forest,r,c)
            forest_scores[r][c] = score
    return forest_scores

def get_max_score_in_forest(forest_scores: list[list[int]]) -> int:
    max_current = 0
    for row in forest_scores:
        max_current = max(row + [max_current,])
    return max_current

if __name__ == "__main__":
    forest = return_list_of_lists_from_file()
    forest_bin = create_map_of_visibile_trees(forest,draw=True)
    visible_count = sum_of_visible_trees(forest_bin)
    forest_scores = create_map_of_scenic_scores(forest)
    max_score = get_max_score_in_forest(forest_scores)
    print(f"Total trees: {len(forest) * len(forest[0])}")
    print(f"Visible tree count: {visible_count}")
    print(f"Max score: {max_score}")

