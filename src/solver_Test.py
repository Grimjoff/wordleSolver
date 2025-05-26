import random
from src.wordle_solver_logic import WordleSolverLogic

def run_tests(word_list, num_tests=100, verbose=False):
    solver = WordleSolverLogic(word_list)
    total_guesses = 0
    solved = 0

    for _ in range(num_tests):
        target = random.choice(word_list)
        solver.reset()
        guesses_needed = solver.solve_word(target, verbose=verbose)
        if guesses_needed is not None:
            solved += 1
            total_guesses += guesses_needed
        # else:
            # if verbose:
                #print(f"Failed to solve {target}")

    print(f"Solved {solved}/{num_tests} words")
    if solved > 0:
        print(f"Average guesses: {total_guesses / solved:.2f}")

if __name__ == "__main__":
    # Load your word list as before, e.g.:
    with open("../data/oldList.csv") as f:
        word_list = [line.strip() for line in f if line.strip()]

    run_tests(word_list, num_tests=14855, verbose=True)
