
puzzle = [[4, 0, 0, 0, 0, 0, 9, 3, 8],
          [0, 3, 2, 0, 9, 4, 1, 0, 0],
          [0, 9, 5, 3, 0, 0, 2, 4, 0],
          [3, 7, 0, 6, 0, 9, 0, 0, 4],
          [5, 2, 9, 0, 0, 1, 6, 7, 3],
          [6, 0, 4, 7, 0, 3, 0, 9, 0],
          [9, 5, 7, 0, 0, 8, 3, 0, 0],
          [0, 0, 3, 9, 0, 0, 4, 0, 0],
          [2, 4, 0, 0, 3, 0, 7, 0, 9]]

import copy

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
    if type(x) is list:
        return True
    else:
        return False

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
def grid_remover(sudoku):
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

# performs simple elimination until it cannot make further changes

def simple_elimination(sudoku):
    
    sudoku_copied = copy.deepcopy(sudoku)
    
    convert_to_listed(sudoku_copied)
    
    same = False
    
    while same == False:
        
        sudoku_original = copy.deepcopy(sudoku_copied)
    
        row_remover(sudoku_copied)
        column_remover(sudoku_copied)
        grid_remover(sudoku_copied)
        
        if sudoku_original == sudoku_copied:
            same = True
            
    return list_to_int(sudoku_copied)

        
# Find The naked pairs by row (input has to be the row)

def find_naked_pairs(row):
    pairs = []
    nakedpairs = []
    
    for col in range(9):
        
        if is_list(row[col]) and len(row[col]) == 2:
                    pairs.append(row[col])
                    
                    for i in range(len(pairs)):
                        
                        for j in range(i + 1, len(pairs)):
                            
                            if pairs[i] == pairs[j] and pairs[i][0] and pairs[i][1] not in nakedpairs:
                                nakedpairs.append(pairs[i][0])
                                nakedpairs.append(pairs[i][1])
                            
   
    return nakedpairs

# Applies find_naked_pairs to each row in the sudoku then removes them 
# from any lists that are not the naked pairs themselves 

def naked_pairs_rows(sudoku):
    
    for row in sudoku:
        naked_pair = find_naked_pairs(row)
        
        for col in row:
               
            if is_list(col):
                
                if len(col) > 2:
               
                    for x in naked_pair:
                       
                        if x in col:
                           col.remove(x)
                           
                if len(col) == 2:
                
                    if col[0] not in naked_pair or col[1] not in naked_pair:
                       
                        for x in naked_pair:
                           
                            if x in col:
                               col.remove(x)
   
    return list_to_int(sudoku)    

# We decided to change the sudoku columns and grids to rows so we could use 
# the same function and then convert them back

# This function changes the sudoku to a list of columns

def column_shuffle(sudoku):
    unlisted = []
    # a list of all the entries in row order unlisted
   
    for row in range(len(sudoku)): 
        
        for col in range(len(sudoku)):
                unlisted.append(sudoku[col][row])
    
    relisted = []
    # putting entries into 9 lists of 9
    
    for i in range(0, len(unlisted), 9):
        relisted.append(unlisted[i:i+9])
    
    return relisted

# This function applies naked pair elimination to columns

def naked_pairs_cols(sudoku):
   
    return column_shuffle(naked_pairs_rows(column_shuffle(sudoku)))

# This function changes the sudoku to a list of grids

def grid_shuffle(sudoku):
    rows = []
    
    for i in range(0,9,3):
        
        for j in range(0, 9, 3):
            grid_as_row = []
            
            for k in range(3):
                grid_as_row.extend(sudoku[i + k][j:j + 3])
            rows.append(grid_as_row)
    
    return rows

# This function applies naked pair elimination to grids

def naked_pairs_grids(sudoku):
    
    return grid_shuffle(naked_pairs_rows(grid_shuffle(sudoku)))

# Function to perform all versions of naked pairs until no further changes 
# can be made

def naked_pairs_elimination(sudoku):
    
    same = False
    
    while same == False:
        
        sudoku_original = copy.deepcopy(sudoku)
 
        naked_pairs_rows(sudoku)
        naked_pairs_cols(sudoku)
        naked_pairs_grids(sudoku)
        
        if sudoku_original == sudoku:
            same = True
            
    return sudoku




