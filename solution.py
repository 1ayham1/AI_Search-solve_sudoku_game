assignments = []


digits = '123456789'
rows = 'ABCDEFGHI'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

#-------------------------------------------------------------------------------------
boxes = cross(rows, digits)

row_units = [cross(r, digits) for r in rows]
column_units = [cross(rows, c) for c in digits]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#Without including Diagonal
#==================================================================
#unitlist = row_units + column_units + square_units
#units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
#peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
#==================================================================

left_Diag = [i[0]+j[0] for i,j in zip(rows, digits)]
right_Diag = [i[0]+j[0] for i,j in zip(rows, digits[::-1])] #just reverse the cols

unitlist = row_units + column_units + square_units + [left_Diag]  + [right_Diag] 
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

#For a given Box (A1) peers contain the Boxes in the same row, col, square and main diagonals

peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


#-------------------------------------------------------------------------------------




def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def del_Naked_Twins(digit,right_peers, values):
    
    import re
    
    for peer in right_peers :      
        if(len(values[peer])>2):
        #now for each Naked_Twins, eliminate their values from thier corrosponding peers.
            my_regex =  r'[' + re.escape(digit) + r"']*"
            values[peer] = re.sub(my_regex,'',values[peer])
    
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    
    
    '''
    General Stragegy:
    -----------------
    I.   FIND NAKED TWINS
            1) Iterate over all the boxes [A1--> I9]. Matrix index is stored in values.keys()
            2) For each box, get its peer. (boxes in the same row, col, square and diagonal). 
            3) Return a list of boxes where 
                a) values[box]==values[peer]
                b) values[box]==2
    II.  Eliminate NAKED TWINS
    III. Return New values dict.
     
    '''
    #---------------------------------------------------------------------------------------------------------------
    #Step 1: Finding Naked Twins Candidates. More information about the implementtion strategy is in the Readme file.
    #---------------------------------------------------------------------------------------------------------------
     
    rev_multidict = {}
    Naked_Twins = []
    
    for key, value in values.items():
        rev_multidict.setdefault(value, set()).add(key)

    shared_NT_Values = [key for key, box_list in rev_multidict.items() if len(box_list) > 1 and len(key)==2]
    
    for candidate in shared_NT_Values:
    
        box_list= list(rev_multidict[candidate])
    
        for i in range(0,len(box_list)-1):
            for j in range(i,len(box_list)):
                next_value = box_list[j]
                if(box_list[i] in peers[next_value]):
                    #print(box_list[i],next_value)
                    Naked_Twins.append([box_list[i],next_value])
                    
    
    
    #---------------------------------------    
    # Step 2: Eliminating redundent values.
    #---------------------------------------
    
    NT_boxes = Naked_Twins
    
    #This could be used in another vaiation. To be examined later.
    #flat_NT = set([item for sublist in NT_boxes for item in sublist])  
    
    for box in NT_boxes:
        
        # box is a list containing Naked Twins ['A7','B7]
        
        row1 = box[0][0]
        row2 = box[1][0]
        num1 = box[0][1]
        num2 = box[1][1]


        #just preserve original peer values
        peers_cp = peers.copy()

        digit = values[box[0]]
        
        '''
        you need to check whether Naked twins pairs belong to the same row, col or diagonal in order to
        delete the same values from the corrosponding row. 
        for each pair: 
            1. if the first value is changing while the other is the same (ex A1, B1), then delete from col
            2. if the first value is the same while the other is the chaning (ex A1, A7), then delete from row
            3. Else: delete the value from the diagonal.
        '''
        
        if((row1 != row2) and (num1 ==num2) ):
            # Ex: A1, B1: delete in col
            col_peers = {v for v in peers_cp[box[0]] if (v[1] == num1) }
            values = del_Naked_Twins(digit,col_peers, values)
        

        elif ((row1 == row2) and (num1 !=num2) ):
            # Ex: A1, A7: delete in row
            row_peers = {v for v in peers_cp[box[0]] if (v[0] == row1) }
            values = del_Naked_Twins(digit,row_peers, values)
      
        else:
            #delete in diagonal
            
            if(peers_cp[box[0]]) in left_Diag:
                diag_peers = left_Diag
            elif (peers_cp[box[0]]) in right_Diag:
                diag_peers = right_Diag
            else:
                diag_peers = left_Diag + right_Diag
            
            values = del_Naked_Twins(digit,diag_peers, values)

                        
    
    return values




def grid_values(grid):
    
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in digits))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        # Use the Eliminate Strategy
        values = eliminate(values)
        
        # Use the Only Choice Strategy
        values = only_choice(values)
        
        # Use Naked-Twins Strategy
        
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        
        # Sanity check, return False if there is a box with zero available values:
        
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    
    for value in values[s]:
        new_sudoku = values.copy() #never forget to make a copy it is passed by ref.
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:   #if it converged
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
