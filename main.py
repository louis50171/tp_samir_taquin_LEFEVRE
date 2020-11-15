from class_Puzzle import Puzzle
from gui import launch_gui

if __name__ == '__main__':
    # PARAMETERS
    puzzle_size = 3
    nb_tiles = 8
    nb_iteration = 1

    # RESOLUTION
    score = 0
    for k in range(nb_iteration):
        p = Puzzle(puzzle_size, nb_tiles, verbose=False)
        p.create_tiles()  # Randomly create tiles so that the puzzle is solvable

        step = 0  # Iteration limiter
        while not p.is_solve() and step < 200:
            step += 1
            p.solve()
        score += p.is_solve()  # Resolution score
        if k % 100 == 0:
            print("Step ", k + 1, " : Resolution percentage = ", score / (k + 1) * 100, "%")

    # Printing
    if p.is_solve():
        launch_gui(p)
