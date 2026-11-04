"""Core interval algebra for half-open intervals [start, end).

An interval is a pair of numbers with start < end. Empty intervals are not
representable; callers should drop them. All operations return a new tuple of
intervals sorted by start, with no overlaps and no adjacent intervals that
touch (i.e. the result is normalized).

Why half-open? Half-open intervals compose cleanly: adjacent intervals such as
[0, 1) and [1, 2) can be merged into [0, 2), and subtraction never needs to
choose between open and closed endpoints. This is the same convention used by
Python's range and slicing, so it is familiar to most readers.
"""

from __future__ import annotations

from typing import Iterable, List, NamedTuple, Sequence, Tuple


class Interval(NamedTuple):
    """A half-open interval [start, end).

    NamedTuple is used so intervals are immutable, hashable, and unpack like
    plain tuples. That keeps the API lightweight and avoids a custom class with
    six dunder methods for what is fundamentally two numbers.
    """

    start: float
    end: float

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return self.start < self.end


# A normalized interval list is sorted by start and has no overlaps or touching
# neighbours.
Normalized = Tuple[Interval, ...]


def _as_interval(value) -> Interval:
    """Coerce a pair or Interval into an Interval.

    Accepting plain tuples keeps the public functions easy to call from user
    code that already stores intervals as tuples.
    """
    if isinstance(value, Interval):
        return value
    start, end = value
    return Interval(start, end)


def _normalize(intervals: Iterable[Interval]) -> Normalized:
    """Sort and merge a list of intervals.

    This is the workhorse behind every public function. It assumes the caller
    has already dropped empty intervals; empty intervals would silently vanish
    here, which is fine, but we filter them early to keep the logic obvious.
    """
    items: List[Interval] = [iv for iv in intervals if iv.start < iv.end]
    if not items:
        return ()
    items.sort(key=lambda iv: (iv.start, iv.end))
    out: List[Interval] = [items[0]]
    for iv in items[1:]:
        last = out[-1]
        if iv.start <= last.end:
            # Overlapping or touching: extend. max() handles the case where the
            # new interval is fully contained in the previous one.
            out[-1] = Interval(last.start, max(last.end, iv.end))
        else:
            out.append(iv)
    return tuple(out)


def merge(intervals: Iterable) -> Normalized:
    """Merge overlapping and touching half-open intervals.

    Returns a tuple of Interval objects sorted by start. Two intervals that
    merely touch, e.g. [0, 1) and [1, 2), are merged into [0, 2) because the
    union is itself a single interval under the half-open convention.
    """
    return _normalize(_as_interval(iv) for iv in intervals)


def intersect(a: Iterable, b: Iterable) -> Normalized:
    """Intersect two sets of intervals.

    The result contains every maximal interval that lies in both inputs. Both
    inputs are normalized first so the sweep is a simple two-pointer walk.
    """
    left = _normalize(_as_interval(iv) for iv in a)
    right = _normalize(_as_interval(iv) for iv in b)
    out: List[Interval] = []
    i = j = 0
    while i < len(left) and j < len(right):
        lo = max(left[i].start, right[j].start)
        hi = min(left[i].end, right[j].end)
        if lo < hi:
            out.append(Interval(lo, hi))
        # Advance the interval that ends first; the other may still overlap
        # with the next one from the opposite list.
        if left[i].end < right[j].end:
            i += 1
        else:
            j += 1
    return tuple(out)


def subtract(a: Iterable, b: Iterable) -> Normalized:
    """Subtract the set b from the set a.

    Returns the parts of a that are not covered by b. Both inputs are
    normalized first. The sweep walks a while consuming b intervals that lie
    before or overlap the current a interval.
    """
    left = _normalize(_as_interval(iv) for iv in a)
    right = _normalize(_as_interval(iv) for iv in b)
    out: List[Interval] = []
    j = 0
    for iv in left:
        cur_start, cur_end = iv.start, iv.end
        # Skip b intervals that end at or before the current a start.
        while j < len(right) and right[j].end <= cur_start:
            j += 1
        k = j
        while k < len(right) and right[k].start < cur_end:
            piece = right[k]
            if piece.start > cur_start:
                out.append(Interval(cur_start, min(piece.start, cur_end)))
            if piece.end >= cur_end:
                cur_start = cur_end
                break
            cur_start = max(cur_start, piece.end)
            k += 1
        if cur_start < cur_end:
            out.append(Interval(cur_start, cur_end))
    return tuple(out)
