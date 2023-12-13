def find_columns(row, n):
    # returns list of columns of which n is a candidate in a given row
    columns = []
    for col, cell in enumerate(row):
        if isinstance(cell, list):
            for value in cell:
                if value == n:
                    columns.append(col)
    return columns

def two_possible_cell_check(row, n):
    # returns true if n is a candidate in exactly 2 cells in a row
    count = 0
    for col in range(9):
        if not isinstance(row[col], int):
            for value in row[col]:
                if value == n:
                    count += 1
    return count == 2

def find_second_row(sudoku, n, row1, columns):
    # returns a second row in which n is a candidate in the same columns as the first row
    for index, row in enumerate(sudoku):
        # second row must also only have 2 cells being candidates for n
        if index != row1:
            if not isinstance(row[columns[0]], int):
                if not isinstance(row[columns[1]], int):
                    if find_columns(row, n) == columns:
                        if two_possible_cell_check(row, n) == True:
                            return index
                        
def perform_x_wing(sudoku, n, row1, row2, col1, col2):    
    # removes candidate from cells in each row in given columns except for 2 rows in x-wing
    for index, row in enumerate(sudoku):
        if index != row1:
            if index != row2:
                if not isinstance(row[col1], int):
                    if n in row[col1]:
                        row[col1].remove(n)
                        if not isinstance(row[col2], int):
                            if n in row[col2]:
                                row[col2].remove(n)
    return sudoku   

def row_x_wing(sudoku):
    for index, row in enumerate(sudoku):
        # creates count tally for each value in each row
        value_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
        for col in range(9):
            if not isinstance(row[col], int):
                for i in row[col]:
                    value_counts[i] += 1
        for value, count in value_counts.items():
            # when count is 2, looks for second row where count is also 2 in same columns
            if count == 2:
                columns = find_columns(row, value)
                second_row = find_second_row(sudoku, value, index, columns)
                if second_row is not None:
                    perform_x_wing(sudoku, value, index, second_row, columns[0], columns[1])
    return sudoku
