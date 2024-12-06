"""Supplement NumPy.

Functions
---------
pad_indices
    Pad indices with arrays for the outermost dimensions of a shape.
get
    Index an array's innermost dimensions, broadcasting over the others.
"""

import numpy as np


def pad_indices(shape, indices):
    """Pad indices with arrays for the outermost dimensions of shape.

    >>> import numpy as np
    >>> import numpyextra as npx
    >>> a = np.arange(6).reshape((3, 2))
    >>> a
    array([[0, 1],
           [2, 3],
           [4, 5]])
    >>> indices = npx.pad_indices(a.shape, ([1, 0, 1],))
    >>> indices
    (array([0, 1, 2]), [1, 0, 1])
    >>> a[indices] += 10
    >>> a
    array([[ 0, 11],
           [12,  3],
           [ 4, 15]])
    >>> npx.pad_indices((3, 2), ([[1, 0, 1], [0, 1, 1], [1, 1, 0], [0, 0, 0]],))
    (array([0, 1, 2]), [[1, 0, 1], [0, 1, 1], [1, 1, 0], [0, 0, 0]])
    >>> npx.pad_indices((3, 2), ())
    (array([[0],
           [1],
           [2]]), array([[0, 1]]))
    >>> npx.pad_indices((3, 2), (2, [1, 0]))
    (2, [1, 0])
    >>> npx.pad_indices((4, 3, 2), ([1, 0, 1],))
    (array([[0],
           [1],
           [2],
           [3]]), array([[0, 1, 2]]), [1, 0, 1])
    >>> npx.pad_indices((4, 3, 2), ([1, 1, 0, 2], 1))
    (array([0, 1, 2, 3]), [1, 1, 0, 2], 1)
    """
    return np.indices(shape[: len(shape) - len(indices)], sparse=True) + indices


def get(a, indices):
    """With indices index a's innermost dimensions, broadcasting over the others.

    - ``lambda a: get(a, ())`` is a generalized universal function
      (gufunc) with signature ``()->()``;
    - ``lambda a, z: get(a, (z,))`` is a gufunc with signature
      ``(m),()->()``;
    - ``lambda a, y, z: get(a, (y, z))`` is a gufunc with signature
      ``(l,m),(),()->()``;

    and so on.

    >>> import numpy as np
    >>> import numpyextra as npx
    >>> a = np.arange(6).reshape((3, 2))
    >>> a
    array([[0, 1],
           [2, 3],
           [4, 5]])
    >>> npx.get(a, ([1, 0, 1],))
    array([1, 2, 5])
    >>> npx.get(a, ([[1, 0, 1], [0, 1, 1], [1, 1, 0], [0, 0, 0]],))
    array([[1, 2, 5],
           [0, 3, 5],
           [1, 3, 4],
           [0, 2, 4]])
    >>> npx.get(a, ())
    array([[0, 1],
           [2, 3],
           [4, 5]])
    >>> npx.get(a, (2, [1, 0]))
    array([5, 4])
    >>> b = np.arange(24).reshape((4, 3, 2))
    >>> b
    array([[[ 0,  1],
            [ 2,  3],
            [ 4,  5]],
    <BLANKLINE>
           [[ 6,  7],
            [ 8,  9],
            [10, 11]],
    <BLANKLINE>
           [[12, 13],
            [14, 15],
            [16, 17]],
    <BLANKLINE>
           [[18, 19],
            [20, 21],
            [22, 23]]])
    >>> npx.get(b, ([1, 0, 1],))
    array([[ 1,  2,  5],
           [ 7,  8, 11],
           [13, 14, 17],
           [19, 20, 23]])
    >>> npx.get(b, ([1, 1, 0, 2], 1))
    array([ 3,  9, 13, 23])
    """
    a = np.asanyarray(a)
    return a[pad_indices(a.shape, indices)]
