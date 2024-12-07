from __future__ import annotations

from collections import deque
from collections.abc import Iterable
from typing import Any, Callable, TypeVar

import numpy as np
from numpy.fft import fft2, fftfreq, fftshift
from numpy.typing import NDArray

T = TypeVar("T")
U = TypeVar("U")
D = TypeVar("D", bound=np.generic)


def apply_along_wedges(
    c_struct: list[list[list[U]]],
    fun: Callable[
        [
            U,
            int,  # wedge index
            int,  # direction index
            int,  # scale index
            int,  # nwedges
            int,  # ndirections
            int,  # nscales
        ],
        T,
    ],
) -> list[list[list[T]]]:
    r"""Apply functions across a UDCT curvelet-like structure

    Parameters
    ----------
    c_struct : list[list[list[U]]]
        Input curvelet structure. First index: scales, second: directions, third: wedges.
    fun : Callable[[U, int, int, int, int, int, int], T]
        Function to apply to each item in the structure. The function's arguments
        are respectively: item, wedge index, direction index, scale index, number
        of wedges in direction, number of directions in scale, number of scales.

    Returns
    -------
    list[list[list[T]]]
        Result of applying the function to each item.

    Examples
    --------
    >>> import numpy as np
    >>> from curvelets.numpy import SimpleUDCT
    >>> from curvelets.utils import apply_along_wedges
    >>> x = np.zeros((32, 32))
    >>> C = SimpleUDCT(x.shape, nscales=3, nbands_per_direction=3)
    >>> y = C.forward(x)
    >>> apply_along_wedges(y, lambda w, *_: w.shape)
    [[[(16, 16)]],
     [[(8, 8), (8, 8), (8, 8)], [(8, 8), (8, 8), (8, 8)]],
     [[(16, 8), (16, 8), (16, 8), (16, 8), (16, 8), (16, 8)],
      [(8, 16), (8, 16), (8, 16), (8, 16), (8, 16), (8, 16)]]]

    """
    mapped_struct: list[list[list[T]]] = []
    for iscale, c_angles in enumerate(c_struct):
        tmp_scale = []
        for idir, c_dir in enumerate(c_angles):
            tmp_dir = []
            for iwedge, c_wedge in enumerate(c_dir):
                out = fun(
                    c_wedge,
                    iwedge,
                    idir,
                    iscale,
                    len(c_dir),
                    len(c_angles),
                    len(c_struct),
                )
                tmp_dir.append(out)
            tmp_scale.append(tmp_dir)
        mapped_struct.append(tmp_scale)
    return mapped_struct


def array_split_nd(ary: NDArray[D], *args: int) -> list[Any]:
    r"""Split an array into multiple sub-arrays recursively, possibly unevenly.

    Parameters
    ----------
    ary : :obj:`NDArray[D] <numpy.typing.NDArray>`
        Input array.
    args : :obj:`int`, optional
        Number of splits for each axis of ``ary``.
        Axis 0 will be split into ``args[0]`` subarrays, axis 1 will be
        into ``args[1]`` subarrays, etc. An axis of length
        ``l = ary.shape[axis]`` that should be split into ``n = args[axis]``
        sections, will return ``l % n`` sub-arrays of size ``l//n + 1``
        and the rest of size ``l//n``.

    Returns
    -------
    list[Any]
        Recursive lists of lists of :obj:`NDArray[D] <numpy.typing.NDArray>`.
        The number of depth of nesting is equivalent to the number arguments in args.

    See Also
    --------
    :obj:`numpy.array_split` : Split an array into multiple sub-arrays.

    Examples
    --------
    >>> from curvelets.utils import array_split_nd
    >>> ary = np.outer(1 + np.arange(2), 2 + np.arange(3))
    array([[2, 3, 4],
           [4, 6, 8]])
    >>> array_split_nd(ary, 2, 3)
    [[array([[2]]), array([[3]]), array([[4]])],
     [array([[4]]), array([[6]]), array([[8]])]]
    >>> ary = np.outer(np.arange(3), np.arange(5))
    >>> array_split_nd(ary, 2, 3)
    [[array([[0, 0],
             [0, 1]]),
      array([[0, 0],
             [2, 3]]),
      array([[0],
             [4]])],
     [array([[0, 2]]), array([[4, 6]]), array([[8]])]]
    """

    axis = ary.ndim - len(args)
    split = np.array_split(ary, args[0], axis=axis)
    if len(args) == 1:
        return split  # type: ignore[no-any-return]
    return [array_split_nd(s, *args[1:]) for s in split]


def deepflatten(lst: list[Any]) -> Iterable[Any]:
    r"""Flatten arbitrarily nested lists

    Parameters
    ----------
    lst : list[Any]
        Nested list of lists.

    Yields
    ------
    Iterator[Iterable[Any]]
        Elements in ``lst`` in order.

    Examples
    --------
    >>> from curvelets.utils import deepflatten
    >>> list(deepflatten([[[[[[1],2,[[3,4]]]]]]]))
    [1, 2, 3, 4]
    """
    q: Any = deque()
    for item in lst:
        if isinstance(item, list):
            q.extendleft(reversed(item))
        else:
            q.appendleft(item)
        while q:
            elem = q.popleft()
            if isinstance(elem, list):
                q.extendleft(reversed(elem))
            else:
                yield elem


def ndargmax(ary: NDArray[D]) -> tuple[np.intp, ...]:
    r"""N-dimensional argmax of array.

    Parameters
    ----------
    ary : :obj:`NDArray <numpy.typing.NDArray>`
        Input array.

    Returns
    -------
    :obj:`tuple` [:obj:`numpy.intp`, ...]
        N-dimensional index of the maximum of ``ary``.

    Examples
    --------
    >>> import numpy as np
    >>> from curvelets.utils import ndargmax
    >>> x = np.zeros((10, 10, 10))
    >>> x[1, 1, 1] = 1.0
    >>> ndargmax(x)
    (1, 1, 1)

    """
    return np.unravel_index(ary.argmax(), ary.shape)  # type: ignore[no-any-return]


def normal_vector_field(
    data: NDArray[np.generic], rows: int, cols: int, dx: float = 1, dy: float = 1
) -> NDArray[np.float64]:
    r"""Creates equally spaced vectors normal to the data.

    Parameters
    ----------
    data : :obj:`NDArray <numpy.typing.NDArray>`
        Input data. Plot with :obj:`plt.imshow <matplotlib.pyplot.imshow>` ``(data.T)``.
    rows : int
        Number of rows.
    cols : int
        Number of columns.
    dx : float, optional
        Spacing in the ``axis=0`` direction, by default 1
    dy : float, optional
        Spacing in the ``axis=1`` direction, by default 1

    Returns
    -------
    :obj:`NDArray <numpy.typing.NDArray>` [:obj:`numpy.float64`]
        Normal vectors shaped ``(nrows, ncols, 2)``
    """
    kvecs: NDArray[np.float64] = np.empty((rows, cols, 2), dtype=float)
    d_split: list[list[NDArray[D]]] = array_split_nd(data.T, rows, cols)

    for irow in range(kvecs.shape[0]):
        for icol in range(kvecs.shape[1]):
            d_loc = d_split[irow][icol].T
            d_k_loc = fftshift(fft2(d_loc))
            kx_loc = fftshift(fftfreq(d_loc.shape[0], d=dx))
            kz_loc = fftshift(fftfreq(d_loc.shape[1], d=dy))

            # Use top quadrants of f-k spectrum
            top_quadrant = kz_loc > 0
            kx_locmax, kz_locmax = ndargmax(np.abs(d_k_loc[:, top_quadrant]))  # pylint: disable=unbalanced-tuple-unpacking

            k = np.array([kx_loc[kx_locmax], kz_loc[top_quadrant][kz_locmax]])
            kvecs[irow, icol, :] = k / np.linalg.norm(k)
    return kvecs
