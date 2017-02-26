import pygame
from pprint import pprint as pp

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]



double_rows = rows + rows
double_cols = cols + cols[::-1]

diagonal_forward = [s+t for s, t in zip(rows, cols)]
diagonal_reverse = [s+t for s, t in zip(rows, cols[::-1])]
diagonal_units = list(set(diagonal_forward).union(diagonal_reverse))
diagonals = [diagonal_forward, diagonal_reverse]

unitlist = row_units + column_units + square_units + diagonals
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
pp(units)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    twins = find_twins(values)
    # Eliminate the naked twins as possibilities for their peers
    for index, set_of_twins in enumerate(twins):
        for twin in set_of_twins:
            value = values[twin]
            values_to_remove = {ord(x): None for x in value}

            for peer in units[twin][index]:
                peer_value = values[peer]
                if (len(peer_value) > 1) and (peer_value != value):
                    assign_value(values, peer, peer_value.translate(values_to_remove))


    return values

def find_twins(values):
    """Finds the naked twins from a list of possible twins.
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}

        Returns:
            an array which holds four dictionaries. The first element contains naked_twins for rows, element two is the columns, three is the square units, and four is for diagonals.
        """
    potential_twins = [box for box in values.keys() if len(values[box]) == 2]
    confirmed_twins = [{}, {}, {}, {}, {}]
    for box in potential_twins:
        digit = values[box]

        for index, set_of_units in enumerate(units[box]):
            for peer in set_of_units:
                if digit == values[peer] and box != peer:
                    if box not in confirmed_twins[index]:
                        confirmed_twins[index][box] = [peer]
                    else:
                        confirmed_twins[index][box].append(peer)

    return confirmed_twins

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
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            # values[peer] = values[peer].replace(digit, '')
            assign_value(values, peer, values[peer].replace(digit, ''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[k]) == 1 for k in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    new, key = min((len(values[k]), k) for k in boxes if len(values[k]) > 1)
    # unsolved_values = {k: len(v) for k, v in values.items() if len(values[k]) > 1}

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for num in values[key]:
        potential_values = values.copy()
        # potential_values[key] = num
        assign_value(potential_values, key, num)
        success = search(potential_values)
        if success:
            return success

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    search(values)
    return values

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
