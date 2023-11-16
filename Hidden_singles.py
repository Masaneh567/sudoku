#!/usr/bin/env python
# coding: utf-8

# In[3]:



import numpy as np

def is_list(x): #used to identif if an item is a list or not
   if type(x) is list:
       return True
   else:
       return False


def add_first_candidates(sudoku):

   for box in sudoku:
       for i in range(9):
           if box[i] == 0:

                      box[i] = list(range(1,10))
   return sudoku






# In[4]:


def remove_by_row(sudoku): #removing cancidates if they appear in a row not sure i like the enumerate thing.

    for row in sudoku:
        for cell_idx, cell in enumerate(row):
            if is_list(cell):
                for other_idx, other_cell in enumerate(row):
                    if not is_list(other_cell) and other_cell in cell:
                        cell.remove(other_cell)

    return sudoku




# In[5]:


def column_remover(sudoku):


    for x in range(9):
        for y in range(9):
            if is_list(sudoku[y][x]):
                for z in range(9):
                    if not is_list(sudoku[z][x]) and sudoku[z][x] in sudoku[y][x]:
                        sudoku[y][x].remove(sudoku[z][x])
    return sudoku


# In[6]:


def remove_by_grid(sudoku):

    for y in range(9):
        for x in range(9):
            if is_list(sudoku[y][x]):
                first_grid_row = (x // 3) * 3
                first_grid_column = (y // 3) * 3
                for n in range(first_grid_row,first_grid_row+3):
                    for m in range(first_grid_column, first_grid_column+3):
                        if not is_list(sudoku[m][n]) and sudoku[m][n] in sudoku[y][x]:
                            sudoku[y][x].remove(sudoku[m][n])
    return sudoku


# In[7]:


def list_to_int(sudoku):
    for row in sudoku:
        for x in range(9):
            if is_list(row[x]) and len(row[x]) == 1:
                row[x] = row[x][0]
    return sudoku


# In[118]:


import copy
def test_1(sudoku):
    solved = False  # Initializing the while loop
    times_looped = 0
    while solved == False:
        times_looped = times_looped+1 #added this for interest to see how many iterations it takes.
        # Save the current state of the Sudoku before making any changes
        #previous_state = copy.deepcopy(sudoku)

        previous_state = [row[:] for row in sudoku] # slicing allows to make copies without altering the original code

        # Apply your solving functions repeatedly until no more changes are made
        add_first_candidates(sudoku)
        remove_by_row(sudoku)
        column_remover(sudoku)
        remove_by_grid(sudoku)
        confirm_row_hidden_singles(sudoku)
        list_to_int(sudoku)

        if sudoku == previous_state:
            solved = True
        # Check if the Sudoku has changed after applying the functions

    return times_looped , sudoku





# In[10]:


print(sudoku)


# In[111]:


easy_sudoku=[[6, 5, 0, 0, 0, 3, 2, 4, 7],
             [4, 0, 0, 0, 0, 7, 0, 0, 0],
             [9, 0, 7, 2, 5, 0, 0, 0, 3],
             [2, 0, 0, 3, 0, 0, 0, 8, 1],
             [0, 0, 1, 7, 0, 6, 4, 0, 9],
             [7, 0, 3, 8, 9, 0, 5, 2, 0],
             [0, 6, 0, 0, 0, 9, 3, 0, 0],
             [3, 7, 4, 0, 0, 0, 9, 0, 0],
             [1, 0, 9, 0, 0, 0, 0, 0, 4]]


# In[104]:






def confirm_row_hidden_singles(sudoku):
    for row in sudoku:
        for x in range(9):
            if is_list(row[x]):
                freq_unique_candidates = []
                for y in range(9):

                    unique_candidate_in_list = [candidate for candidate in row[x] if isinstance(row[y], list) and candidate not in row[y] or isinstance(row[y], int) and candidate != row[y]]
                    #print(unique_candidate_in_list)
                    freq_unique_candidates.extend(unique_candidate_in_list)
                #if len(unique_candidate_in_list) == 1:
                    #row[x] = unique_candidate_in_list
                #print(unique_candidate_in_list)


                candidate_count = {}
                for candidate in freq_unique_candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                    else:

                        candidate_count[candidate] = 1

    # Find the element with a count of 8 , this is becasue the way ive set it up an element which is unique compared to another element in the row it will be added to a list, so if it appears 8 times then it is unique to the row entirely.
                unique_candidate = None
                for candidate, count in candidate_count.items():
                    if count == 8:
                        if unique_candidate is None:
                            unique_candidate = candidate
                        else:
                            unique_candidate = None
                            break




            # If there is more than one candidate counted 8 times, exit the loop
                if unique_candidate is not None:
                    row[x]=unique_candidate
    return sudoku








# In[105]:


confirm_row_hidden_singles(sudoku_puzzle)


# In[110]:


sudoku_puzzle_harder = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 8, 5],
    [0, 0, 1, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 7, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 1, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 0, 7, 3],
    [0, 0, 2, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 9]
]



test_1(sudoku_puzzle_harder)


# In[119]:



]
) #harder sudoku to test code with, this cannot be solved by simple elimination.


# In[ ]:  

def confirm_column_hidden_singles(sudoku):  # removes hidden singles by column 
    for x in range(9):
        for y in range(9):
            if is_list(sudoku[y][x]): 
                freq_unique_candidates = [] 
                for j in range(9): 
                    unique_candidate_in_list = [candidate for candidate in sudoku[y][x] if isinstance(sudoku[j][x], list) and candidate not in sudoku[j][x] or isinstance(sudoku[j][x], int) and candidate != sudoku[j][x]]
                    freq_unique_candidates.extend(unique_candidate_in_list) 
                    
                    
                candidate_count = {}
                for candidate in freq_unique_candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                    else:
           
                        candidate_count[candidate] = 1

    # Find the element with a count of 8 , this is becasue the way ive set it up an element which is unique compared to another element in the row it will be added to a list, so if it appears 8 times then it is unique to the row entirely. 
                unique_candidate = None
                for candidate, count in candidate_count.items():
                    if count == 8:
                        if unique_candidate is None:
                            unique_candidate = candidate 
                        else: 
                            unique_candidate = None 
                            break
                    
                         
                        
                        
            # If there is more than one candidate counted 8 times, exit the loop
                if unique_candidate is not None:
                    sudoku[y][x] = unique_candidate 
                    
    return sudoku 




def confirm_grid_hidden_singles(sudoku):   # confirms hidden singles by grid. 
    for y in range(9):
        for x in range(9):
            if is_list(sudoku[y][x]): 
                freq_unique_candidates= []
                first_grid_row = (x // 3) * 3
                first_grid_column = (y // 3) * 3
                for n in range(first_grid_row,first_grid_row+3):
                    for m in range(first_grid_column, first_grid_column+3):
                        unique_candidate_in_list = [candidate for candidate in sudoku[y][x] if isinstance(sudoku[m][n], list) and candidate not in sudoku[m][n] or isinstance(sudoku[m][n], int) and candidate != sudoku[m][n]]
                        freq_unique_candidates.extend(unique_candidate_in_list) 
                    
                candidate_count = {}
                for candidate in freq_unique_candidates:
                    if candidate in candidate_count:
                        candidate_count[candidate] += 1
                    else:
           
                        candidate_count[candidate] = 1

    # Find the element with a count of 8 , this is becasue the way ive set it up an element which is unique compared to another element in the row it will be added to a list, so if it appears 8 times then it is unique to the row entirely. 
                unique_candidate = None
                for candidate, count in candidate_count.items():
                    if count == 8:
                        if unique_candidate is None:
                            unique_candidate = candidate 
                        else: 
                            unique_candidate = None 
                            break
                    
                         
                        
                        
            # If there is more than one candidate counted 8 times, exit the loop
                if unique_candidate is not None:
                    sudoku[y][x] = unique_candidate 
                    
    return sudoku



