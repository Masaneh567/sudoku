import copy


# INITIAL STEPS CODE

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

# INITIAL STEPS CODE END


# SIMPLE ELIM CODE

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

def simple_elim(puzzle):
    row_remover(puzzle)
    list_to_int(puzzle)
    column_remover(puzzle)
    list_to_int(puzzle)
    box_remover(puzzle)
    list_to_int(puzzle)
    print('Simple_Elimination')
    return puzzle

# SIMPLE ELIM CODE END

# INTERSECTION CODE

def pointing_rows(puzzle2, row, col, num):
    
    # INDEXING
    box_col = (col // 3) * 3
    box_row = (row // 3) * 3

    index = []
    for i in range(9):
        index.append(i)

    index.remove(box_col)
    index.remove(box_col + 1)
    index.remove(box_col + 2)
    
    # BOX MUST BE REDUCED FOR IT TO WORK
    # ROW MUST BE REDUCED FOR IT TO WORK
    puzzle1 = box_remover(puzzle2)
    puzzle = row_remover(puzzle1)

    # how many times num appears in lists inside that box
    box_count = 0

    #for the box we are in
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            #if it is a list and the number we are looking for is in that list
            if is_list(puzzle[i][j]) and num in puzzle[i][j]:
                #add 1 to box count
                box_count += 1

    # how many times num appears in lists in that box in that row
    row_box_count = 0

    #for the box we are in
    for i in range(box_col, box_col + 3):
        if is_list(puzzle[row][i]) and num in puzzle[row][i]:
            row_box_count += 1

    if box_count == row_box_count and box_count != 0:
        for i in index:
            if is_list(puzzle[row][i]) and num in puzzle[row][i]:
                puzzle[row][i].remove(num)

    return puzzle


def pointing_cols(puzzle2, row, col, num):
    box_col = (col // 3) * 3
    box_row = (row // 3) * 3

    index = []
    for i in range(9):
        index.append(i)

    index.remove(box_row)
    index.remove(box_row + 1)
    index.remove(box_row + 2)
    
    # BOX MUST BE REDUCED FOR IT TO WORK
    # COL MUST BE REDUCED FOR IT TO WORK
    puzzle1 = box_remover(puzzle2)
    puzzle = row_remover(puzzle1)

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
    puzzle_reduced = box_remover(puzzle)

    for row in range(9):
        for col in range(9):
            for num in range(1, 10):
                puzzle_reduced2 = pointing_rows(puzzle_reduced, row, col, num)

    puzzle_reduced3 = list_to_int(puzzle_reduced2)

    return puzzle_reduced3


def pointing_cols_reduction(puzzle):
    puzzle_reduced = box_remover(puzzle)

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
    print('Pointing_Reduction')

    return puzzle_reduced3


def row_pots_list(num, row, cols, sudoku1):
    sudoku = row_remover(sudoku1)
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


def col_pots_list(num, row, cols, sudoku1):
    sudoku = column_remover(sudoku1)
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

    for row in range(9):
        for cols in [0, 3, 6]:
            for num in range(1, 10):
                sudoku2 = row_pots_list(num, row, cols, sudoku)
    return sudoku2


def box_cols_reduction(sudoku):
    
    for cols in range(9):
        for row in [0, 3, 6]:
            for num in range(1, 10):
                sudoku2 = col_pots_list(num, row, cols, sudoku)

    return sudoku2

def box_line_reduction(sudoku):
    sudoku2 = box_row_reduction(sudoku)
    sudoku3 = box_cols_reduction(sudoku2)

    puzzle_reduced = list_to_int(sudoku3)
    print('Box_Line_Reduction')

    return puzzle_reduced

# INTERSECTION CODE END

# ADD IN EVERYONE ELSE'S FUNCTIONS HERE
###




# MAIN LOOP CODE

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

# MAIN LOOP CODE END


# TESTING CODE

# This code is purely for testing purposes and is not used at all in the final
# product.

# When using the testing code please comment out the UI code before using.

# When not using the testing code please comment out like it is now.

'''

def test_loop(puzzle):
    
    same = False
    
    while same == False:
        
        puzzle_copy = copy.deepcopy(puzzle)
        print(puzzle)
        puzzle1 = convert_to_listed(puzzle)
        # INSERT THE FUNCTION YOU WANT TO TEST LOOP BELOW
        puzzle2 = simple_elim(puzzle1)
        puzzle3 = pointing_reduction(puzzle2)
        puzzle4 = box_line_reduction(puzzle3)
        puzzle5 = hidden_singles_elimination(puzzle4)
        puzzle6 = naked_pairs_elimination(puzzle5)
        
        if puzzle6 == puzzle_copy:
            same = True
            
    return puzzle

# This is a solvable sudoku that can be used for testing purposes
sudoku =[[4, 0, 0, 0, 0, 0, 9, 3, 8],
          [0, 3, 2, 0, 9, 4, 1, 0, 0],
          [0, 9, 5, 3, 0, 0, 2, 4, 0],
          [3, 7, 0, 6, 0, 9, 0, 0, 4],
          [5, 2, 9, 0, 0, 1, 6, 7, 3],
          [6, 0, 4, 7, 0, 3, 0, 9, 0],
          [9, 5, 7, 0, 0, 8, 3, 0, 0],
          [0, 0, 3, 9, 0, 0, 4, 0, 0],
          [2, 4, 0, 0, 3, 0, 7, 0, 9]]

print('This is your inputted sudoku: ')
for i in range(9):
    print(sudoku[i])
    
puzzle = convert_to_listed(sudoku)
puzzle_complete = test_loop(puzzle)

print("Here is your solved puzzle: ")
for i in range(9):
    print(puzzle_complete[i])

# TESTING CODE END

'''

# USER INTERFACE CODE

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
    for i in range(9):
        print(puzzle1[i])
    print("This is as far as i could solve it, replacing all lists with 0's")
    puzzle2 = failed_sudoku(puzzle1)
    for i in range(9):
        print(puzzle2[i])

# USER INTERFACE CODE END






