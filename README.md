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


#convert one letter lists to just integers
def list_to_int(sudoku):
    for row in sudoku:
        for x in range(9):
            if is_list(row[x]) and len(row[x]) == 1:
                row[x] = row[x][0]
    return sudoku

first_round = list_to_int(column_remover(row_remover(convert_to_listed(puzzle))))
print(first_round)
second_round = list_to_int(column_remover(row_remover(first_round)))
print(second_round)
third_round = list_to_int(column_remover(row_remover(second_round)))
print(third_round)
fourth_round = list_to_int(column_remover(row_remover(third_round)))
print(fourth_round)
fifth_round = list_to_int(column_remover(row_remover(fourth_round)))
print(fifth_round)
