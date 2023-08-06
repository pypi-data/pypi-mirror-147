import numpy
import functools
import operator
import typing
import functools
import itertools
import more_itertools
import scipy.stats

# CONVERTERS
def matrix2value_map(matrix: numpy.ndarray, mapping: dict = {}) -> dict:

    """
        matrix2value_map reduces the matrix into
        a value map. `mapping` is just an ordinary dict,
        mapping one value to another

        NOTE: since zeros are excluded in a value map, leading zero
        rows/columns will not be included.

        Return:
            dictionary: value -> indices
    """
    return {
        value: [
            [
                mapping[j] if j in mapping and i > 0 and j > 0 else j
                for j in k
            ]
            for i, k in enumerate(numpy.argwhere(matrix == value).T.tolist())
        ]
        for value in set(matrix[matrix != 0])
    }

# linalg functions
def matrix2linalg(matrix: numpy.ndarray) -> tuple:
    """
        matrix2linalg assumes support vector index 0
        and returns A, b
    """
    A = matrix[:, 1:]
    b = matrix.T[0]
    return A, b

def linalg2matrix(A: numpy.ndarray, b: numpy.ndarray) -> tuple:
    """
        matrix2linalg assumes support vector index 0
        and returns A, b
    """
    return numpy.append(b.reshape(-1,1), A, 1)

def not_implies_or_reduce(L,i) -> list:

    """
        Takes the i'th row in L as x, reduces rest of list L
        from i and forth (L[i+1:]) and OR-reduces it into one
        row as y. Finally returns x not-implies y ( ~(x -> y) ).

        L: list of list of bools
        i: int as an row-index of L

        Return:
            List[bool]
    """

    return operator.mul(
        L[i],
        operator.sub(
            1,
            operator.ge(
                numpy.sum(L[i+1:], 0),
                1
            )
        )
    )

def row_wise_exp_offset(M: numpy.ndarray):

    if not M.ndim == 3:
        raise Exception(f"expected M to be 3D but got {M.ndim}D")

    m = M.copy()
    with numpy.errstate(divide='ignore', invalid='ignore'):
        offset = numpy.ceil(
            numpy.divide(
                numpy.log(numpy.abs(m).sum(axis=2)+1),
                numpy.log(2)
            )
        )
        offset_cmsm = numpy.cumsum(offset, axis=1)

    m[:,1:] = (m[:,1:] + offset_cmsm[:,:-1].reshape(offset_cmsm[:,:-1].shape + (1,))) * (m[:,1:] > 0)

    return m

def rank_ndarray(M: numpy.ndarray) -> numpy.ndarray:

    """
        Rank numbers in array in incrementing order.

        Example (1d arr):
            Input:
                M = [2,0,3]

            Output:
                M = [1,0,2]

        Example (2d arr):
            Input:
                M = [
                    [1,3,5],
                    [0,0,3],
                    [1,2,7]
                ]
            Output:
                M = [
                    [1,3,4],
                    [0,0,3],
                    [1,2,5]
                ]

        Return:
            numpy.ndarray
    """

    m = M.copy()
    unique_arr = numpy.unique(M.flatten())
    mn = unique_arr.min()
    ranked_arr = numpy.arange(mn, unique_arr.size+mn)
    for source, target in filter(lambda x: x[0] != x[1], zip(unique_arr, ranked_arr)):
        m[m == (source)] = target

    return m

def nd_states2objectives(nd_states: numpy.ndarray) -> numpy.ndarray:
    m = row_wise_exp_offset(nd_states)
    # Computing p & -q (as in -(p -> q)) where p is first row in matrix
    # and q is the reversed cumulative sum from second row and forth.
    # This is done for each matrix in m
    m_abs = numpy.abs(m)
    msk = (m_abs * (1 - m_abs[:,::-1].cumsum(axis=1)[:,::-1] + m_abs)) >= 1
    _m = row_wise_exp_offset(
        rank_ndarray(m_abs * msk)
    )
    m_ne_msk = (m < 0) & (_m != 0)
    v_sort_idxs = numpy.argsort(-_m, axis=1)
    v = numpy.power(2, _m) >> 1
    v[m_ne_msk] *= -1
    objs = numpy.take_along_axis(v, v_sort_idxs, axis=1)[:,0]
    return objs

def linprog2weighted_linprog(linprog: numpy.ndarray) -> numpy.ndarray:

    """
        Turns a linprog matrix (A, b) into a weighted
        linprog matrix (A, b, w) by keeping all values greater
        than 0 in w, all values less than 0 in A and letting b
        be the sum of the rows in A.

        Example,
            let linprog = [
                [ 0., -1.,  0.,  0.,  1.]
            ]

            which results in
            A = [
                [1, 0, 0, 0]
            ]
            b = [1]
            w = [
                [0, 0, 0, 1]
            ]

            or as concatenated matrix
            [
                [1, 1, 0, 0, 0, 0, 0, 0, 1]
            ]

        This can be used for example saying, if index 0 is set, then apply
        weight vector [0, 0, 0, 1] to something.

        Return:
            numpy.ndarray
    """
    if linprog.size == 0:
        return linprog

    cons_msk = linprog[:,1:] > 0
    cond_msk = linprog[:,1:] < 0
    n, m = linprog[:,1:].shape
    wlinprog = numpy.zeros((n, 1+2*m), dtype=numpy.int)
    wlinprog.T[0] = cond_msk.sum(axis=1)
    wlinprog[:,1:1+m][cond_msk] = 1
    wlinprog[:,1+m:1+2*m][cons_msk] = 1
    return wlinprog

def reducable_matrix_columns_approx(M: numpy.ndarray) -> numpy.ndarray:
    """
        Returns what columns are reducable under approximate condition.
        This method is much faster than the exhaustive `reducable_matrix_columns` function.
        Columns with positive values could be assumed
        Columns with negative values could be removed (not-assumed)

        Return:
            numpy.ndarray (vector)
    """
    A, b = matrix2linalg(M)
    r = (A*((A*(A <= 0) + (A*(A > 0)).sum(axis=1).reshape(-1,1)) < b.reshape(-1,1))) + A*((A * (A > 0)).sum(axis=1) == b).reshape(-1,1)
    return r.sum(axis=0)

def reduce_matrix_columns(M: numpy.ndarray, columns_vector: numpy.ndarray) -> numpy.ndarray:

    """
        Reducing columns from M (a system of linear inequalities) from columns_vector
        where a positive number meaning "assume" and a negative number meaning "not assume".
        The matrix is reduced column-wise by equally many positives and negatives in columns-vector.

        NOTE: M is concatenated A, b (as in Ax >= b), where b == A.T[0]

        Example:
            Input:
                M = numpy.ndarray([
                    [0,-1, 1, 0, 0],
                    [0, 0,-1, 1, 0],
                    [0, 0, 0,-1, 1],
                ])

                columns_vector = numpy.ndarray([
                    1, 0,-1, 0
                ]) # meaning assume index 0

            Output:
                numpy.ndarray([
                    [1, 1, 0],
                    [0,-1, 0],
                    [0, 0, 1],
                ])

        Return:
            numpy.ndarray
    """

    A, b = matrix2linalg(M)
    _b = b - (A.T*(columns_vector > 0).reshape(-1,1)).sum(axis=0)
    _A = numpy.delete(A, numpy.argwhere(columns_vector != 0).T[0], 1)
    return numpy.append(_b.reshape(-1,1), _A, axis=1)

def reducable_matrix_rows(M: numpy.ndarray) -> numpy.ndarray:
    """
        Returns a boolean vector indicating what rows are reducable.

        Return:
            numpy.ndarray (vector)
    """

    return (((M[:, 1:] * (M[:, 1:] < 0)).sum(axis=1) >= M.T[0])) + ((M[:,1:] >= 0).all(axis=1) & (M.T[0]<=0))

def reduce_matrix_rows(M: numpy.ndarray, rows_vector: numpy.ndarray) -> numpy.ndarray:

    """
        Reduces rows from a rows_vector where num of rows of M equals
        size of rows_vector. Each row in rows_vector == 0 is kept.
    """

    return M[rows_vector == 0]

def reducable_matrix_rows_and_columns(M: numpy.ndarray) -> tuple:

    """
        Returns reducable rows and columns of given matrix M.

        Approximative controls if only approximative methods should be applied.

        Returned is a tuple of (
            a vector equal size as M's row size where 1 represents a removed row
                and 0 represents a kept row,
            a vector with equal size as M's column size where a positive number
                represents requireds and a negative number represents forbids
        )

        Return:
            tuple

    """

    _M = M.copy()
    red_cols = reducable_matrix_columns_approx(_M)
    red_rows = reducable_matrix_rows(_M) * 1
    full_cols = numpy.zeros(_M.shape[1]-1)
    full_rows = numpy.zeros(_M.shape[0])
    while red_cols.any() | red_rows.any():
        _M = reduce_matrix_columns(_M, red_cols)
        full_cols[full_cols == 0] = red_cols

        red_rows = reducable_matrix_rows(_M) * 1
        _M = reduce_matrix_rows(_M, red_rows)
        full_rows[full_rows == 0] = red_rows

        red_cols = reducable_matrix_columns_approx(_M)
        red_rows = reducable_matrix_rows(_M) * 1

    return full_rows, full_cols

def reduce_matrix(M: numpy.ndarray, rows_vector: numpy.ndarray=None, columns_vector: numpy.ndarray=None) -> numpy.ndarray:
    """
        Reduces matrix M by information passed in rows_vector and columns_vector.

        The rows_vector is a vector of 0's and 1's where rows matching index of value 1 are removed.

        The columns_vector is a vector of positive and negative integers
        where the positive represents active selections and negative
        represents active "not" selections. Matrix M is reduced under those assumptions.

        Example:
            Input:
                M = numpy.array([
                    [ 0,-1, 1, 0, 0, 0, 0],
                    [ 0, 0,-1, 1, 0, 0, 0],
                    [-1, 0, 0,-1,-1, 0, 0],
                    [ 1, 0, 0, 0, 0, 1, 1],
                ])
                columns_vector = numpy.array([1,0,0,0,0,0])

            Output:
                (
                    numpy.array([
                    [ 1, 1, 0, 0, 0, 0],
                    [ 0,-1, 1, 0, 0, 0],
                    [-1, 0,-1,-1, 0, 0],
                    [ 1, 0, 0, 0, 1, 1],
                ])
                )
    """
    _M = M.copy()
    if rows_vector is not None:
        _M = reduce_matrix_rows(_M, rows_vector)
    if columns_vector is not None:
        _M = reduce_matrix_columns(_M, columns_vector)
    return _M

def neglectable_columns(M: numpy.ndarray, patterns: numpy.ndarray) -> numpy.ndarray:
    """
        Returns neglectable columns of given matrix M based on given patterns,
        i.e. the columns which doesn't differentiate the patterns in M
        and the patterns not in M

        Example:
            Input:
                M = numpy.array([
                    [-1,-1,-1, 0, 0, 0, 1],
                    [-1,-1, 0,-1, 0, 0, 1],
                ])
                patterns = numpy.array([
                    [1, 1, 0],
                    [0, 1, 1],
                    [1, 0, 1]
                ])
            Output:
                numpy.array([0, 1, 1, 1, 1, 0])

            Column 0 is differentiating the patterns in M from those that are not in M.
            Column 5 is not in the patterns and has a positive number for any row in M and
            is therefore considered non-neglectable.
    """
    A, b = matrix2linalg(M)
    # Extend patterns to be of same shape as A
    _patterns = patterns.copy()
    _patterns = numpy.pad(_patterns, ((0,0), (0, A.shape[1] - _patterns.shape[1])), 'constant')

    # We will never neglect columns that aren't part of any pattern
    columns_not_in_patterns = (_patterns==0).all(axis=0)
    non_neglectable_columns = columns_not_in_patterns
    _A = A.copy()
    _A[:, columns_not_in_patterns] = 0
    _A[numpy.nonzero(_A)] = 1

    # Find which patterns are not in A
    patterns_not_in_A = _patterns[~(_patterns[:, None] == _A).all(-1).any(-1)]
    if patterns_not_in_A.shape[0]==0:
        # Possible to neglect everything except non neglectable columns
        return (~non_neglectable_columns).astype(int)

    # Find common pattern in A
    common_pattern_in_A = (_A == 1).all(axis=0)
    if not (patterns_not_in_A[:,common_pattern_in_A]==1).all(axis=1).any(axis=0):
        # Possible to neglect everything except the common pattern and the non neglectable columns
        return (~(common_pattern_in_A | non_neglectable_columns)).astype(int)
    return ((_A[:, (patterns_not_in_A==0).all(axis=0) & (non_neglectable_columns==0)]).any(axis=1).all()) * (patterns_not_in_A!=0).any(axis=0).astype(int)

def neglect_columns(M: numpy.ndarray, columns_vector: numpy.ndarray) -> numpy.ndarray:
    """
        Neglects columns from a columns_vector where num of cols of M - 1 equals
        size of cols_vector, i.e. the entire column for col in columns_vector > 0
        is set to 0 and the support vector is updated.

        Example:
            Input:
                M = numpy.array([
                    [0,-1, 1, 0, 0],
                    [0, 0,-1, 1, 0],
                    [0, 0, 0,-1, 1],
                ])

                columns_vector = numpy.array([
                    1, 0, 1, 0
                ])

            Output:
                numpy.ndarray([
                    [ 1, 0, 1, 0, 0],
                    [-1, 0,-1, 0, 0],
                    [ 1, 0, 0, 0, 1],
                ])

            Return:
                numpy.ndarray
    """
    A, b = matrix2linalg(M)
    _b = b - (A.T*(columns_vector > 0).reshape(-1,1)).sum(axis=0)
    _A = A
    _A[:, columns_vector>0] = 0
    return numpy.append(_b.reshape(-1,1), _A, axis=1)

def matrix2crc_lines(
    mat: numpy.ndarray,
    key: callable,
    req_all: str="REQUIRES_ALL",
    req_any: str="REQUIRES_ANY",
    forb_all: str="FORBIDS_ALL",
    oon: str="ONE_OR_NONE"
) -> typing.List[tuple]:

    """
        Converts (approximately) a value map into a list of
        indexed crc-line rules. Since there are values in a value
        map that cannot be represented as a crc-line rule, assumptions
        has been made here.

        NOTE: column index 0 is assumed to be the "support vector"

        Example:
            Input:
                value_map = {
                    -2: [[1],[0]],
                    -1: [[0,0,0,1,1,1,2,2,4,4,4,6,6,6],[0,2,5,1,5,6,1,4,0,1,2,0,3,4]],
                    1: [[0,3,3,3,5,5,5], [6,0,1,2,0,3,4]],
                    2: [[2], [7]],
                }

            Output:
                [
                    (("b","x"), "REQUIRES_ALL", ("y")),
                    (("a","x"), "FORBIDS_ALL", ("y")),
                    (["a","d"], "REQUIRES_ALL", ("z")),
                    ((), "REQUIRES_ANY", ("a", "b")),
                    ((), "ONE_OR_NONE", ("a", "b")),
                    ((), "REQUIRES_ANY", ("c", "d")),
                    ((), "ONE_OR_NONE", ("c", "d")),
                ]

        NOTE:
            Saying a & b FORBIDS ALL c is same as
            a & c FORBIDS_ALL b and b & c FORBIDS_ALL a.

        Return:
            List[tuple]
    """
    Au, bu = mat[:,1:], mat.T[0]
    n_positive = (Au > 0).sum(axis=1)
    n_negative = (Au < 0).sum(axis=1)
    minimum = Au.min(axis=1)
    maximum = Au.max(axis=1)

    def cnst2rule(
        a: numpy.ndarray,
        b: int,
        np: int,
        nn: int,
        mn: int,
        mx: int,
        req_all: str="REQUIRES_ALL",
        req_any: str="REQUIRES_ANY",
        forb_all: str="FORBIDS_ALL",
        oon: str="ONE_OR_NONE"
    ) -> tuple:

        # If at least one positive, it has be either rall or rany
        if np > 0:
            # A req any cnst sum is always larger than its s-constant
            # Both req all/any has 1 on consequence vars and negative
            # value for its condition variables
            cnd = map(key, numpy.argwhere(a < 0).T[0])
            csq = map(key, numpy.argwhere(a == 1).T[0])
            label = req_any if a.sum() > b else req_all
            return tuple(cnd), label, tuple(csq)

        # the forb and oon must have at least one negative
        # but no negatives
        elif nn > 0:

            # All values are either 0 or -1, meaning either
            # a forbids all without conditions or...
            if mn == -1:
                if b == 0:
                    cnd = ()
                    csq = map(key, numpy.argwhere(a == -1).T[0])
                    label = forb_all
                    return tuple(cnd), label, tuple(csq)
                elif b < 0:
                    a_sum = a.sum()
                    if a_sum < b:
                        if b-a_sum == 1:
                            var = map(key, numpy.argwhere(a == -1).T[0])
                            cnd = more_itertools.take(abs(b), var)
                            csq = tuple(var)
                            label = forb_all
                        else:
                            cnd = ()
                            csq = map(key, numpy.argwhere(a == -1).T[0])
                            label = oon

                        return tuple(cnd), label, tuple(csq)
            else:
                cnd = map(key, numpy.argwhere(a < -1).T[0])
                csq = map(key, numpy.argwhere(a == -1).T[0])
                label = forb_all if (a == mn).sum()*mn == b else oon
                return tuple(cnd), label, tuple(csq)

        return None

    return itertools.starmap(
        functools.partial(
            cnst2rule,
            req_all=req_all,
            req_any=req_any,
            forb_all=forb_all,
            oon=oon,
        ),
        zip(Au, bu, n_positive, n_negative, minimum, maximum)
    )

def prio2weight(vec: numpy.ndarray) -> numpy.ndarray:

    """
        Example:
            Input:
                numpy.array([2,2,1,1,1,4,3])

            Output:
                numpy.array([4,4,1,1,1,24,12])
    """
    d = {}
    def inner(prio, arr, d):
        sign = -1 if prio < 0 else 1
        prio = abs(prio)
        if prio in d:
            return sign * d[prio]

        if prio == 0:
            res = 0
        elif prio == 1:
            res = 1
        else:
            p = abs(inner(prio-1, arr, d))
            res = p * (abs(arr) == (prio-1)).sum() + p

        d[prio] = res
        return sign * res

    return numpy.array(list(map(functools.partial(inner, arr=vec, d=d), vec)))

def truncate_nd_state(nd_state: numpy.ndarray) -> numpy.ndarray:

    """
        Takes a 2D state and truncates into a 1D state
        using certain logic.

        Example:
            Input:
                nd_state = numpy.array([
                    [ 0, 0, 0, 0, 1, 2],
                    [-1,-1,-1,-1, 0, 0],
                    [ 0, 0, 1, 2, 0, 0],
                    [ 0, 0, 1, 0, 0, 0]
                ])

            Output:
                numpy.array([-4,-4, 8,16, 1, 2])

        Return:
            numpy.ndarray (1d)
    """
    nd_state_abs = numpy.abs(nd_state)[:,::-1]
    la_state = numpy.zeros(nd_state_abs.shape)
    mat_idxs = numpy.repeat(numpy.arange(nd_state.shape[0]), nd_state.shape[2])
    row_idxs = (nd_state_abs != 0).argmax(axis=1).flatten()
    col_idxs = numpy.tile(numpy.arange(nd_state.shape[2]), nd_state.shape[0])
    la_state[mat_idxs, row_idxs, col_idxs] = 1
    la_state = (la_state * nd_state_abs)[:,::-1]
    la_state_ranked = scipy.stats.rankdata(la_state, method='dense', axis=2) #- (la_state == 0).any(axis=2).reshape(-1,1)
    la_state_re_ranked = la_state_ranked + ((la_state == 0).any(axis=2) * -numpy.ones(la_state_ranked.shape[1])).reshape(la_state.shape[0],la_state.shape[1],1)

    states = (la_state_re_ranked+numpy.cumsum(numpy.pad(la_state_re_ranked.max(axis=2), ((0,0),(1,0))),axis=1)[:,:-1].reshape(la_state.shape[0], la_state.shape[1], 1))*(la_state_re_ranked > 0)
    states[nd_state < 0] = states[nd_state < 0]*-1
    truncated = numpy.array(list(map(prio2weight, (states).sum(axis=1))))

    return truncated

def rank_3darray(cube: numpy.ndarray) -> numpy.ndarray:

    """
        Ranks a 3d (cude) numpy array from lowest value
        to highest with 1 in difference

        Example:
            Input:
                np.array([
                    [
                        [ 1, 9, 4, 6],
                        [ 1,-9, 4,-6],
                        [ 0, 1, 3, 2],
                        [ 4, 3, 1, 0],
                    ],
                ])

            Output:
                np.array([
                    [
                        [ 1, 4, 2, 3],
                        [ 1,-2, 2,-1],
                        [ 0, 1, 2, 3],
                        [ 3, 2, 1, 0],
                    ],
                ])

        Return:
            numpy.ndarray
    """
    mat = cube.reshape(cube.shape[0]*cube.shape[1],cube.shape[2])
    row_idxs = numpy.arange(mat.shape[0])
    for i in numpy.arange(1, mat.shape[1]+1):
        msk = (mat == mat[row_idxs, numpy.argmin(numpy.abs(mat-i), axis=1)].reshape(-1,1)) * (mat > i)
        mat[msk] = i

    return mat.reshape(cube.shape)

def my_func(input_list: numpy.ndarray) -> numpy.ndarray:
    sorted_indices = numpy.argsort(input_list)
    result = ufunc(input_list[sorted_indices])
    sorted_indices_inv = numpy.argsort(sorted_indices)
    return result[sorted_indices_inv]




