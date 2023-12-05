import copy


# INITIAL
def convert_to_listed(puzzle):
    for row in puzzle:
        for cols in range(9):
            if row[cols] == 0:
                row[cols] = list(range(1, 10))

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced


def is_list(x):
    return type(x) == list


def list_to_int(puzzle):
    for row in puzzle:
        for cols in range(9):
            if is_list(row[cols]) and len(row[cols]) == 1:
                row[cols] = row[cols][0]
    return puzzle


# SIMPLE ELIM
# remove by row function
# rowcols is to look for list of potentials, rowcols2 is the numbers already given/solved in the sudoku to remove from
# list of potentials
def row_remover(puzzle):
    for row in puzzle:
        for cols in range(9):
            # if it is a list then...
            if is_list(row[cols]):
                # go through 0-8
                for cols2 in range(9):
                    # [row, col2] is not a list and [row,col2] is in the list [row,col]...
                    if not is_list(row[cols2]) and row[cols2] in row[cols]:
                        # remove the element from the list
                        row[cols].remove(row[cols2])

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced


def column_remover(puzzle):
    for row in puzzle:
        for cols in range(9):
            # if it is a list then...
            if is_list(row[cols]):
                # hold that list and look through the rest of the column
                for row2 in range(9):
                    # if the element in the column is not a list and the element in the column appears in the list,
                    # then remove it from the list.
                    if not is_list(puzzle[row2][cols]) and puzzle[row2][cols] in row[cols]:
                        row[cols].remove(puzzle[row2][cols])

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced


# remove by grid function
# rowcols is to look for list of potentials, n is the column index and m is the box index to check each square for
# numbers already given/solved to remove from list of potentials
def box_remover(puzzle):
    for row in range(9):
        for cols in range(9):
            if is_list(puzzle[row][cols]):
                # if its a list
                rcols = (cols // 3) * 3
                rrow = (row // 3) * 3
                # seperate into 3 groups, col 1 goes to 0 col 2 goes to 0 col 9 goes to 2 etc
                # same for rows
                # times by 3, so 0 goes to 0, 1 goes to 3, 2 goes to 6
                for n in range(rcols, rcols + 3):
                    # 0,3
                    # 3,6
                    # 6,9
                    for m in range(rrow, rrow + 3):
                        if not is_list(puzzle[m][n]) and puzzle[m][n] in puzzle[row][cols]:
                            puzzle[row][cols].remove(puzzle[m][n])

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced


# I DONT LIKE KEEP THE LOOPS IN THE END MAIN FUNCTION AND ONLY WANNA CONVERT TO LIST ONCE CANT REMOVE AS MATT FUNCTION
# CALLS THIS THOUGH
def initial_step(puzzle):
    convert_to_listed(puzzle)

    same = False

    while same == False:

        puzzle_copy = copy.deepcopy(puzzle)

        row_remover(puzzle)
        column_remover(puzzle)
        box_remover(puzzle)
        list_to_int(puzzle)

        if puzzle_copy == puzzle:
            same = True

    return puzzle


# INTERSECTION
def pointing_rows(puzzle, row, col, num):
    box_col = (col // 3) * 3
    box_row = (row // 3) * 3

    index = []
    for i in range(9):
        index.append(i)

    index.remove(box_col)
    index.remove(box_col + 1)
    index.remove(box_col + 2)

    # how many times num appears in lists inside that box
    box_count = 0

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if is_list(puzzle[i][j]) and num in puzzle[i][j]:
                box_count += 1

    # how many times num appears in lists in that box in that row
    row_box_count = 0

    for i in range(box_col, box_col + 3):
        if is_list(puzzle[row][i]) and num in puzzle[row][i]:
            row_box_count += 1

    if box_count == row_box_count and box_count != 0:
        for i in index:
            if is_list(puzzle[row][i]) and num in puzzle[row][i]:
                puzzle[row][i].remove(num)

    return puzzle


def pointing_cols(puzzle, row, col, num):
    box_col = (col // 3) * 3
    box_row = (row // 3) * 3

    index = []
    for i in range(9):
        index.append(i)

    index.remove(box_row)
    index.remove(box_row + 1)
    index.remove(box_row + 2)

    # how many times num appears in lists inside that box
    box_count = 0

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if is_list(puzzle[i][j]) and num in puzzle[i][j]:
                box_count += 1

    # how many times num appears in lists in that box in that column
    col_box_count = 0

    for i in range(box_row, box_row + 3):
        if is_list(puzzle[i][col]) and num in puzzle[i][col]:
            col_box_count += 1

    if box_count == col_box_count and box_count != 0:
        for i in index:
            if is_list(puzzle[i][col]) and num in puzzle[i][col]:
                puzzle[i][col].remove(num)

    return puzzle


def pointing_rows_reduction(puzzle):
    puzzle_reduced = initial_step(puzzle)

    for row in range(9):
        for col in range(9):
            for num in range(1, 10):
                puzzle_reduced2 = pointing_rows(puzzle_reduced, row, col, num)

    puzzle_reduced3 = list_to_int(puzzle_reduced2)

    return puzzle_reduced3


def pointing_cols_reduction(puzzle):
    puzzle_reduced = initial_step(puzzle)

    for row in range(9):
        for col in range(9):
            for num in range(1, 10):
                puzzle_reduced2 = pointing_cols(puzzle_reduced, row, col, num)

    puzzle_reduced3 = list_to_int(puzzle_reduced2)

    return puzzle_reduced3


def pointing_reduction(puzzle):
    puzzle_reduced1 = pointing_rows_reduction(puzzle)
    puzzle_reduced2 = pointing_cols_reduction(puzzle_reduced1)

    puzzle_reduced3 = list_to_int(puzzle_reduced2)

    return puzzle_reduced3


def row_pots_list(num, row, cols, sudoku):
    row_count = 0
    for i in range(9):
        if is_list(sudoku[row][i]) and num in sudoku[row][i]:
            row_count += 1
    rcols = (cols // 3) * 3
    row_box_count = 0
    for j in range(rcols, rcols + 3):
        if is_list(sudoku[row][j]) and num in sudoku[row][j]:
            row_box_count += 1
    if row_box_count == row_count and row_count != 0:
        rrow = (row // 3) * 3
        rerow = list(range(rrow, rrow + 3))
        rerow.remove(row)
        for m in rerow:
            for n in range(rcols, rcols + 3):
                if is_list(sudoku[m][n]) and num in sudoku[m][n]:
                    sudoku[m][n].remove(num)
    return sudoku


def col_pots_list(num, row, cols, sudoku):
    col_count = 0
    for i in range(9):
        if is_list(sudoku[i][cols]) and num in sudoku[i][cols]:
            col_count += 1
    rrow = (row // 3) * 3
    col_box_count = 0
    for j in range(rrow, rrow + 3):
        if is_list(sudoku[j][cols]) and num in sudoku[j][cols]:
            col_box_count += 1
    if col_count == col_box_count and col_count != 0:
        rcols = (cols // 3) * 3
        recols = list(range(rcols, rcols + 3))
        recols.remove(cols)
        for m in recols:
            for n in range(rrow, rrow + 3):
                if is_list(sudoku[n][m]) and num in sudoku[n][m]:
                    sudoku[n][m].remove(num)
    return sudoku


def box_row_reduction(sudoku):
    sudoku2 = row_remover(sudoku)
    for row in range(9):
        for cols in [0, 3, 6]:
            for num in range(1, 10):
                sudoku2 = row_pots_list(num, row, cols, sudoku2)
    return sudoku2


def box_cols_reduction(sudoku):
    sudoku2 = column_remover(sudoku)
    for cols in range(9):
        for row in [0, 3, 6]:
            for num in range(1, 10):
                sudoku2 = col_pots_list(num, row, cols, sudoku2)

    return sudoku2


def box_line_reduction(sudoku):
    sudoku2 = box_row_reduction(sudoku)
    sudoku3 = box_cols_reduction(sudoku2)

    puzzle_reduced = list_to_int(sudoku3)

    return puzzle_reduced


# THIS ISNT NEEDED SAME REASON AS INITIAL STEP
'''
def intersection(puzzle):
    same = False

    initial_step(puzzle)

    while same == False:

        puzzle_copy = copy.deepcopy(puzzle)

        initial_step(puzzle)
        pointing_reduction(puzzle)
        box_line_reduction(puzzle)

        if puzzle_copy == puzzle:
            same = True

    return puzzle
'''


# ADD IN EVERYONE ELSE'S FUNCTIONS HERE
###

# REPLACES INITIAL STEP
def simple_elim(puzzle):
    row_remover(puzzle)
    list_to_int(puzzle)
    column_remover(puzzle)
    list_to_int(puzzle)
    box_remover(puzzle)
    list_to_int(puzzle)
    return puzzle


# THESE ARE THE LOOPS CALLING YOUR FUNCTIONS CHECK FUNCTIONS FINISH WITH A LIST TO INTEGER/INCLUDE IN HERE
def main_loop(puzzle):
    puzzle_copy = copy.deepcopy(puzzle)
    puzzle = simple_elim(puzzle)
    if not puzzle_copy == puzzle:
        main_loop(puzzle)
    else:
        puzzle_copy = copy.deepcopy(puzzle)
        puzzle = box_line_reduction(puzzle)
        if not puzzle_copy == puzzle:
            main_loop(puzzle)
        else:
            puzzle_copy = copy.deepcopy(puzzle)
            puzzle = pointing_reduction(puzzle)

            if not puzzle_copy == puzzle:
                main_loop(puzzle)
            '''else:
                puzzle_copy = copy.deepcopy(puzzle)
                naked_pairs_elimination(puzzle)            
                if not puzzle_copy == puzzle:
                    main_loop(puzzle)
                else: etcetcetc'''
    return puzzle


# CHECK IF SOLVED
def is_solved(puzzle):
    for i in range(9):
        for j in range(9):
            if is_list(puzzle[i][j]):
                return False
    return True


# IF NOT SOLVED RUN THIS TO RETURN THE LISTS AS 0'z
def failed_sudoku(puzzle):
    for i in range(9):
        for j in range(9):
            if is_list(puzzle[i][j]):
                puzzle[i][j] = 0
    return puzzle


# FINAL FUNCTION
def sudoku_solver(puzzle):
    puzzle = convert_to_listed(puzzle)
    puzzle = main_loop(puzzle)
    return puzzle


print("Enter your sudoku puzzle row by row, with a space between entries. (Write 0 for an empty cell). ")
sudoku = []
for i in range(9):
    istr = str(i + 1)
    b = input('Enter row number ' + istr + ' : ' )
    numbers = b.split(' ')
    row = [int(i) for i in numbers]
    sudoku.append(row)

print('This is your inputted sudoku: ')
for i in range(9):
    print(sudoku[i])
puzzle1 = sudoku_solver(sudoku)
if is_solved(puzzle1):
    print("Here is your solved puzzle: ")
    for i in range(9):
        print(puzzle1[i])
else:
    print("I was unable to solve your puzzle. This is as far as I could solve it: ")
    puzzle2 = failed_sudoku(puzzle1)
    for i in range(9):
        print(puzzle2[i])
