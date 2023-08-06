import copy
import numpy

def value_map2matrix(value_map: dict, m_max: int = 0, dtype = numpy.int16) -> numpy.ndarray:

    """
        value_map2matrix reduces the value map into
        a numpy matrix.

        Return:
            numpy.ndarray: (n x m)
    """
    if value_map == {}:
        # A linprog system has at least the support vector
        return numpy.zeros((1, m_max+1))

    n,m = 0,m_max
    for values in value_map.values():
        _n, _m = numpy.max(values, axis=1) if (len(values[0]) > 0 and len(values[1]) > 0) else (0, 0)

        n = _n if _n > n else n
        m = _m if _m > m else m

    M = numpy.zeros((n+1, m+1), dtype=dtype)
    for value, indices in value_map.items():
        M[tuple(indices)] = value

    return M

def merge_value_maps(*value_maps) -> dict:
    """
        merge_value_maps merges recursively value maps into one value map.
        Since the row indices from one value map to the other may collide,
        each merge will first find the highest row index value in the left
        value map, and then add it onto all the row values of the right value map.

        Return:
            dict (value map): value -> [[row_idxs], [col_idxs]]
    """
    if len(value_maps) == 0:
        return {}

    if len(value_maps) == 1:
        return value_maps[0]

    value_map_list = list(value_maps)
    value_map_left, value_map_right = value_map_list[0], value_map_list[1]
    if value_map_left == {} and value_map_right == {}:
        return {}

    elif value_map_left == {}:
        return value_map_right

    elif value_map_right == {}:
        return value_map_left

    highest_idx = 0
    for _, (row_idxs, _) in value_map_left.items():
        for row_idx in row_idxs:
            if row_idx > highest_idx:
                highest_idx = row_idx

    merged_value_map = copy.deepcopy(value_map_left)
    for value, (row_idxs, col_idxs) in value_map_right.items():
        merged_value_map.setdefault(value, [[], []])
        merged_value_map[value][0] += [highest_idx+row_idx+1 for row_idx in row_idxs]
        merged_value_map[value][1] += col_idxs

    return merge_value_maps(merged_value_map, *value_map_list[2:])

def configuration2value_map(configurations: list, variables: list) -> dict:
    """
        Takes a list of configurations and a list of the variables and returns a value map
        representing those configurations.

        NOTE: A variable in any configuration that is not in the variables list is simply neglected

        Example:
            Input:
                configurations = [
                    ('a', 'b', 'c'),
                    ('c', 'd', 'e'),
                    ]
                variables = ['a', 'b', 'c', 'd', 'e']
            Output:
                {1: [
                    [0, 0, 0, 1, 1, 1],
                    [0, 1, 2, 2, 3, 4]
                    ]}
        Return:
            dict (value map): value -> [[row_idxs], [col_idxs]]
    """

    _row = [
        int(row_index)
        for row_index in range(len(configurations)) 
        for var in configurations[row_index] 
        if var in variables
    ]
    _col = [
        variables.index(var) 
        for row_index in range(len(configurations)) 
        for var in configurations[row_index] 
        if var in variables
    ]
    return { 1: [_row, _col]}
