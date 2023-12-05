import random
import sys
from typing import List

sys.setrecursionlimit(999)

"""
A basic point class with (x,y) floating-point coordinates
"""
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x:.4f}, {self.y:.4f})'


"""
A basic segment class consisting of two Point endpoints.
"""
class Segment:
    def __init__(self, start: Point, end: Point, data):
        assert isinstance(start, Point)
        assert isinstance(end, Point)
        self.start = start
        self.end = end
        self.data = data

    def __str__(self):
        return f'{self.start} -> {self.end}'

    def min_x(self):
        return min(self.start.x, self.end.x)

    def max_x(self):
        return max(self.start.x, self.end.x)

    def min_y(self):
        return min(self.start.y, self.end.y)

    def max_y(self):
        return max(self.start.y, self.end.y)


"""
A segment tree
"""
class SegmentTree:
    left = None
    right = None

    """
    min_x and max_x params are for internal use only
    """
    def __init__(self, segments: List[Segment]):
        assert len(segments) > 0
        assert all([isinstance(x, Segment) for x in segments])
        x_endpoints = sorted([x.start.x for x in segments] + [x.end.x for x in segments])
        self.split_point = x_endpoints[random.randint(0, len(x_endpoints)-1)]
        self.min_x = min(segments, key=lambda s: s.min_x()).min_x()
        self.max_x = max(segments, key=lambda s: s.max_x()).max_x()

        left = list()
        right = list()
        self.center = list()
        for segment in segments:
            if segment.min_x() <= self.min_x and segment.max_x() >= self.max_x:
                self.center.append(segment)
            else:
                if segment.min_x() < self.split_point:
                    left.append(segment)
                if segment.max_x() > self.split_point:
                    right.append(segment)

        # Handle edge cases where we cannot split two overlapping segments by simply processing
        # them left-to-right.
        if len(segments) >= 2 and (len(left) == 0 or len(right) == 0):
            self.left = SegmentTree([min(segments, key=lambda s: s.min_x())])
            self.right = SegmentTree([x for x in segments if x.min_x() > self.min_x])
        else:
            if len(left) > 0:
                self.left = SegmentTree(left)
            if len(right) > 0:
                self.right = SegmentTree(right)
        self.center.sort(key=lambda s: segment.min_y())

    """
    Return the data associated with all particles in the specified bounding box.
    The data associated with a particle is typically its ID/index.
    """
    def window_query(self, left: float, right: float, top: float, bottom: float):
        retval = set()

        if left <= self.min_x and right >= self.max_x:
            # TODO: do binary search instead of a linear scan.  In practice, this list is likely to be small, and
            # there is probably a negligible performance benefit.
            for segment in self.center:
                if segment.min_y() > top:
                    break
                if segment.min_y() >= bottom:
                    retval.add(segment)

        if self.left is not None and left < self.split_point:
            retval |= self.left.window_query(left, right, top, bottom)
        if self.right is not None and right > self.split_point:
            retval |= self.right.window_query(left, right, top, bottom)

        return retval
