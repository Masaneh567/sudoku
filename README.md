#An easy level sudoku from the sudoku app
puzzle = [[6, 5, 0, 0, 0, 3, 2, 4, 7],
          [4, 0, 0, 0, 0, 7, 0, 0, 0],
          [9, 0, 7, 2, 5, 0, 0, 0, 3],
          [2, 0, 0, 3, 0, 0, 0, 8, 1],
          [0, 0, 1, 7, 0, 6, 4, 0, 9],
          [7, 0, 3, 8, 9, 0, 5, 2, 0],
          [0, 6, 0, 0, 0, 9, 3, 0, 0],
          [3, 7, 4, 0, 0, 0, 9, 0, 0],
          [1, 0, 9, 0, 0, 0, 0, 0, 4]]

#Function to replace zeros (numbers to be solved) with a list 1-9 for what numbers it could be
def convert_to_listed(puzzle):
    for row in puzzle:
        for num in range(9):
            if row[num] == 0:
                row[num] = list(range(1,10))
    return puzzle

#Just a function I used to help other functions
def is_list(x):
    if type(x) is list:
        return True
    else:
        return False

#remove by row function
def row_remover(sudoku):
    for row in sudoku:
        for x in range(9):
            if is_list(row[x]):
                for y in range(9):
                    if not is_list(row[y]) and row[y] in row[x]:
                        row[x].remove(row[y])
    return sudoku

#remove by column function
def column_remover(sudoku):
    for row in sudoku:
        for x in range(9):
            if is_list(row[x]):
                for y in range(9):
                    if not is_list(sudoku[y][x]) and sudoku[y][x] in row[x]:
                        row[x].remove(sudoku[y][x])
    return sudoku

#remove by grid function
def remove_by_grid(sudoku):
    for y in range(9):
        for x in range(9):
            if is_list(sudoku[y][x]):
                r = (x // 3) * 3
                p = (y // 3) * 3
                for n in range(r, r+3):
                    for m in range(p, p+3):
                        if not is_list(sudoku[m][n]) and sudoku[m][n] in sudoku[y][x]:
                            sudoku[y][x].remove(sudoku[m][n])
    return sudoku

#convert one letter lists to just integers
def list_to_int(sudoku):
    for row in sudoku:
        for x in range(9):
            if is_list(row[x]) and len(row[x]) == 1:
                row[x] = row[x][0]
    return sudoku

#Will run this in probably a while loop, but this solves the sudoku given at the top
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
