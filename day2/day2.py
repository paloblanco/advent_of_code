DAY2_INPUT_FNAME = r"day2input.txt"

ROCK        = 1
PAPER       = 2
SCISSORS    = 3

LOSE    = 0
DRAW    = 3
WIN     = 6 

LETTER_LOOKUP = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

RESULTS_OPP_ME = {
    ROCK: {
        ROCK: DRAW,
        PAPER: WIN,
        SCISSORS: LOSE
    },
    PAPER: {
        ROCK: LOSE,
        PAPER: DRAW,
        SCISSORS: WIN
    },
    SCISSORS: {
        ROCK: WIN,
        PAPER: LOSE,
        SCISSORS: DRAW
    }
}

WIN_LOOKUP = {
    "X": LOSE,
    "Y": DRAW,
    "Z": WIN
}

MY_CHOICE_AGAINST_OPPONENT = {
    LOSE: {
        ROCK: SCISSORS,
        PAPER: ROCK,
        SCISSORS: PAPER
    },
    DRAW: {
        ROCK: ROCK,
        PAPER: PAPER,
        SCISSORS: SCISSORS
    },
    WIN: {
        ROCK: PAPER,
        PAPER: SCISSORS,
        SCISSORS: ROCK
    },

}

def convert_letter_to_prs_number(letter: str) -> int:
    return LETTER_LOOKUP[letter]

def get_results_from_match(letter_opponent: str, letter_me: str) -> int:
    rps_opp = convert_letter_to_prs_number(letter_opponent)
    rps_me = convert_letter_to_prs_number(letter_me)
    return RESULTS_OPP_ME[rps_opp][rps_me] + rps_me

def get_letter_tuples_from_file(fname=DAY2_INPUT_FNAME):
    with open(fname,"r") as results_file:
        results_lines=results_file.readlines()
    results_lines = [each.strip().split(" ") for each in results_lines]
    return results_lines

def tally_results_from_guide(fname=DAY2_INPUT_FNAME):
    results_lines = get_letter_tuples_from_file(fname)
    results_tallied = [get_results_from_match(each[0],each[1]) for each in results_lines]
    return sum(results_tallied)

def get_results_from_match_revised(letter_opponent: str, letter_me: str) -> int:
    rps_opp = convert_letter_to_prs_number(letter_opponent)
    match_result = WIN_LOOKUP[letter_me]
    my_choice = MY_CHOICE_AGAINST_OPPONENT[match_result][rps_opp]
    return match_result + my_choice

def tally_results_from_revised_guide(fname=DAY2_INPUT_FNAME):
    results_lines = get_letter_tuples_from_file(fname)
    results_tallied = [get_results_from_match_revised(each[0], each[1]) for each in results_lines]
    return sum(results_tallied)


if __name__ == "__main__":
    result = tally_results_from_guide()
    result_revised = tally_results_from_revised_guide()
    print(f"My total is: {result}")
    print(f"My revised total is: {result_revised}")
