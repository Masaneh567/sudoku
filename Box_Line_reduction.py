puzzle = [[6, 5, 0, 0, 0, 3, 2, 4, 7],
          [4, 0, 0, 0, 0, 7, 0, 0, 0],
          [9, 0, 7, 2, 5, 0, 0, 0, 3],
          [2, 0, 0, 3, 0, 0, 0, 8, 1],
          [0, 0, 1, 7, 0, 6, 4, 0, 9],
          [7, 0, 3, 8, 9, 0, 5, 2, 0],
          [0, 6, 0, 0, 0, 9, 3, 0, 0],
          [3, 7, 4, 0, 0, 0, 9, 0, 0],
          [1, 0, 9, 0, 0, 0, 0, 0, 4]]

def convert_to_listed(puzzle):
    for row in puzzle:
        for cols in range(9):
            if row[cols] == 0:
                row[cols] = list(range(1,10))
    return puzzle

def is_list(x):
    return type(x) == list

def row_remover(sudoku):
    for row in sudoku:
        for cols in range(9):
            if is_list(row[cols]):
                for cols2 in range(9):
                    if not is_list(row[cols2]) and row[cols2] in row[cols]:
                        row[cols].remove(row[cols2])
    return sudoku

def column_remover(sudoku):
    for row in sudoku:
        for cols in range(9):
            if is_list(row[cols]):
                for row2 in range(9):
                    if not is_list(sudoku[row2][cols]) and sudoku[row2][cols] in row[cols]:
                        row[cols].remove(sudoku[row2][cols])
    return sudoku

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

def list_to_int(sudoku):
    for row in sudoku:
        for cols in range(9):
            if is_list(row[cols]) and len(row[cols]) == 1:
                row[cols] = row[cols][0]
    return sudoku

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
            for num in range(1,10):
                sudoku2 = row_pots_list(num, row, cols, sudoku2)
    return sudoku2

def box_cols_reduction(sudoku):
    sudoku2 = column_remover(sudoku)
    for cols in range(9):
        for row in [0, 3, 6]:
            for num in range(1,10):

                sudoku2 = col_pots_list(num, row, cols, sudoku2)

    return sudoku2

def box_line_reduction(sudoku):
    sudoku2 = box_row_reduction(sudoku)
    sudoku3 = box_cols_reduction(sudoku2)
    return sudoku3

print(puzzle)
first_round = list_to_int(box_line_reduction(list_to_int(remove_by_grid(column_remover(row_remover(convert_to_listed(puzzle)))))))
print(first_round)
second_round = list_to_int(box_line_reduction(list_to_int(remove_by_grid(column_remover(row_remover(first_round))))))
print(second_round)
third_round = list_to_int(box_line_reduction(list_to_int(remove_by_grid(column_remover(row_remover(second_round))))))
print(third_round)
'''fourth_round = list_to_int(remove_by_grid(column_remover(row_remover(third_round))))
print(fourth_round)
fifth_round = list_to_int(remove_by_grid(column_remover(row_remover(fourth_round))))
print(fifth_round)
sixth_round = list_to_int(remove_by_grid(column_remover(row_remover(fifth_round))))
print(sixth_round)'''