# mini-interval-merge

Merge, subtract and intersect sets of half-open intervals. All operations are pure functions that take iterables of intervals (or `(start, end)` pairs) and return a tuple of `Interval` objects sorted by start, with overlaps and touching neighbours already merged.

```python
from mini_interval_merge import Interval, merge, subtract, intersect

merge([(0, 1), (1, 2), (5, 7)])          # (Interval(0, 2), Interval(5, 7))
subtract([(0, 10)], [(3, 5)])            # (Interval(0, 3), Interval(5, 10))
intersect([(0, 3), (5, 8)], [(1, 6)])    # (Interval(1, 3), Interval(5, 6))
```

## Why this exists

Interval arithmetic is easy to get subtly wrong: sorting, merging touching
intervals, and sweeping two lists at once all have off-by-one traps. This
library fixes one convention — half-open intervals `[start, end)` — and
implements the three operations people actually need on top of it. The
trade-off is that empty intervals (`start == end`) are not representable and
are silently dropped; if you need point intervals you must model them as
zero-length ranges yourself.

## The awkward edge

Half-open intervals that touch are merged: `merge([(0, 1), (1, 2)])` returns
`(Interval(0, 2),)`, not two intervals. That is deliberate — the union of two
touching half-open intervals is a single half-open interval — but it surprises
people who expect `[0, 1)` and `[1, 2)` to stay separate. The same convention
means `intersect([(0, 1)], [(1, 2)])` is empty, because a single point is not
an interval.

## API

- `Interval(start, end)` — a named tuple representing `[start, end)`.
- `merge(intervals)` — union of the inputs.
- `subtract(a, b)` — parts of `a` not covered by `b`.
- `intersect(a, b)` — parts covered by both `a` and `b`.

Each function accepts any iterable of `Interval` objects or `(start, end)`
pairs and returns a tuple of `Interval` objects.
