"""

"""
from __future__ import annotations

__author__ = "Oliver Lindemann <lindemann@cognitive-psychology.eu>"


from typing import List

import numpy as np
import shapely
from numpy.typing import NDArray

from .._misc import IntOVector, delete_elements
from .._shapes import Dot, Ellipse, Point2D
from .._shapes import ellipse_geometry as ellipse_geo
from .._shapes.abc_shapes import (AbstractCircularShape, AbstractShape,
                                  AttributeType)
from .convex_hull import ConvexHull


class ShapeArray(object):
    """Numpy Optimizes Representation of Array of shapes"""

    def __init__(self) -> None:
        self._xy = np.empty((0, 2), dtype=np.float64)
        self._sizes = np.empty((0, 2), dtype=np.float64)
        self._shapes = []
        self._cache_polygons = None
        self._cache_ids = None
        self._convex_hull = None
        self._shape_updated_required = False

    @property
    def xy(self) -> NDArray[np.float64]:
        """array of positions"""
        return self._xy

    @xy.setter
    def xy(self, val: NDArray[np.float64]):
        if val.shape != self._xy.shape:
            raise ValueError(
                f"xy has to be a numpy array with shape={self._xy.shape}")
        if np.any(self._xy != val):  # any change
            self._shape_updated_required = True
            self._clear_cached()
        self._xy = val

    @property
    def sizes(self) -> NDArray[np.float64]:
        """array of sizes"""
        return self._sizes

    @sizes.setter
    def sizes(self, val: NDArray[np.float64]):
        if val.shape != self._sizes.shape:
            raise ValueError(
                f"xy has to be a numpy array with shape={self._sizes.shape}")
        if np.any(self._sizes != val):
            self._shape_updated_required = True
            self._clear_cached()
        self._sizes = val

    def attributes(self) -> List[AttributeType]:
        return [s.attribute for s in self._shapes]

    @property
    def shapes(self) -> List[AbstractShape]:
        """list of the shapes"""
        if self._shape_updated_required:
            self.shapes_update()
        return self._shapes

    def shape_types(self) -> NDArray[np.str_]:
        """np.array of shape types"""
        return np.array([s.shape_type() for s in self._shapes])

    @property
    def polygons(self) -> NDArray[shapely.Polygon]:  # type: ignore
        """nparray of polygons"""
        if self._cache_polygons is None:
            # build polygons
            self._cache_polygons = np.array([s.polygon for s in self.shapes])
        return self._cache_polygons

    def ids(self, shape_type: str) -> NDArray:
        """np.array of ids for the different shape types"""
        return np.flatnonzero(self.shape_types() == shape_type)

    def shapes_update(self):
        """Updates list shapes, if property arrays `xy` or `sizes` have changed.

        Users have to call this method only, if `xy`or `sizes`has been manipulated
        manually in place (like `stim.xy[3, :] = (20, 10)`.
        If property setters are used (`stim.xy = new_xy`), this updates of shapes
        is done automatically.
        """
        for i, shape in enumerate(self._shapes):
            if np.any(shape.xy != self._xy[i, :]):
                shape.xy = self._xy[i, :]
            if np.any(shape.size != self._sizes[i, :]):
                shape.size = self._sizes[i, :]

        self._clear_cached()
        self._shape_updated_required = False

    def _clear_cached(self):
        """clears convex hull and ids"""
        self._convex_hull = None
        self._cache_ids = None
        self._cache_polygons = None

    def shape_add(self, shape: AbstractShape):
        """add shape to the array"""
        if isinstance(shape, AbstractShape):
            self._shapes.append(shape)
            self._xy = np.append(self._xy, np.atleast_2d(shape.xy), axis=0)
            self._sizes = np.append(
                self._sizes, np.atleast_2d(shape.size), axis=0)
            self._clear_cached()
        else:
            raise TypeError(
                f"Can't add '{type(shape)}'. That's not a ShapeType."
            )

    def shapes_join(self, other: ShapeArray) -> None:
        """join with shapes of other array"""
        for x in other.shapes:
            self.shape_add(x)

    def shape_replace(self, index: int, shape: AbstractShape):
        self._shapes[index] = shape
        self._xy[index, :] = shape.xy
        self._sizes[index, :] = shape.size
        self._clear_cached()

    def shape_delete(self, index: IntOVector) -> None:

        self._shapes = delete_elements(self._shapes, index)
        self._xy = np.delete(self._xy, index, axis=0)
        self._sizes = np.delete(self._sizes, index, axis=0)
        self._clear_cached()

    def shapes_clear(self):
        """ """
        self._shapes = []
        self._xy = np.empty((0, 2), dtype=np.float64)
        self._sizes = np.empty((0, 2), dtype=np.float64)
        self._clear_cached()

    def shape_pop(self, index: int | None = None) -> AbstractShape:
        """Remove and return item at index"""
        if index is None:
            index = len(self._shapes) - 1
        rtn = self.shapes[index]
        self.shape_delete(index)
        return rtn

    def sort_by_eccentricity(self):
        """Sort order of the shapes in the array by eccentricity, that is, by the
        distance the center of the convex hull (from close to far)
        """
        d = self.distances(Point2D(self.convex_hull.centroid))
        idx = np.argsort(d)
        self._xy = self._xy[idx, :]
        self._sizes = self._sizes[idx]
        self._shapes = [self._shapes[i] for i in idx]
        self._clear_cached()

    @property
    def n_shapes(self) -> int:
        """number of shapes"""
        return len(self._shapes)

    @property
    def convex_hull(self) -> ConvexHull:
        """Convex hull polygon of the Shape Array"""
        if not isinstance(self._convex_hull, ConvexHull):
            self._convex_hull = ConvexHull(self.polygons.tolist())
        return self._convex_hull

    def distances(self, shape: Point2D | AbstractShape) -> NDArray[np.float64]:
        """distances of a shape or Point2D to the elements in the shape array"""

        if isinstance(shape, (Point2D, AbstractCircularShape)):
            # circular target shape
            rtn = np.full(len(self._shapes), np.nan)

            idx = self.ids(Dot.shape_type())
            if len(idx) > 0:
                # circular -> dots in shape array
                rtn[idx] = _distance_circ_dot_array(obj=shape,
                                                    dots_xy=self._xy[idx, :],
                                                    dots_diameter=self._sizes[idx, 0])
            idx = self.ids(Ellipse.shape_type())
            if len(idx) > 0:
                # circular -> ellipses in shape array
                rtn[idx] = _distance_circ_ellipse_array(obj=shape,
                                                        ellipses_xy=self._xy[idx, :],
                                                        ellipse_sizes=self._sizes[idx, :])
            # check if non-circular shapes are in shape_array
            idx = np.flatnonzero(np.isnan(rtn))
            if len(idx) > 0:
                if isinstance(shape, AbstractCircularShape):
                    rtn[idx] = shapely.distance(
                        shape.polygon, self.polygons[idx])
                else:
                    rtn[idx] = shapely.distance(
                        shape.xy_point, self.polygons[idx])
            return rtn

        else:
            # non-circular shape as target
            return shapely.distance(shape.polygon, self.polygons)

    def dwithin(self, shape: Point2D | AbstractShape,  distance: float = 0) -> NDArray[np.bool_]:
        """Returns True for all elements of the array that are within the
        specified distance.

        Note
        -----
        Using this function is more efficient than computing the distance and comparing the result.
        """

        if isinstance(shape, (Point2D, AbstractCircularShape)):
            rtn = np.full(len(self._shapes), False)

            idx = self.ids(Dot.shape_type())
            if len(idx) > 0:
                # circular -> dots in shape array
                dists = _distance_circ_dot_array(obj=shape,
                                                 dots_xy=self._xy[idx, :],
                                                 dots_diameter=self._sizes[idx, 0])
                rtn[idx] = dists < distance

            idx = self.ids(Ellipse.shape_type())
            if len(idx) > 0:
                # circular -> ellipses in shape array
                dists = _distance_circ_ellipse_array(obj=shape,
                                                     ellipses_xy=self._xy[idx, :],
                                                     ellipse_sizes=self._sizes[idx, :])
                rtn[idx] = dists < distance

            # check if non-circular shapes are in shape_array
            idx = np.flatnonzero(np.isnan(rtn))
            if len(idx) > 0:
                if isinstance(shape, AbstractCircularShape):
                    rtn[idx] = shapely.dwithin(
                        shape.polygon, self.polygons[idx],  distance=distance)
                else:
                    rtn[idx] = shapely.dwithin(
                        shape.xy_point, self.polygons[idx],  distance=distance)

        else:
            # non-circular shape
            rtn = shapely.dwithin(
                shape.polygon, self.polygons, distance=distance)

        return rtn

    def has_overlaps(self, min_distance: float = 0) -> bool:
        """Returns True for two or more elements overlap (i.e. taking
        into account the minimum distance).
        """
        for x in range(len(self._shapes)):
            if np.any(self.overlaps(x, min_distance)) > 0:
                return True
        return False

    def overlaps(self, index: int, min_distance: float = 0) -> NDArray[np.bool_]:
        """get overlaps with other shapes. Ignores overlap with oneself."""
        overlaps = self.dwithin(self.shapes[index], distance=min_distance)
        overlaps[index] = False  # ignore overlap with oneself
        return overlaps


def _distance_circ_dot_array(obj: Point2D | AbstractCircularShape,
                             dots_xy: NDArray[np.float64],
                             dots_diameter: NDArray[np.float64]) -> NDArray[np.float64]:
    """Distances circular shape or Point to multiple dots
    """
    d_xy = dots_xy - obj.xy
    if isinstance(obj, Point2D):
        circ_dia = 0
    elif isinstance(obj, Dot):
        circ_dia = obj.diameter
    elif isinstance(obj, Ellipse):
        circ_dia = ellipse_geo.diameter(
            size=np.atleast_2d(obj.size),
            theta=np.arctan2(d_xy[:, 1], d_xy[:, 0]))  # ellipse radius to each dot in the array
    else:
        raise RuntimeError(f"Unknown circular shape type: {type(obj)}")

    # center dist - radius_a - radius_b
    return np.hypot(d_xy[:, 0], d_xy[:, 1]) - (dots_diameter + circ_dia) / 2


def _distance_circ_ellipse_array(obj: Point2D | AbstractCircularShape,
                                 ellipses_xy: NDArray[np.float64],
                                 ellipse_sizes: NDArray[np.float64]) -> NDArray[np.float64]:
    """Distance circular shape or Point2D to multiple ellipses
    """
    d_xy = ellipses_xy - obj.xy
    theta = np.arctan2(d_xy[:, 1], d_xy[:, 0])
    # radii of ellipses in array to circ_shape
    ellipse_dia = ellipse_geo.diameter(size=ellipse_sizes, theta=theta)
    if isinstance(obj, Point2D):
        shape_dia = 0
    elif isinstance(obj, Dot):
        shape_dia = obj.diameter
    elif isinstance(obj, Ellipse):
        shape_dia = ellipse_geo.diameter(size=np.atleast_2d(obj.size),
                                         theta=theta)  # ellipse radius to each ellipse in the array
    else:
        raise RuntimeError(f"Unknown circular shape type: {type(obj)}")

    # center dist - radius_a - radius_b
    return np.hypot(d_xy[:, 0], d_xy[:, 1]) - (ellipse_dia + shape_dia)/2
