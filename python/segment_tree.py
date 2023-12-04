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


"""
A segment tree
"""
class SegmentTree:
    """
    min_x and max_x params are for internal use only
    """
    def __init__(self, segments: List[Segment], depth = 0):
        assert len(segments) > 0
        assert all([isinstance(x, Segment) for x in segments])
        x_endpoints = sorted([x.start.x for x in segments] + [x.end.x for x in segments])
        self.split_point = x_endpoints[random.randint(0, len(x_endpoints)-1)]
        self.min_x = min(segments, key=lambda s: s.min_x()).min_x()
        self.max_x = max(segments, key=lambda s: s.max_x()).max_x()

        print(f'min: {self.min_x}, max: {self.max_x}, split: {self.split_point}')
        for segment in segments:
            print(segment)

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
        print(f'left: {len(left)}')
        print(f'right: {len(right)}')
        print(f'center: {len(self.center)}')
        print(f'depth: {depth}')
        if len(left) > 0:
            self.left = SegmentTree(left, depth+1)
        if len(right) > 0:
            self.right = SegmentTree(right, depth+1)
        self.center.sort(key=lambda s: segment.min_x())


    # def window_query(self, lower_left, upper_right):




