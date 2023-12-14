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
    
def list_to_int(sudoku):
    # converts cells with 1 possible candidate to that candidate
    for row in sudoku:
        for col in range(9):
            if isinstance(row[col], list) and len(row[col]) == 1:
                row[col] = row[col][0]
    return sudoku
    
def column_to_row(list_of_lists):
    # converts columns to rows
    unlisted = []
    # a list of all the entries in row order unlisted
    for row in range(len(list_of_lists)): 
        for col in range(len(list_of_lists)):
            unlisted.append(list_of_lists[col][row])
    relisted = []
    # puts entries into 9 lists of 9
    for i in range(0, len(unlisted), 9):
        relisted.append(unlisted[i:i+9])
    return relisted
                                                                                                          
def col_x_wing(sudoku):
    # same as row x-wing except with columns and rows switched
    column_to_row(row_x_wing(column_to_row(sudoku)))
    return sudoku
