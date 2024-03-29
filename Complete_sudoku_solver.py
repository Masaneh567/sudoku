import copy


# INITIAL STEPS CODE

def convert_to_listed(puzzle):
    for row in puzzle:
        for cols in range(9):
            if row[cols] == 0:
                row[cols] = list(range(1, 10))

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced


def is_list(x):
    return type(x) == list


def list_to_int(puzzle):
    for row in puzzle:
        for cols in range(9):
            if is_list(row[cols]) and len(row[cols]) == 1:
                row[cols] = row[cols][0]
    return puzzle

# INITIAL STEPS CODE END


# SIMPLE ELIM CODE

# remove by row function
# rowcols is to look for list of potentials, rowcols2 is the numbers already given/solved in the sudoku to remove from
# list of potentials
def row_remover(puzzle):
    for row in puzzle:
        for cols in range(9):
            # if it is a list then...
            if is_list(row[cols]):
                # go through 0-8
                for cols2 in range(9):
                    # [row, col2] is not a list and [row,col2] is in the list [row,col]...
                    if not is_list(row[cols2]) and row[cols2] in row[cols]:
                        # remove the element from the list
                        row[cols].remove(row[cols2])

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced


def column_remover(puzzle):
    for row in puzzle:
        for cols in range(9):
            # if it is a list then...
            if is_list(row[cols]):
                # hold that list and look through the rest of the column
                for row2 in range(9):
                    # if the element in the column is not a list and the element in the column appears in the list,
                    # then remove it from the list.
                    if not is_list(puzzle[row2][cols]) and puzzle[row2][cols] in row[cols]:
                        row[cols].remove(puzzle[row2][cols])

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced


# remove by grid function
# rowcols is to look for list of potentials, n is the column index and m is the box index to check each square for
# numbers already given/solved to remove from list of potentials
def box_remover(puzzle):
    for row in range(9):
        for cols in range(9):
            if is_list(puzzle[row][cols]):
                # if its a list
                rcols = (cols // 3) * 3
                rrow = (row // 3) * 3
                # seperate into 3 groups, col 1 goes to 0 col 2 goes to 0 col 9 goes to 2 etc
                # same for rows
                # times by 3, so 0 goes to 0, 1 goes to 3, 2 goes to 6
                for n in range(rcols, rcols + 3):
                    # 0,3
                    # 3,6
                    # 6,9
                    for m in range(rrow, rrow + 3):
                        if not is_list(puzzle[m][n]) and puzzle[m][n] in puzzle[row][cols]:
                            puzzle[row][cols].remove(puzzle[m][n])

    puzzle_reduced = list_to_int(puzzle)

    return puzzle_reduced

def simple_elim(puzzle):
    row_remover(puzzle)
    list_to_int(puzzle)
    column_remover(puzzle)
    list_to_int(puzzle)
    box_remover(puzzle)
    list_to_int(puzzle)
    print('Simple_Elimination')
    return puzzle

# SIMPLE ELIM CODE END

# INTERSECTION CODE

def pointing_rows(puzzle2, row, col, num):
    
    # INDEXING
    box_col = (col // 3) * 3
    box_row = (row // 3) * 3

    index = []
    for i in range(9):
        index.append(i)

    index.remove(box_col)
    index.remove(box_col + 1)
    index.remove(box_col + 2)
    
    # BOX MUST BE REDUCED FOR IT TO WORK
    # ROW MUST BE REDUCED FOR IT TO WORK
    puzzle1 = box_remover(puzzle2)
    puzzle = row_remover(puzzle1)

    # how many times num appears in lists inside that box
    box_count = 0

    #for the box we are in
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            #if it is a list and the number we are looking for is in that list
            if is_list(puzzle[i][j]) and num in puzzle[i][j]:
                #add 1 to box count
                box_count += 1

    # how many times num appears in lists in that box in that row
    row_box_count = 0

    #for the box we are in
    for i in range(box_col, box_col + 3):
        if is_list(puzzle[row][i]) and num in puzzle[row][i]:
            row_box_count += 1

    if box_count == row_box_count and box_count != 0:
        for i in index:
            if is_list(puzzle[row][i]) and num in puzzle[row][i]:
                puzzle[row][i].remove(num)

    return puzzle


def pointing_cols(puzzle2, row, col, num):
    box_col = (col // 3) * 3
    box_row = (row // 3) * 3

    index = []
    for i in range(9):
        index.append(i)

    index.remove(box_row)
    index.remove(box_row + 1)
    index.remove(box_row + 2)
    
    # BOX MUST BE REDUCED FOR IT TO WORK
    # COL MUST BE REDUCED FOR IT TO WORK
    puzzle1 = box_remover(puzzle2)
    puzzle = row_remover(puzzle1)

    # how many times num appears in lists inside that box
    box_count = 0

    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if is_list(puzzle[i][j]) and num in puzzle[i][j]:
                box_count += 1

    # how many times num appears in lists in that box in that column
    col_box_count = 0

    for i in range(box_row, box_row + 3):
        if is_list(puzzle[i][col]) and num in puzzle[i][col]:
            col_box_count += 1

    if box_count == col_box_count and box_count != 0:
        for i in index:
            if is_list(puzzle[i][col]) and num in puzzle[i][col]:
                puzzle[i][col].remove(num)

    return puzzle


def pointing_rows_reduction(puzzle):
    puzzle_reduced = box_remover(puzzle)

    for row in range(9):
        for col in range(9):
            for num in range(1, 10):
                puzzle_reduced2 = pointing_rows(puzzle_reduced, row, col, num)

    puzzle_reduced3 = list_to_int(puzzle_reduced2)

    return puzzle_reduced3


def pointing_cols_reduction(puzzle):
    puzzle_reduced = box_remover(puzzle)

    for row in range(9):
        for col in range(9):
            for num in range(1, 10):
                puzzle_reduced2 = pointing_cols(puzzle_reduced, row, col, num)

    puzzle_reduced3 = list_to_int(puzzle_reduced2)

    return puzzle_reduced3


def pointing_reduction(puzzle):
    puzzle_reduced1 = pointing_rows_reduction(puzzle)
    puzzle_reduced2 = pointing_cols_reduction(puzzle_reduced1)

    puzzle_reduced3 = list_to_int(puzzle_reduced2)
    print('Pointing_Reduction')

    return puzzle_reduced3


def row_pots_list(num, row, cols, sudoku1):
    sudoku = row_remover(sudoku1)
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


def col_pots_list(num, row, cols, sudoku1):
    sudoku = column_remover(sudoku1)
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

    for row in range(9):
        for cols in [0, 3, 6]:
            for num in range(1, 10):
                sudoku2 = row_pots_list(num, row, cols, sudoku)
    return sudoku2


def box_cols_reduction(sudoku):
    
    for cols in range(9):
        for row in [0, 3, 6]:
            for num in range(1, 10):
                sudoku2 = col_pots_list(num, row, cols, sudoku)

    return sudoku2

def box_line_reduction(sudoku):
    sudoku2 = box_row_reduction(sudoku)
    sudoku3 = box_cols_reduction(sudoku2)

    puzzle_reduced = list_to_int(sudoku3)
    print('Box_Line_Reduction')

    return puzzle_reduced

# INTERSECTION CODE END

# ADD IN EVERYONE ELSE'S FUNCTIONS HERE
###

# X-WINGS CODE

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

def x_wings(sudoku):
    sudoku2 = row_x_wing(sudoku)
    sudoku3 = col_x_wing(sudoku2)

    puzzle_reduced = list_to_int(sudoku3)
    print('X-Wings')

    return puzzle_reduced


# X-WINGS CODE END

# HIDDEN SINGLES CODE

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

def hidden_singles_elimination(sudoku):
        
    sudoku2 = confirm_row_hidden_singles(sudoku)
    sudoku3 = confirm_column_hidden_singles(sudoku2)
    sudoku4 = confirm_grid_hidden_singles(sudoku3)

    puzzle_reduced = list_to_int(sudoku4)
    print('Hidden_Singles_Elimination')
    
    return puzzle_reduced
    

# HIDDEN SINGLES CODE END


# NAKED PAIRS CODE

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

def naked_pairs_elimination(sudoku):
    
    sudoku2 = naked_pairs_rows(sudoku)
    sudoku3 = naked_pairs_cols(sudoku2)
    sudoku4 = naked_pairs_grids(sudoku3)

    puzzle_reduced = list_to_int(sudoku4)
    print('Naked_Pairs_Elimination')

    return puzzle_reduced

# NAKED PAIRS END

# BACKTRACKER

def is_sudoku_solved(sudoku):
    
    solved = True  # Assume the Sudoku is solved until proven otherwise
    
    for row in sudoku:
        
        for col in row:

            if is_list(col) or col == 0:
                solved = False

    return solved
                

def find_empty_location(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0 or is_list(sudoku[i][j]):
                return i, j
    return None

def is_valid_guess(sudoku, row, col, num):
    for i in range(9):
        if sudoku[row][i] == num or sudoku[i][col] == num or sudoku[(row // 3) * 3 + i // 3][(col // 3) * 3 + i % 3] == num:
            return False
    return True

def backtracker(sudoku):
    print("Backtracker")
    if is_sudoku_solved(sudoku):
        return sudoku

    empty_location = find_empty_location(sudoku)
    
    if empty_location:
        row, col = empty_location

        for num in sudoku[row][col]:
           
            if is_valid_guess(sudoku, row, col, num):
                sudoku_copy = copy.deepcopy(sudoku)
                sudoku_copy[row][col] = num
                
                result = backtracker(sudoku_copy)  
                if is_sudoku_solved(result):
                    for i in range(9):
                        for j in range(9):
                            sudoku[i][j] = sudoku_copy[i][j]
    
                    return sudoku

    return sudoku

# BACKTRACKER CODE END

# MAIN LOOP CODE

# THESE ARE THE LOOPS CALLING YOUR FUNCTIONS CHECK FUNCTIONS FINISH WITH A LIST TO INTEGER/INCLUDE IN HERE
def main_loop(puzzle):
    puzzle_copy = copy.deepcopy(puzzle)
    puzzle = simple_elim(puzzle)
    if not puzzle_copy == puzzle:
        main_loop(puzzle)
        
    else:
        puzzle_copy = copy.deepcopy(puzzle)
        hidden_singles_elimination(puzzle)
        if not puzzle_copy == puzzle:
            main_loop(puzzle)
        else:
            puzzle_copy = copy.deepcopy(puzzle)
            naked_pairs_elimination(puzzle) 
            if not puzzle_copy == puzzle:
                main_loop(puzzle)
            else:
                puzzle_copy = copy.deepcopy(puzzle)
                puzzle = box_line_reduction(puzzle)
                if not puzzle_copy == puzzle:
                    main_loop(puzzle)
                else:
                    puzzle_copy = copy.deepcopy(puzzle)
                    puzzle = pointing_reduction(puzzle)
                    if not puzzle_copy == puzzle:
                        main_loop(puzzle)
                        
                    else:
                        puzzle_copy = copy.deepcopy(puzzle)
                        puzzle = x_wings(puzzle)
                        if not puzzle_copy == puzzle:
                            main_loop(puzzle)
                        else:
                            puzzle_copy = copy.deepcopy(puzzle)
                            backtracker(puzzle) 
                            if not puzzle_copy == puzzle:
                                main_loop(puzzle)
                                '''else: etc'''
                
    return puzzle


# CHECK IF SOLVED
def is_solved(puzzle):
    for i in range(9):
        for j in range(9):
            if is_list(puzzle[i][j]):
                return False
    return True


# IF NOT SOLVED RUN THIS TO RETURN THE LISTS AS 0'z
def failed_sudoku(puzzle):
    for i in range(9):
        for j in range(9):
            if is_list(puzzle[i][j]):
                puzzle[i][j] = 0
    return puzzle


# FINAL FUNCTION
def sudoku_solver(puzzle):
    puzzle = convert_to_listed(puzzle)
    puzzle = main_loop(puzzle)
    return puzzle

# MAIN LOOP CODE END


# TESTING CODE

# This code is purely for testing purposes and is not used at all in the final
# product.

# When using the testing code please comment out the UI code before using.

# When not using the testing code please comment out like it is now.

'''

def test_loop(puzzle):
    
    same = False
    
    while same == False:
        
        puzzle_copy = copy.deepcopy(puzzle)
        print(puzzle)
        puzzle1 = convert_to_listed(puzzle)
        # INSERT THE FUNCTION YOU WANT TO TEST LOOP BELOW
        puzzle2 = simple_elim(puzzle1)
        puzzle3 = pointing_reduction(puzzle2)
        puzzle4 = box_line_reduction(puzzle3)
        puzzle5 = hidden_singles_elimination(puzzle4)
        puzzle6 = naked_pairs_elimination(puzzle5)
        
        if puzzle6 == puzzle_copy:
            same = True
            
    return puzzle

# This is a solvable sudoku that can be used for testing purposes
sudoku =[[4, 0, 0, 0, 0, 0, 9, 3, 8],
          [0, 3, 2, 0, 9, 4, 1, 0, 0],
          [0, 9, 5, 3, 0, 0, 2, 4, 0],
          [3, 7, 0, 6, 0, 9, 0, 0, 4],
          [5, 2, 9, 0, 0, 1, 6, 7, 3],
          [6, 0, 4, 7, 0, 3, 0, 9, 0],
          [9, 5, 7, 0, 0, 8, 3, 0, 0],
          [0, 0, 3, 9, 0, 0, 4, 0, 0],
          [2, 4, 0, 0, 3, 0, 7, 0, 9]]

print('This is your inputted sudoku: ')
for i in range(9):
    print(sudoku[i])
    
puzzle = convert_to_listed(sudoku)
puzzle_complete = test_loop(puzzle)

print("Here is your solved puzzle: ")
for i in range(9):
    print(puzzle_complete[i])

# TESTING CODE END
'''

# USER INTERFACE CODE

print("Enter your sudoku puzzle row by row, with a space between entries. (Write 0 for an empty cell). ")
sudoku = []
for i in range(9):
    istr = str(i + 1)
    b = input('Enter row number ' + istr + ' : ' )
    numbers = b.split(' ')
    row = [int(i) for i in numbers]
    sudoku.append(row)
    

print('This is your inputted sudoku: ')
for i in range(9):
    print(sudoku[i])
puzzle1 = sudoku_solver(sudoku)
if is_solved(puzzle1):
    print("Here is your solved puzzle: ")
    for i in range(9):
        print(puzzle1[i])
else:
    print("I was unable to solve your puzzle. This is as far as I could solve it: ")
    for i in range(9):
        print(puzzle1[i])
    print("This is as far as i could solve it, replacing all lists with 0's")
    puzzle2 = failed_sudoku(puzzle1)
    for i in range(9):
        print(puzzle2[i])

# USER INTERFACE CODE END
