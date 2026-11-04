"""Public API for mini-interval-merge.

Exports the Interval type and the merge, subtract and intersect operations.
"""

from .core import Interval, merge, subtract, intersect

__all__ = ["Interval", "merge", "subtract", "intersect"]
