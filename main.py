puzzle = [[6, 5, 0, 0, 0, 3, 2, 4, 7],
          [4, 0, 0, 0, 0, 7, 0, 0, 0],
          [9, 0, 7, 2, 5, 0, 0, 0, 3],
          [2, 0, 0, 3, 0, 0, 0, 8, 1],
          [0, 0, 1, 7, 0, 6, 4, 0, 9],
          [7, 0, 3, 8, 9, 0, 5, 2, 0],
          [0, 6, 0, 0, 0, 9, 3, 0, 0],
          [3, 7, 4, 0, 0, 0, 9, 0, 0],
          [1, 0, 9, 0, 0, 0, 0, 0, 4]]

# For variable names: row = row, cols = column, cols2 or row2 is just a second index to go through them,
# rrow and rcols are just the reset to the top left version for searching by grid

# Function to replace zeros (numbers to be solved) with a list 1-9 for what numbers it could be
def convert_to_listed(puzzle):
    for row in puzzle:
        for cols in range(9):
            if row[cols] == 0:
                row[cols] = list(range(1,10))
    return puzzle

def is_list(x):
    return type(x) == list

# remove by row function
# rowcols is to look for list of potentials, rowcols2 is the numbers already given/solved in the sudoku to remove from
# list of potentials
def row_remover(sudoku):
    for row in sudoku:
        for cols in range(9):
            if is_list(row[cols]):
                for cols2 in range(9):
                    if not is_list(row[cols2]) and row[cols2] in row[cols]:
                        row[cols].remove(row[cols2])
    return sudoku

# remove by column function
# rowcols is to look for list of potentials, row2cols is the numbers already given/solved in the sudoku to remove from
# list of potentials
def column_remover(sudoku):
    for row in sudoku:
        for cols in range(9):
            if is_list(row[cols]):
                for row2 in range(9):
                    if not is_list(sudoku[row2][cols]) and sudoku[row2][cols] in row[cols]:
                        row[cols].remove(sudoku[row2][cols])
    return sudoku

# remove by grid function
# rowcols is to look for list of potentials, n is the column index and m is the box index to check each square for
# numbers already given/solved to remove from list of potentials
def remove_by_grid(sudoku):
    for row in range(9):
        for cols in range(9):
            if is_list(sudoku[row][cols]):
                rcols = (cols // 3) * 3
                rrow = (row // 3) * 3
                for n in range(rcols, rcols+3):
                    for m in range(rrow, rrow+3):
                        if not is_list(sudoku[m][n]) and sudoku[m][n] in sudoku[row][cols]:
                            sudoku[row][cols].remove(sudoku[m][n])
    return sudoku

# convert one letter lists to just integers
def list_to_int(sudoku):
    for row in sudoku:
        for cols in range(9):
            if is_list(row[cols]) and len(row[cols]) == 1:
                row[cols] = row[cols][0]
    return sudoku
'''
first_round = list_to_int(remove_by_grid(column_remover(row_remover(convert_to_listed(puzzle)))))
print(first_round)
second_round = list_to_int(remove_by_grid(column_remover(row_remover(first_round))))
print(second_round)
third_round = list_to_int(remove_by_grid(column_remover(row_remover(second_round))))
print(third_round)
fourth_round = list_to_int(remove_by_grid(column_remover(row_remover(third_round))))
print(fourth_round)
fifth_round = list_to_int(remove_by_grid(column_remover(row_remover(fourth_round))))
print(fifth_round)
sixth_round = list_to_int(remove_by_grid(column_remover(row_remover(fifth_round))))
print(sixth_round)
'''
