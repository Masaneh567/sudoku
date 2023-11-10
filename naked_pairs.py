#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 15:19:05 2023

@author: miaglynn
"""

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
        convert_to_listed(sudokucopy)
        row_remover(sudokucopy)
        column_remover(sudokucopy)
        remove_by_grid(sudokucopy)
        list_to_int(sudokucopy)

        if sudokucopy == previous_state:
            solved = True
        # Check if the Sudoku has changed after applying the functions

    return  sudokucopy

        
# Find The naked pairs by row (input has to be the row)

def find_naked_pairs_rows(row):
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

# Applies find_naked_pairs_rows to each row in the sudoku then removes them 
# from any lists that are not the naked pairs themselves 

def naked_pairs_rows(sudoku):
    sudokucopy = copy.deepcopy(sudoku)
    
    for row in sudokucopy:
        naked_pair = find_naked_pairs_rows(row)
        
        for col in row:
            
            if is_list(naked_pair):
             
                for x in naked_pair:
                   
                     if is_list(col) and len(col) > 2:
                        
                         for x in naked_pair:
                            
                             if x in col:
                                col.remove(x)\
                                    
                     if is_list(col) and len(col) == 2:
                         
                         if col[0] not in naked_pair or col[1] not in naked_pair:
                            
                             for x in naked_pair:
                                
                                 if x in col:
                                    col.remove(x)
   
    return list_to_int(sudokucopy)   
  
first = test_1(puzzle) 
print(naked_pairs_rows(first))









