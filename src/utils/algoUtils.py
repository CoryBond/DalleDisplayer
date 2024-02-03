from typing import List

from utils.enums import DIRECTION


# Copy paste of bisect_left
def reverse_bisect_right(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        # Use __lt__ to match the logic in list.sort() and in heapq
        if x > a[mid]: hi = mid
        else: lo = mid+1
    return lo


# Copy paste of bisect_left
def reverse_bisect_left(a, x, lo=0, hi=None):
    """Return the index where to insert item x in list a, assuming a is sorted.

    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.

    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        # Use __lt__ to match the logic in list.sort() and in heapq
        if a[mid] > x: lo = mid+1
        else: hi = mid
    return lo


def get_next_string_index_from_reverse_sorted(theString: str, reverseSortedStrings: List[str], direction: DIRECTION = DIRECTION.FORWARD) -> int:
    """
    Util function that gets the next logical index of a given string in a reverse sorted string list. If the provided string has no "next" entry
    then None is returned instead.

    The performance of this function should be Olog(s = size of reverseSortedFiles) for getting the next index.

    Parameters
    ----------
    theString: (str):
        The string to search the sorted files in.

    reverseSortedStrings: (list):
        The strings to search the next string index in.
        The provided list of strings must be sorted IN REVERSE order for this function to work properly.

    Returns
    -------
    int
        A number if there exists a next logical entry for the provided string or None if not
    """
    if(reverseSortedStrings is not None and len(reverseSortedStrings) > 0):
        if(direction is not DIRECTION.BACKWARD):
            nextIndex = reverse_bisect_right(reverseSortedStrings, theString)
            if(nextIndex < len(reverseSortedStrings)):
                return nextIndex
        else:
            nextIndex = reverse_bisect_left(reverseSortedStrings, theString)
            if(nextIndex != 0):
                return nextIndex - 1
    return None