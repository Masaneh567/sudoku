import copy
from itertools import product

# x-wingable sudoku from https://www.sudokuwiki.org/X_Wing_Strategy
puzzle = [[1,[3,7,8],[3,7],[2,3,4,7,8],[2,7,8],[2,3,4,7,8],5,6,9],
          [4,9,2,[3,7],5,6,1,[3,7],8],
          [[3,7,8],5,6,1,[7,8],9,2,4,[3,7]],
          [[3,5,7],[3,7],9,6,4,[2,7],8,[2,5],1],
          [[5,7],6,4,[2,7,8,9],1,[2,7,8],[3,7,9],[2,5],[3,7]],
          [2,1,8,[7,9],3,5,6,[7,9],4],
          [[3,7,8],4,[3,7],5,[2,7,8,9],[2,3,7,8],[3,7,9],1,6],
          [9,[3,7,8],5,[3,7,8],6,1,4,[3,7,8],2],
          [6,2,1,[3,4,7,8],[7,8,9],[3,4,7,8],[3,7,9],[3,7,8,9],5]]
          
def convert_to_listed(sudoku):
    for row in sudoku:
        for col in range(9):
            if row[col] == 0:
                row[col] = list(range(1,10))
    return sudoku

def is_list(x):
   if type(x) is list:
       return True
   else:
       return False          
            
def list_to_int(sudoku):
    for row in sudoku:
        for col in range(9):
            if is_list(row[col]) and len(row[col]) == 1:
                row[col] = row[col][0]
    return sudoku
    
def column_to_row(list_of_lists):
    unlisted = []
    # a list of all the entries in row order unlisted
    for row in range(len(list_of_lists)): 
        for col in range(len(list_of_lists)):
                unlisted.append(list_of_lists[col][row])
    relisted = []
    # putting entries into 9 lists of 9
    for i in range(0, len(unlisted), 9):
        relisted.append(unlisted[i:i+9])
    return relisted

def find_columns(row, n):
    # returns list of columns of which n is a candidate in a given row
    columns = []
    for i, cell in enumerate(row):
        if isinstance(cell, list):
            for value in cell:
                if value == n:
                    columns.append(i)
    return columns

def two_poss_value_check(row, n):
    # returns true if n is a candidate in exactly 2 cells in a row
    count = 0
    for col in range(9):
        if isinstance(row[col], list):
            for n in row[col]:
                count += 1
    return count == 2

def find_second_row(sudoku, n, row1, columns):
    # returns a second row in which n is a candidate in the same columns as the first row
    for index, row in enumerate(sudoku):
        # second row must also only have 2 cells being candidates for n
        if index != row1:
            if two_poss_value_check(row, n) and find_columns(row, n) == columns:
                return index
        
def find_x_wing(sudoku):
    # returns list of candidates and co-ordinates of x-wing
    candidates = []
    row1 = []
    row2 = []
    col1 = []
    col2 = []
    for row in sudoku:
        # creates count tally for each value in each row
        value_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
        for col in range(9):
            if isinstance(row[col], list):
                for i in row[col]:
                    value_counts[i] += 1
        for value, count in value_counts.items():
            # x-wing only applicable when value is a candidate in exactly 2 cells
            if count == 2:
                columns = find_columns(row, value)
                second_row = find_second_row(sudoku, value, row, columns)
                
                if second_row is not None:                
                    candidates.append(value)
                    row1.append(row)
                    row2.append(second_row)
                    col1.append(columns[0])
                    col2.append(columns[1])
    return candidates, row1, row2, col1, col2
                   
def row_x_wing(sudoku):
    candidates, row1, row2, col1, col2 = find_x_wing(sudoku)
    
    # if no x-wing candidates, returns original sudoku
    if candidates is None:
        return sudoku
    
    # removes candidate from cells in each row in given columns except for rows in x-wing
    for n, r1, r2, c1, c2 in product(candidates, row1, row2, col1, col2):
        for row in sudoku:
            if row != r1 or row != r2:
                if n in row[c1]:
                    row[c1].remove(n)
                    if n in row[c2]:
                        row[c2].remove(n)
    return sudoku
                                                                                                          
def col_x_wing(sudoku):
    # same as row x-wing except with columns and rows switched
    column_to_row(row_x_wing(column_to_row(sudoku)))
    return sudoku

def test_1(sudoku):
    sudokucopy = copy.deepcopy(sudoku)
    solved = False  # Initializing the while loop
    # times_looped = 0
    while solved == False:
        # times_looped = times_looped+1 #added this for interest to see how many iterations it takes.
        # Save the current state of the Sudoku before making any changes
        # previous_state = copy.deepcopy(sudoku)

        previous_state = [row[:] for row in sudokucopy] # slicing allows to make copies without altering the original code

        # Apply your solving functions repeatedly until no more changes are made
        # convert_to_listed(sudokucopy)
        row_x_wing(sudokucopy)
        # col_x_wing(sudokucopy)
        # list_to_int(sudokucopy)
        if sudokucopy == previous_state:
            solved = True
        # Check if the Sudoku has changed after applying the functions
        
    return sudokucopy
    

first = test_1(puzzle) 
print(test_1(first))

