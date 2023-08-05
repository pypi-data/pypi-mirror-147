"""
Thin MapReduce-like layer that wraps the Python multiprocessing
library.
"""
from __future__ import annotations
from typing import Optional
import doctest
import collections.abc
import multiprocessing as mp
from operator import concat
from functools import reduce, partial
import parts

def _parts(xs, quantity):
    """
    Wrapper for partitioning function that returns a sized
    list of parts if the original input iterable is sized.
    """
    xss = parts.parts(xs, quantity)
    return list(xss) if isinstance(xss, collections.abc.Sized) else xss

class pool:
    """
    Class for a MapReduce-for-multiprocessing pool.

    >>> from operator import inv, add
    >>> with pool() as pool_:
    ...     results = pool_.mapreduce(m=inv, r=add, xs=range(3))
    ...     results
    -6
    """
    def __init__(
        self: pool,
        processes: Optional[int] = None, stages: Optional[int] = None, progress=None,
        close: Optional[bool] = False
    ):
        """
        Initialize a pool given the target number of processes.
        """
        # Use the maximum number of available processes as the default.
        # If a negative number of processes is designated, wrap around
        # and subtract from the maximum.
        if isinstance(processes, int) and processes <= 0:
            processes = mp.cpu_count() + processes
        elif processes is None:
            processes = mp.cpu_count()

        # Only create a multiprocessing pool if necessary.
        if processes != 1:
            self._pool = mp.Pool(processes=processes) # pylint: disable=consider-using-with

        self._processes = processes
        self._stages = stages
        self._progress = progress
        self._close = close # Indicates whether to close the pool after first `mapreduce` call.
        self._closed = False
        self._terminated = False

    def __enter__(self: pool):
        """
        Placeholder to enable use of `with` construct.
        """
        return self

    def __exit__(self: pool, exc_type, exc_value, exc_traceback):
        """
        Close the pool; exceptions are not suppressed.
        """
        self.close()

    def _map(self: pool, op, xs):
        """
        Split data (one part per process) and map the operation
        onto each part.
        """
        if self._processes == 1:
            return [[op(x) for x in xs]]
        else:
            return self._pool.map(
                partial(map, op),
                parts.parts(xs, self._pool._processes)
            )

    def _reduce(self: pool, op, xs_per_part):
        """
        Apply the specified binary operator to the results
        obtained from multiple processes.
        """
        if self._processes == 1 and len(xs_per_part) == 1:
            return reduce(op, map(partial(reduce, op), xs_per_part))
        else:
            return reduce(op, self._pool.map(partial(reduce, op), xs_per_part))

    def mapreduce(
        self: pool, m, r, xs,
        stages: Optional[int] = None, progress=None, close: Optional[bool] = None
    ):
        """
        Perform the map and reduce operations (optionally in stages on
        subsequences of the data) and then release resources if directed
        to do so.

        >>> from operator import inv, add
        >>> with pool() as pool_:
        ...     pool_.mapreduce(m=inv, r=add, xs=range(3))
        -6
        """
        # A `ValueError` is returned to maintain consistency with the
        # behavior of the underlying multiprocessing `Pool` object.
        if self.closed():
            raise ValueError('Pool not running')

        # Update state to enforce semantics of closing.
        self._closed = close if close is not None else self._closed

        stages = self._stages if stages is None else stages
        progress = self._progress if progress is None else progress
        close = self._close if close is None else close

        if stages is None:
            result = self._reduce(r, self._map(m, xs))
        else:
            # Separate input into specified number of stages.
            xss = _parts(xs, stages)

            # Perform each stage sequentially.
            result = None
            for xs_ in (progress(xss) if progress is not None else xss):
                result_stage = self._reduce(r, self._map(m, xs_))
                result = result_stage if result is None else r(result, result_stage)

        # Release resources if directed to do so.
        if close:
            self.close()

        return result

    def mapconcat(
        self: pool, m, xs,
        stages: Optional[int] = None, progress=None, close: Optional[bool] = None
    ):
        """
        Perform the map operation (optionally in stages on subsequences
        of the data) and then release resources if directed to do so.

        >>> with pool() as pool_:
        ...     pool_.mapconcat(m=tuple, xs=[[1], [2], [3]])
        (1, 2, 3)
        """
        return self.mapreduce(m, concat, xs, stages, progress, close)

    def close(self: pool):
        """
        Prevent any additional work from being added to the pool and release
        resources associated with the pool.

        >>> from operator import inv
        >>> pool_ = pool()
        >>> pool_.close()
        >>> pool_.mapconcat(m=inv, xs=range(3))
        Traceback (most recent call last):
          ...
        ValueError: Pool not running
        """
        self._closed = True
        if self._processes != 1:
            self._pool.close()

    def closed(self: pool) -> bool:
        """
        Return a boolean indicating whether the pool has been closed.

        >>> pool_ = pool()
        >>> pool_.close()
        >>> pool_.closed()
        True
        """
        if self._processes == 1:
            return self._closed
        else:
            return self._closed or self._pool._state in ('CLOSE', 'TERMINATE')

    def terminate(self: pool):
        """
        Terminate the underlying multiprocessing pool (associated resources
        will eventually be released, or they will be released when the pool
        is closed).
        """
        self._closed = True
        self._terminated = True
        if self._processes != 1:
            self._pool.terminate()

    def cpu_count(self: pool) -> int:
        """
        Return number of available CPUs.

        >>> with pool() as pool_:
        ...     isinstance(pool_.cpu_count(), int)
        True
        """
        return mp.cpu_count()

    def __len__(self: pool) -> int:
        """
        Return number of processes supplied as a configuration parameter
        when the pool was created.

        >>> with pool(1) as pool_:
        ...     len(pool_)
        1
        """
        return self._processes

def mapreduce(
    m, r, xs,
    processes: Optional[int] = None, stages: Optional[int] = None, progress=None
):
    """
    One-shot synonym for performing a workflow (no explicit object
    management or resource allocation is required on the user's part).

    >>> from operator import inv, add
    >>> mapreduce(m=inv, r=add, xs=range(3))
    -6
    """
    if processes == 1:
        if stages is not None:
            xss = _parts(xs, stages) # Create one part per stage.
            return reduce(r, [
                m(x)
                for xs in (progress(xss) if progress is not None else xss)
                for x in xs
            ])
        else:
            return reduce(r, [m(x) for x in xs])
    else:
        pool_ = pool() if processes is None else pool(processes)
        return pool_.mapreduce(m, r, xs, stages=stages, progress=progress, close=True)

def mapconcat(
    m, xs,
    processes: Optional[int] = None, stages: Optional[int] = None, progress=None
):
    """
    One-shot synonym for applying an operation across an iterable
    and assembling the results back into a list (no explicit object
    management or resource allocation is required on the user's part).

    >>> mapconcat(m=list, xs=[[1], [2], [3]])
    [1, 2, 3]
    """
    return mapreduce(m, concat, xs, processes, stages=stages, progress=progress)

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
