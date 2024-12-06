# -*- coding: utf-8 -*-
# Created on Tue Feb  1 15:23:07 2022
# @author: toj
"""
Ray casting and intersection tests


.. currentmodule:: mymesh.rays

Intersection Tests
==================
.. autosummary::
    :toctree: submodules/

    RayTriangleIntersection
    RayTrianglesIntersection
    RaysTrianglesIntersection
    RayBoxIntersection
    RayBoxesIntersection
    PlaneBoxIntersection
    PlaneTriangleIntersection
    PlaneTrianglesIntersection
    TriangleTriangleIntersection
    TriangleTriangleIntersectionPt
    TrianglesTrianglesIntersection
    TrianglesTrianglesIntersectionPts
    TriangleBoxIntersection
    BoxTrianglesIntersection
    SegmentSegmentIntersection
    SegmentsSegmentsIntersection
    RaySegmentsIntersection
    RaySurfIntersection
    RaysSurfIntersection
    RayOctreeIntersection
    SurfSelfIntersection
    SurfSurfIntersection
    PlaneSurfIntersection

Inside/Outside Tests
====================
.. autosummary::
    :toctree: submodules/

    PointInSurf
    PointsInSurf
    PointInBox
    PointsInVoxel
    PointInTri
    PointsInTris
"""
#%%
from . import utils, octree, delaunay, try_njit
import numpy as np
import itertools, random, sys, warnings
import scipy

## Intersection Tests:
def RayTriangleIntersection(pt, ray, TriCoords, bidirectional=False, eps=1e-6):
    """
    Möller-Trumbore intersection algorithm to detect whether a ray intersects with a triangle.
    Möller, T., & Trumbore, B. (2005). Fast, minimum storage ray/triangle intersection. In ACM SIGGRAPH 2005 Courses, SIGGRAPH 2005. https://doi.org/10.1145/1198555.1198746
    :cite:p:`Moller2005`

    For multiple triangles, see :func:`RayTrianglesIntersection` and for multiple rays, see
    :func:`RaysTrianglesIntersection`. 
    
    When choosing between  :func:`RayTriangleIntersection`,  :func:`RayTrianglesIntersection`, and  :func:`RaysTrianglesIntersection`, one should generally only choose the one that has as much vectorization as is needed, and not more. For example, RayTriangleIntersection will generally be slightly more efficient than  :func:`RayTrianglesIntersection` if only one triangle is being considered, but  :func:`RayTrianglesIntersection` will be significantly faster than using :func:`RayTriangleIntersection` many times within a loop.

    Parameters
    ----------
    pt : array_like
        3D coordinates for the starting point of the ray.
    ray : array_like
        3D vector of ray direction. This should, in general, be a unit vector.
    TriCoords : array_like
        Coordinates of the three vertices of the triangle in the format
        ``np.array([[a, b, c], [d, e, f], [g, h, i]])``
    bidirectional : bool, optional
        Determines whether to check for intersections only the direction the ray is pointing,
        or in both directions (±ray), by default False.
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-6

    Returns
    -------
    intersectionPt : np.ndarray or []
        If there is an intersection, the 3D coordinates of the intersection point
        are returned, otherwise [] is returned.
    """    
    edge1 = np.subtract(TriCoords[1],TriCoords[0])
    edge2 = np.subtract(TriCoords[2], TriCoords[0])
    
    p = np.cross(ray, edge2)
    det = np.dot(edge1, p)
    if (det > -eps) and (det < eps):
        return []
    invdet = 1/det
    tvec = np.subtract(pt, TriCoords[0])
    u = np.dot(tvec,p) * invdet
    if (u < 0) or (u > 1):
        return []
    
    q = np.cross(tvec, edge1)
    v = np.dot(ray, q) * invdet
    if (v < 0) or (u+v > 1):
        return []
    
    t = np.dot(edge2, q) * invdet
    if (t > eps) or bidirectional:
        intersectionPt = np.array(pt) + np.array(ray)*t
    else:
        return []
    
    return intersectionPt

def RayTrianglesIntersection(pt, ray, Tris, bidirectional=False, eps=1e-14):
    """
    Vectorized Möller-Trumbore intersection algorithm to detect whether a ray intersects with a set of triangles.
    Möller, T., & Trumbore, B. (2005). Fast, minimum storage ray/triangle intersection. In ACM SIGGRAPH 2005 Courses, SIGGRAPH 2005. https://doi.org/10.1145/1198555.1198746
    :cite:p:`Moller2005`

    This is a vectorized form of RayTriangleIntersection for multiple triangles. For multiple rays,
    see RaysTrianglesIntersection(). 
    
    When choosing between  :func:`RayTriangleIntersection`,  :func:`RayTrianglesIntersection`, and  :func:`RaysTrianglesIntersection`, one should generally only choose the one that has as much vectorization as is needed, and not more. For example, RayTriangleIntersection will generally be slightly more efficient than  :func:`RayTrianglesIntersection` if only one triangle is being considered, but  :func:`RayTrianglesIntersection` will be significantly faster than using :func:`RayTriangleIntersection` many times within a loop.

    Parameters
    ----------
    pt : array_like
        3D coordinates for the starting point of the ray.
    ray : array_like
        3D vector of ray direction. This should, in general, be a unit vector.
    Tris : array_like
        Coordinates of triangle vertices for each triangle in the format
        ``np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...)``
        Should have shape (n,3,3) for n triangles.
    bidirectional : bool, optional
        Determines whether to check for intersections only the direction the ray is pointing,
        or in both directions (±ray), by default False.
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-14

    Returns
    -------
    intersections : np.ndarray
        Indices of triangles that are intersected by ray.
    intersectionPts : np.ndarray
        Coordinates of intersection points for each intersection.
    """    
    with np.errstate(divide='ignore', invalid='ignore'):
        edge1 = Tris[:,1] - Tris[:,0]
        edge2 = Tris[:,2] - Tris[:,0]
        
        p = np.cross(ray, edge2)
        det = np.sum(edge1*p,axis=1)
        
        invdet = 1/det
        tvec = pt - Tris[:,0]
        u = np.sum(tvec*p,axis=1) * invdet
        
        q = np.cross(tvec,edge1)
        v = np.sum(ray*q,axis=1) * invdet
        
        t = np.sum(edge2*q,axis=1) * invdet
        
        checks = (
            ((det > -eps) & (det < eps)) |
            ((u < 0) | (u > 1)) |
            ((v < 0) | (u+v > 1)) |
            ((abs(t) <= eps) & (not bidirectional))
            )
        intersections = np.where(~checks)[0]
        intersectionPts = pt + ray*t[intersections,None]
        
    return intersections, intersectionPts

def RaysTrianglesIntersection(pts, rays, Tris, bidirectional=False, eps=1e-14):
    """
    Vectorized Möller-Trumbore intersection algorithm to detect intersections between a pairwise set of rays and a set of triangles.
    Möller, T., & Trumbore, B. (2005). Fast, minimum storage ray/triangle intersection. In ACM SIGGRAPH 2005 Courses, SIGGRAPH 2005. https://doi.org/10.1145/1198555.1198746
    :cite:p:`Moller2005`

    Note:
        With this version of the intersection test, there must be one ray for each triangle. itertools.combinations can be useful for constructing such a set of pairwise combinations, or see :func:`RaysSurfIntersection` which handles this and can utilize octree acceleration. 

    This is a vectorized form of :func:`RayTriangleIntersection` for multiple triangles. For a single ray with multiple triangles, see :func:`RaysTrianglesIntersection`. 
    
    When choosing between  :func:`RayTriangleIntersection`, :func:`RayTrianglesIntersection`, and  :func:`RaysTrianglesIntersection`, one should generally only choose the one that has as much vectorization as is needed, and not more. For example, RayTriangleIntersection will generally be slightly more efficient than  :func:`RayTrianglesIntersection` if only one triangle is being considered, but  :func:`RayTrianglesIntersection` will be significantly faster than using :func:`RayTriangleIntersection` many times within a loop.

    Parameters
    ----------
    pts : array_like
        2D array-like of 3D coordinates for the starting point of the rays.
        Should have shape (n, 3) for n rays.
    rays : array_like
        2D array-like of 3D vectors of ray directions. These should, in general, be unit vectors.
        Should have shape (n, 3) for n rays.
    Tris : array_like
        Coordinates of triangle vertices for each triangle in the format
        ``np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...)``.
        Should have shape (n,3,3) for n triangles.
    bidirectional : bool, optional
        Determines whether to check for intersections only in the direction the 
        ray is pointing, or in both directions (±ray), by default False.
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-14

    Returns
    -------
    _type_
        _description_
    """

    with np.errstate(divide='ignore', invalid='ignore'):
        edge1 = Tris[:,1] - Tris[:,0]
        edge2 = Tris[:,2] - Tris[:,0]
        
        p = np.cross(rays, edge2)
        det = np.sum(edge1*p,axis=1)
        
        invdet = 1/det
        tvec = pts - Tris[:,0]
        u = np.sum(tvec*p,axis=1) * invdet
        
        q = np.cross(tvec,edge1)
        v = np.sum(rays*q,axis=1) * invdet
        
        t = np.sum(edge2*q,axis=1) * invdet
        
        checks = (
            ((det > -eps) & (det < eps)) |
            ((u < 0) | (u > 1)) |
            ((v < 0) | (u+v > 1)) |
            ((abs(t) <= eps) & (not bidirectional))
            )
        intersections = np.where(~checks)[0]
        intersectionPts = pts[intersections] + rays[intersections]*t[intersections,None]
        
    return intersections, intersectionPts

def RayBoxIntersection(pt, ray, xlim, ylim, zlim):
    """
    Intersection algorithm for detecting intersections between a ray and an axis-aligned box.
    Williams, A., Barrus, S., Morley, R. K., & Shirley, P. (2005). An efficient and robust ray-box intersection algorithm. ACM SIGGRAPH 2005 Courses, SIGGRAPH 2005, 10(1), 55-60. https://www.doi.org/10.1145/1198555.1198748
    :cite:p:`Williams2005`

    Parameters
    ----------
    pt : array_like
        3D coordinates for the starting point of the ray.
    ray : array_like
        3D vector of ray direction. This should, in general, be a unit vector.
    xlim : array_like
        Two element list, array, or tuple with the upper and lower x-direction bounds for an axis-aligned box.
    ylim : array_like
        Two element list, array, or tuple with the upper and lower y-direction bounds for an axis-aligned box.
    zlim : array_like
        Two element list, array, or tuple with the upper and lower z-direction bounds for an axis-aligned box.

    Returns
    -------
    intersection : bool
        True if there is an intersection between the ray and the box, otherwise False.
    """    
    
    if ray[0] > 0:
        divx = 1/ray[0]
        tmin = (xlim[0] - pt[0]) * divx
        tmax = (xlim[1] - pt[0]) * divx
    elif ray[0] < 0:
        divx = 1/ray[0]
        tmin = (xlim[1] - pt[0]) * divx
        tmax = (xlim[0] - pt[0]) * divx
    else:
        tmin = np.sign(xlim[0] - pt[0])*np.inf
        tmax = np.sign(xlim[1] - pt[0])*np.inf
    
    
    if ray[1] > 0:
        divy = 1/ray[1]
        tymin = (ylim[0] - pt[1]) * divy
        tymax = (ylim[1] - pt[1]) * divy
    elif ray[1] < 0:
        divy = 1/ray[1]
        tymin = (ylim[1] - pt[1]) * divy
        tymax = (ylim[0] - pt[1]) * divy
    else:
        tymin = np.sign(ylim[0] - pt[1])*np.inf
        tymax = np.sign(ylim[1] - pt[1])*np.inf
    
    if (tmin > tymax) or (tymin > tmax):
        return False
    if (tymin > tmin):
        tmin = tymin
    if (tymax < tmax):
        tmax = tymax
    
    
    if ray[2] > 0:
        divz = 1/ray[2]
        tzmin = (zlim[0] - pt[2]) * divz
        tzmax = (zlim[1] - pt[2]) * divz
    elif ray[2] < 0:
        divz = 1/ray[2]
        tzmin = (zlim[1] - pt[2]) * divz
        tzmax = (zlim[0] - pt[2]) * divz
    else:
        tzmin = np.sign(zlim[0] - pt[2])*np.inf
        tzmax = np.sign(zlim[1] - pt[2])*np.inf
        
        
    if (tmin > tzmax) or (tzmin > tmax):
        return False
    
    return True

def RayBoxesIntersection(pt, ray, xlims, ylims, zlims):
    """
    Vectorized intersection algorithm for detecting intersections between a ray and a set of axis-aligned boxes.
    Williams, A., Barrus, S., Morley, R. K., & Shirley, P. (2005). An efficient and robust ray-box intersection algorithm. ACM SIGGRAPH 2005 Courses, SIGGRAPH 2005, 10(1), 55-60. https://www.doi.org/10.1145/1198555.1198748
    :cite:p:`Williams2005`

    Parameters
    ----------
    pt : array_like
        3D coordinates for the starting point of the ray.
    ray : array_like
        3D vector of ray direction. This should, in general, be a unit vector.
    xlims : array_like
        2D array_like with the upper and lower x-direction bounds for each axis-aligned box. Should have shape (n,2).
    ylims : array_like
        2D array_like with the upper and lower y-direction bounds for each axis-aligned box. Should have shape (n,2).
    zlims : array_like
        2D array_like with the upper and lower z-direction bounds for each axis-aligned box. Should have shape (n,2).

    Returns
    -------
    intersections : np.ndarray()
        Array of booleans, True if there is an intersection between the ray and the box, otherwise False.
    """    
    xlims = np.asarray(xlims)
    ylims = np.asarray(ylims)
    zlims = np.asarray(zlims)
    intersections = np.repeat(True, len(xlims))

    if ray[0] > 0:
        divx = 1/ray[0]
        tmin = (xlims[:,0] - pt[0]) * divx
        tmax = (xlims[:,1] - pt[0]) * divx
    elif ray[0] < 0:
        divx = 1/ray[0]
        tmin = (xlims[:,1] - pt[0]) * divx
        tmax = (xlims[:,0] - pt[0]) * divx
    else:
        tmin = np.sign(xlims[:,0] - pt[0])*np.inf
        tmax = np.sign(xlims[:,1] - pt[0])*np.inf
    
    if ray[1] > 0:
        divy = 1/ray[1]
        tymin = (ylims[:,0] - pt[1]) * divy
        tymax = (ylims[:,1] - pt[1]) * divy
    elif ray[1] < 0:
        divy = 1/ray[1]
        tymin = (ylims[:,1] - pt[1]) * divy
        tymax = (ylims[:,0] - pt[1]) * divy
    else:
        tymin = np.sign(ylims[:,0] - pt[1])*np.inf
        tymax = np.sign(ylims[:,1] - pt[1])*np.inf
    
    intersections[(tmin > tymax) | (tymin > tmax)] = False
    tmin = np.maximum(tymin, tmin)
    tmax = np.minimum(tymax, tmax)
    
    # tzmin/tzmax only calculated for intersections not already found to be false
    if ray[2] > 0:
        divz = 1/ray[2]
        tzmin = (zlims[intersections,0] - pt[2]) * divz
        tzmax = (zlims[intersections,1] - pt[2]) * divz
    elif ray[2] < 0:
        divz = 1/ray[2]
        tzmin = (zlims[intersections,1] - pt[2]) * divz
        tzmax = (zlims[intersections,0] - pt[2]) * divz
    else:
        tzmin = np.sign(zlims[intersections,0] - pt[2])*np.inf
        tzmax = np.sign(zlims[intersections,1] - pt[2])*np.inf
    
    # TODO: Somethings wrong - probably here
    intersections[intersections] = ~((tmin[intersections] > tzmax) | (tzmin > tmax[intersections]))
    return intersections

def PlaneBoxIntersection(pt, Normal, xlim, ylim, zlim):
    """
    Intersection algorithm for detecting intersections between a plane and an axis-aligned box.

    Parameters
    ----------
    pt : array_like
        3D coordinates for a point on the plane
    Normal : array_like
        3D vector representing the normal vector to the plane
    xlim : array_like
        Two element list, array, or tuple with the upper and lower x-direction bounds for an axis-aligned box.
    ylim : array_like
        Two element list, array, or tuple with the upper and lower y-direction bounds for an axis-aligned box.
    zlim : array_like
        Two element list, array, or tuple with the upper and lower z-direction bounds for an axis-aligned box.

    Returns
    -------
    intersection : bool
        True if there is an intersection, otherwise False.
    """    

    BoxCoords = [
        [xlim[0],ylim[0],zlim[0]],
        [xlim[1],ylim[0],zlim[0]],
        [xlim[0],ylim[1],zlim[0]],
        [xlim[1],ylim[1],zlim[0]],
        [xlim[0],ylim[0],zlim[1]],
        [xlim[1],ylim[0],zlim[1]],
        [xlim[0],ylim[1],zlim[1]],
        [xlim[1],ylim[1],zlim[1]],
        ]
    # Signed Distances from the vertices of the box to the plane
    sd = [np.dot(Normal,p)-np.dot(Normal,pt) for p in BoxCoords]
    signs = [np.sign(x) for x in sd]
    if all(signs) == 1 or all(signs) == -1:
        # No Intersection, all points on same side of plane
        intersection = False
    else:
        # Intersection, points on different sides of the plane
        intersection = True
    return intersection
    
def PlaneTriangleIntersection(pt, Normal, TriCoords):
    """
    Intersection test for detecting intersections between a plane and a triangle.

    An intersection will be detected if points are on different sides of the plane, or if any points lie exactly on the plane.

    Parameters
    ----------
    pt : array_like
        3 element array, point on plane 
    Normal : array_like
        3 element array, normal vector to plane 
    TriCoords : array_like
        Coordinates of the three vertices of the triangle in the format
        ``np.array([[a, b, c], [d, e, f], [g, h, i]])``

    Returns
    -------
    intersection : bool
        True if there is an intersection, otherwise False.
    """    
    # Signed Distances from the vertices of the box to the plane
    sd = [np.dot(Normal,p)-np.dot(Normal,pt) for p in TriCoords]
    signs = [np.sign(x) for x in sd]
    if all(signs) == 1 or all(signs) == -1:
        # No Intersection, all points on same side of plane
        intersection = False
    else:
        # Intersection, points on different sides of the plane
        intersection = True
    return intersection
    
def PlaneTrianglesIntersection(pt, Normal, Tris, eps=1e-14):
    """
    Vectorized intersection test for detecting intersections between a plane and a set of triangles.

    An intersection will be detected if points are on different sides of the plane, or if any points lie exactly on the plane. That are a distance +/- eps from the plane will be considered as on the plane.

    Parameters
    ----------
    pt : array_like
        3 element array, point on plane 
    Normal : array_like
        3 element array, normal vector to plane 
    Tris : array_like
        Coordinates of triangle vertices for each triangle in the format
        np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...).
        Should have shape (n,3,3) for n triangles.
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-14

    Returns
    -------
    intersections : np.ndarray
        Array of bools for each triangle, True of there is an intersection, otherwise False.
    """   

    Tris = np.asarray(Tris)
    pt = np.asarray(pt)
    Normal = np.asarray(Normal)/np.linalg.norm(Normal)
    sd = np.sum(Normal*Tris,axis=2) - np.dot(Normal,pt)
    intersections = ~(np.all((sd < -eps),axis=1) | np.all((sd > eps),axis=1))

    return intersections
    
def TriangleTriangleIntersection(Tri1,Tri2,eps=1e-14,edgeedge=False):
    """
    Intersection test for two triangles. 

    Möller, T. (1997). Fast triangle-triangle intersection test. Journal of Graphics Tools, 2(2), 25-30. https://doi.org/10.1080/10867651.1997.10487472
    :cite:p:`Moller1997`

    Parameters
    ----------
    Tri1 : array_like
        Coordinates of the three vertices of the first triangle in the format
        ``np.array([[a, b, c], [d, e, f], [g, h, i]])``
    Tri2 : array_like
        Coordinates of the three vertices of the second triangle in the format
        ``np.array([[a, b, c], [d, e, f], [g, h, i]])``
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-14
    edgeedge : bool, optional
        If ``edgeedge`` is true, two triangles that meet exactly at the edges will be counted as an intersection, by default False. This inclues two adjacent triangles that share an edge, but also cases where two points of Tri1 lie exactly on the edges of Tri2.

    Returns
    -------
    intersection : bool
        True if there is an intersection, otherwise False.
    """    

    if type(Tri1) is list: Tri1 = np.array(Tri1)
    if type(Tri2) is list: Tri2 = np.array(Tri2)

    # Plane2 (N2.X+d2):
    N2 = np.cross(np.subtract(Tri2[1,:],Tri2[0,:]),np.subtract(Tri2[2,:],Tri2[0,:]))
    d2 = -np.dot(N2,Tri2[0,:])
    
    # Signed distances from vertices in Tri1 to Plane2:
    sd1 = np.round([np.dot(N2,v)+d2 for v in Tri1],16)
    signs1 = np.sign(sd1)
    if all(signs1 == 1) or all(signs1 == -1):
        # All vertices of Tri1 are on the same side of Plane2
        return False
    elif all(np.abs(sd1) < eps):
        # Coplanar
        # Perform Edge Intersection
        edges = np.array([[0,1],[1,2],[2,0]])
        edges1idx = np.array([edges[0],edges[1],edges[2],edges[0],edges[1],edges[2],edges[0],edges[1],edges[2]])
        edges2idx = np.array([edges[0],edges[1],edges[2],edges[1],edges[2],edges[0],edges[2],edges[0],edges[1]])
        edges1 = Tri1[edges1idx]
        edges2 = Tri2[edges2idx]

        intersections = SegmentsSegmentsIntersection(edges1,edges2,return_intersection=False,eps=eps)
        if any(intersections):
            return True
        else:
            # Peform point-in-tri test
            alpha,beta,gamma = utils.BaryTri(Tri1, Tri2[0])
            if all([alpha>=0,beta>=0,gamma>=0]):
                return True
            else:
                alpha,beta,gamma = utils.BaryTri(Tri2, Tri1[0])
                if all([alpha>=0,beta>=0,gamma>=0]):
                    return True
                else:
                    return False
    
    # Plane1 (N1.X+d1): 
    N1 = np.cross(np.subtract(Tri1[1,:],Tri1[0,:]),np.subtract(Tri1[2,:],Tri1[0,:]))
    d1 = -np.dot(N1,Tri1[0,:])
    
    # Signed distances from vertices in Tri1 to Plane2:
    # sd2 = np.round([np.dot(N1,v)+d1 for v in Tri2],16)
    sd2 = np.array([np.dot(N1,v)+d1 for v in Tri2])
    signs2 = np.sign(sd2)
    if all(signs2 == 1) or all(signs2 == -1):
        # All vertices of Tri2 are on the same side of Plane1
        return False

    # Intersection line of Tri1 & Tri2: L = O+tD
    D = np.cross(N1,N2).tolist()
  
    Dmax = max(D)
    # Projections of Tri1 to L
    Pv1 = np.array([v[D.index(Dmax)] for v in Tri1])

    if signs1[0] == signs1[2] :
        t11 = Pv1[0] + (Pv1[1]-Pv1[0])*sd1[0]/(sd1[0]-sd1[1])
        t12 = Pv1[2] + (Pv1[1]-Pv1[2])*sd1[2]/(sd1[2]-sd1[1])
    elif signs1[0] == signs1[1]:
        t11 = Pv1[0] + (Pv1[2]-Pv1[0])*sd1[0]/(sd1[0]-sd1[2])
        t12 = Pv1[1] + (Pv1[2]-Pv1[1])*sd1[1]/(sd1[1]-sd1[2])
    elif signs1[1] == signs1[2]:
        t11 = Pv1[2] + (Pv1[0]-Pv1[2])*sd1[2]/(sd1[2]-sd1[0])
        t12 = Pv1[1] + (Pv1[0]-Pv1[1])*sd1[1]/(sd1[1]-sd1[0])
    elif signs1[1] != 0:
        t11 = Pv1[0] + (Pv1[1]-Pv1[0])*sd1[0]/(sd1[0]-sd1[1])
        t12 = Pv1[2] + (Pv1[1]-Pv1[2])*sd1[2]/(sd1[2]-sd1[1])
    elif signs1[2] != 0:
        t11 = Pv1[0] + (Pv1[2]-Pv1[0])*sd1[0]/(sd1[0]-sd1[2])
        t12 = Pv1[1] + (Pv1[2]-Pv1[1])*sd1[1]/(sd1[1]-sd1[2])
    else:
        t11 = Pv1[2] + (Pv1[0]-Pv1[2])*sd1[2]/(sd1[2]-sd1[0])
        t12 = Pv1[1] + (Pv1[0]-Pv1[1])*sd1[1]/(sd1[1]-sd1[0])
    # Projections of Tri2 to L
    Pv2 = np.array([v[D.index(Dmax)] for v in Tri2])

    # sumzero = np.sum(signs2==0)
    if signs2[0] == signs2[2]:
        t21 = Pv2[0] + (Pv2[1]-Pv2[0])*sd2[0]/(sd2[0]-sd2[1])
        t22 = Pv2[2] + (Pv2[1]-Pv2[2])*sd2[2]/(sd2[2]-sd2[1])
    elif signs2[0] == signs2[1]:
        t21 = Pv2[0] + (Pv2[2]-Pv2[0])*sd2[0]/(sd2[0]-sd2[2])
        t22 = Pv2[1] + (Pv2[2]-Pv2[1])*sd2[1]/(sd2[1]-sd2[2])
    elif signs2[1] == signs2[2]:
        t21 = Pv2[2] + (Pv2[0]-Pv2[2])*sd2[2]/(sd2[2]-sd2[0])
        t22 = Pv2[1] + (Pv2[0]-Pv2[1])*sd2[1]/(sd2[1]-sd2[0])
    elif signs2[1] != 0:
        t21 = Pv2[0] + (Pv2[1]-Pv2[0])*sd2[0]/(sd2[0]-sd2[1])
        t22 = Pv2[2] + (Pv2[1]-Pv2[2])*sd2[2]/(sd2[2]-sd2[1])
    elif signs2[2] != 0:
        t21 = Pv2[0] + (Pv2[2]-Pv2[0])*sd2[0]/(sd2[0]-sd2[2])
        t22 = Pv2[1] + (Pv2[2]-Pv2[1])*sd2[1]/(sd2[1]-sd2[2])
    else:
        t21 = Pv2[2] + (Pv2[0]-Pv2[2])*sd2[2]/(sd2[2]-sd2[0])
        t22 = Pv2[1] + (Pv2[0]-Pv2[1])*sd2[1]/(sd2[1]-sd2[0])

   
    t11,t12 = min([t11,t12]),max([t11,t12])
    t21,t22 = min([t21,t22]),max([t21,t22])
    
    # if (t12 <= t21 or t22 <= t11) or (t11 == t21 and t12 == t22):
    if (t12-t21 <= eps or t22-t11 <= eps) or ((not edgeedge) and abs(t11-t21) < eps and abs(t12-t22) < eps):
        return False
    return True

def TriangleTriangleIntersectionPt(Tri1,Tri2,eps=1e-14, edgeedge=False):
    """
    Intersection test for two triangles that returns the point(s) of intersection. 

    Möller, T. (1997). Fast triangle-triangle intersection test. Journal of Graphics Tools, 2(2), 25-30. https://doi.org/10.1080/10867651.1997.10487472
    :cite:p:`Moller1997`

    Parameters
    ----------
    Tri1 : array_like
        Coordinates of the three vertices of the first triangle in the format
        ``np.array([[a, b, c], [d, e, f], [g, h, i]])``
    Tri2 : array_like
        Coordinates of the three vertices of the second triangle in the format
        ``np.array([[a, b, c], [d, e, f], [g, h, i]])``
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-14
    edgeedge : bool, optional
        If ``edgeedge`` is true, two triangles that meet exactly at the edges will be counted as an intersection, by default False. This inclues two adjacent triangles that share an edge, but also cases where two points of Tri1 lie exactly on the edges of Tri2.

    Returns
    -------
    points : array_like
        Array of points where the two triangles intersect.
    """    
    
    # Plane2 (N2.X+d2):
    N2 = np.cross(np.subtract(Tri2[1],Tri2[0]),np.subtract(Tri2[2],Tri2[0]))
    d2 = -np.dot(N2,Tri2[0])
    
    # Signed distances from vertices in Tri1 to Plane2:
    sd1 = np.round([np.dot(N2,v)+d2 for v in Tri1],16)
    signs1 = np.sign(sd1)
    if all(signs1 == 1) or all(signs1 == -1):
        # All vertices of Tri1 are on the same side of Plane2
        return []
    elif all(np.abs(sd1) < eps):
        # Coplanar
        # Perform Edge Intersection
        edges = np.array([[0,1],[1,2],[2,0]])
        edges1idx = np.array([edges[0],edges[1],edges[2],edges[0],edges[1],edges[2],edges[0],edges[1],edges[2]])
        edges2idx = np.array([edges[0],edges[1],edges[2],edges[1],edges[2],edges[0],edges[2],edges[0],edges[1]])
        edges1 = Tri1[edges1idx]
        edges2 = Tri2[edges2idx]

        intersections,pts = SegmentsSegmentsIntersection(edges1,edges2,return_intersection=True,eps=eps)
        if any(intersections):
            points = pts[intersections]
            # Check if there are any verticies within the triangles
            for i in range(3):
                alpha,beta,gamma = utils.BaryTri(Tri1, Tri2[i])
                if all([alpha>=0,beta>=0,gamma>=0]):
                    points = np.vstack([points,Tri2[i]])
                alpha,beta,gamma = utils.BaryTri(Tri2, Tri1[i])
                if all([alpha>=0,beta>=0,gamma>=0]):
                    points = np.vstack([points,Tri1[i]])
            return points
        else:
            # Peform point-in-tri test
            alpha,beta,gamma = utils.BaryTri(Tri1, Tri2[0])
            if all([alpha>=0,beta>=0,gamma>=0]):
                return Tri2
            else:
                alpha,beta,gamma = utils.BaryTri(Tri2, Tri1[0])
                if all([alpha>=0,beta>=0,gamma>=0]):
                    return Tri1
                else:
                    return []
    
    # Plane1 (N1.X+d1): 
    N1 = np.cross(np.subtract(Tri1[1],Tri1[0]),np.subtract(Tri1[2],Tri1[0]))
    d1 = -np.dot(N1,Tri1[0])
    
    # Signed distances from vertices in Tri1 to Plane2:
    sd2 = np.round([np.dot(N1,v)+d1 for v in Tri2],16)
    signs2 = np.sign(sd2)
    if all(signs2 == 1) or all(signs2 == -1):
        # All vertices of Tri2 are on the same side of Plane1
        return []

    # Intersection line of Tri1 & Tri2: L = O+tD
    D = np.cross(N1,N2)
    D = D/np.linalg.norm(D)
    if abs(D[0]) == max(np.abs(D)):
        Ox = 0
        Oy = -(d1*N2[2]-d2*N1[2])/(N1[1]*N2[2] - N2[1]*N1[2])
        Oz = -(d2*N1[1]-d1*N2[1])/(N1[1]*N2[2] - N2[1]*N1[2])
    elif abs(D[1]) == max(np.abs(D)):
        Ox = -(d1*N2[2]-d2*N1[2])/(N1[0]*N2[2] - N2[0]*N1[2])
        Oy = 0
        Oz = -(d2*N1[0]-d1*N2[0])/(N1[0]*N2[2] - N2[0]*N1[2])
    else: #elif abs(D[2]) == max(np.abs(D)):
        Ox = -(d1*N2[1]-d2*N1[1])/(N1[0]*N2[1] - N2[0]*N1[1])
        Oy = -(d2*N1[0]-d1*N2[0])/(N1[0]*N2[1] - N2[0]*N1[1])
        Oz = 0
    O = [Ox,Oy,Oz]

    # Dmax = max(D)
    # Projections of Tri1 to L
    # Pv1 = [v[D.index(Dmax)] for v in Tri1]
    Pv1 = [np.dot(D,(v-O)) for v in Tri1]
    

    if signs1[0] == signs1[2] :
        t11 = Pv1[0] + (Pv1[1]-Pv1[0])*sd1[0]/(sd1[0]-sd1[1])
        t12 = Pv1[2] + (Pv1[1]-Pv1[2])*sd1[2]/(sd1[2]-sd1[1])
    elif signs1[0] == signs1[1]:
        t11 = Pv1[0] + (Pv1[2]-Pv1[0])*sd1[0]/(sd1[0]-sd1[2])
        t12 = Pv1[1] + (Pv1[2]-Pv1[1])*sd1[1]/(sd1[1]-sd1[2])
    elif signs1[1] == signs1[2]:
        t11 = Pv1[2] + (Pv1[0]-Pv1[2])*sd1[2]/(sd1[2]-sd1[0])
        t12 = Pv1[1] + (Pv1[0]-Pv1[1])*sd1[1]/(sd1[1]-sd1[0])
    elif signs1[1] != 0:
        t11 = Pv1[0] + (Pv1[1]-Pv1[0])*sd1[0]/(sd1[0]-sd1[1])
        t12 = Pv1[2] + (Pv1[1]-Pv1[2])*sd1[2]/(sd1[2]-sd1[1])
    elif signs1[2] != 0:
        t11 = Pv1[0] + (Pv1[2]-Pv1[0])*sd1[0]/(sd1[0]-sd1[2])
        t12 = Pv1[1] + (Pv1[2]-Pv1[1])*sd1[1]/(sd1[1]-sd1[2])
    else:
        t11 = Pv1[2] + (Pv1[0]-Pv1[2])*sd1[2]/(sd1[2]-sd1[0])
        t12 = Pv1[1] + (Pv1[0]-Pv1[1])*sd1[1]/(sd1[1]-sd1[0])
    # Projections of Tri2 to L
    # Pv2 = [v[D.index(Dmax)] for v in Tri2]
    Pv2 = [np.dot(D,(v-O)) for v in Tri2]
    # sumzero = np.sum(signs2==0)
    if signs2[0] == signs2[2]:
        t21 = Pv2[0] + (Pv2[1]-Pv2[0])*sd2[0]/(sd2[0]-sd2[1])
        t22 = Pv2[2] + (Pv2[1]-Pv2[2])*sd2[2]/(sd2[2]-sd2[1])
    elif signs2[0] == signs2[1]:
        t21 = Pv2[0] + (Pv2[2]-Pv2[0])*sd2[0]/(sd2[0]-sd2[2])
        t22 = Pv2[1] + (Pv2[2]-Pv2[1])*sd2[1]/(sd2[1]-sd2[2])
    elif signs2[1] == signs2[2]:
        t21 = Pv2[2] + (Pv2[0]-Pv2[2])*sd2[2]/(sd2[2]-sd2[0])
        t22 = Pv2[1] + (Pv2[0]-Pv2[1])*sd2[1]/(sd2[1]-sd2[0])
    elif signs2[1] != 0:
        t21 = Pv2[0] + (Pv2[1]-Pv2[0])*sd2[0]/(sd2[0]-sd2[1])
        t22 = Pv2[2] + (Pv2[1]-Pv2[2])*sd2[2]/(sd2[2]-sd2[1])
    elif signs2[2] != 0:
        t21 = Pv2[0] + (Pv2[2]-Pv2[0])*sd2[0]/(sd2[0]-sd2[2])
        t22 = Pv2[1] + (Pv2[2]-Pv2[1])*sd2[1]/(sd2[1]-sd2[2])
    else:
        t21 = Pv2[2] + (Pv2[0]-Pv2[2])*sd2[2]/(sd2[2]-sd2[0])
        t22 = Pv2[1] + (Pv2[0]-Pv2[1])*sd2[1]/(sd2[1]-sd2[0])

   
    t11,t12 = min([t11,t12]),max([t11,t12])
    t21,t22 = min([t21,t22]),max([t21,t22])
    
    # if (t12 <= t21 or t22 <= t11) or (t11 == t21 and t12 == t22):
    if (t12-t21 <= eps or t22-t11 <= eps) or ((not edgeedge) and abs(t11-t21) < eps and abs(t12-t22) < eps):
        return []

    t1,t2 = np.sort([t11,t12,t21,t22])[1:3]
    edge = np.array([O + t1*D, O + t2*D])
    
    return edge
    
def TrianglesTrianglesIntersection(Tri1s,Tri2s,eps=1e-14,edgeedge=False):
    """
    Vectorized intersection test for two sets of triangles. 

    Möller, T. (1997). Fast triangle-triangle intersection test. Journal of Graphics Tools, 2(2), 25-30. https://doi.org/10.1080/10867651.1997.10487472
    :cite:p:`Moller1997`

    Parameters
    ----------
    Tri1s : array_like
        Coordinates of triangle vertices for each triangle in the format
        ``np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...)``.
        Should have shape (n,3,3) for n triangles.
    Tri2s : array_like
        Coordinates of triangle vertices for each triangle in the format
        ``np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...)``.
        Should have shape (n,3,3) for n triangles.
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-14
    edgeedge : bool, optional
        If ``edgeedge`` is true, two triangles that meet exactly at the edges will be counted as an intersection, by default False. This inclues two adjacent triangles that share an edge, but also cases where two points of Tri1 lie exactly on the edges of Tri2.

    Returns
    -------
    Intersections : np.ndarray
        Array of bools for each pair of triangles. True if there is an intersection, otherwise False.
    """    
    # TODO: Currently considering coplanar as a non-intersection, need to implement a separate coplanar test
    
    # Plane2 (N2.X+d2):
    N2s = np.cross(np.subtract(Tri2s[:,1],Tri2s[:,0]),np.subtract(Tri2s[:,2],Tri2s[:,0]))
    d2s = -np.sum(N2s*Tri2s[:,0,:],axis=1)

    # Signed distances from vertices in Tri1 to Plane2:
    sd1s = np.round([np.sum(N2s*Tri1s[:,i],axis=1)+d2s for i in range(3)],16).T
    signs1 = np.sign(sd1s)
    
    # Plane1 (N1.X+d1): 
    N1s = np.cross(np.subtract(Tri1s[:,1],Tri1s[:,0]),np.subtract(Tri1s[:,2],Tri1s[:,0]))
    d1s = -np.sum(N1s*Tri1s[:,0,:],axis=1)
    
    # Signed distances from vertices in Tri1 to Plane2:
    sd2s = np.round([np.sum(N1s*Tri2s[:,i],axis=1)+d1s for i in range(3)],16).T
    signs2 = np.sign(sd2s)
    
    # Intersection line of Tri1 & Tri2: L = O+tD
    Ds = np.cross(N1s,N2s)
    Dmaxs = np.max(Ds,axis=1)
    
    # Projections of Tri1 to L
    Pv1s = Tri1s.transpose(0,2,1)[(Ds==Dmaxs[:,None]) & ((Ds==Dmaxs[:,None])*[3,2,1] == np.max((Ds==Dmaxs[:,None])*[3,2,1],axis=1)[:,None])]
    # Projections of Tri2 to L
    Pv2s = Tri2s.transpose(0,2,1)[(Ds==Dmaxs[:,None]) & ((Ds==Dmaxs[:,None])*[3,2,1] == np.max((Ds==Dmaxs[:,None])*[3,2,1],axis=1)[:,None])]

    t11s = np.zeros(len(Tri1s)); t12s = np.zeros(len(Tri1s))
    t21s = np.zeros(len(Tri1s)); t22s = np.zeros(len(Tri1s))
    
    with np.errstate(divide='ignore', invalid='ignore'):
        # if signs[:,0] == signs[:,2]:

        a = (signs1[:,0] == signs1[:,2]) 
        b = (signs1[:,0] == signs1[:,1]) 
        c = (signs1[:,1] == signs1[:,2]) 

        A = ((signs1[:,1]!=0)) & ~(a|b|c)
        B = ((signs1[:,2]!=0)) & ~(a|b|c)
        C = ((signs1[:,0]!=0)) & ~(a|b|c)

        Aa = (A | a)
        Bb = (B | b) & ~Aa
        Cc = (C | c) & ~(Aa|Bb)
        
        t11s[Aa] = Pv1s[Aa,0] + (Pv1s[Aa,1]-Pv1s[Aa,0])*sd1s[Aa,0]/(sd1s[Aa,0]-sd1s[Aa,1])
        t12s[Aa] = Pv1s[Aa,2] + (Pv1s[Aa,1]-Pv1s[Aa,2])*sd1s[Aa,2]/(sd1s[Aa,2]-sd1s[Aa,1])
        
        t11s[Bb] = Pv1s[Bb,0] + (Pv1s[Bb,2]-Pv1s[Bb,0])*sd1s[Bb,0]/(sd1s[Bb,0]-sd1s[Bb,2])
        t12s[Bb] = Pv1s[Bb,1] + (Pv1s[Bb,2]-Pv1s[Bb,1])*sd1s[Bb,1]/(sd1s[Bb,1]-sd1s[Bb,2])
        
        t11s[Cc] = Pv1s[Cc,2] + (Pv1s[Cc,0]-Pv1s[Cc,2])*sd1s[Cc,2]/(sd1s[Cc,2]-sd1s[Cc,0])
        t12s[Cc] = Pv1s[Cc,1] + (Pv1s[Cc,0]-Pv1s[Cc,1])*sd1s[Cc,1]/(sd1s[Cc,1]-sd1s[Cc,0])
    
    
        a = (signs2[:,0] == signs2[:,2]) 
        b = (signs2[:,0] == signs2[:,1]) 
        c = (signs2[:,1] == signs2[:,2]) 

        A = ((signs2[:,1]!=0)) & ~(a|b|c)
        B = ((signs2[:,2]!=0)) & ~(a|b|c)
        C = ((signs2[:,0]!=0)) & ~(a|b|c)

        Aa = (A | a)
        Bb = (B | b) & ~Aa
        Cc = (C | c) & ~(Aa|Bb)

        t21s[Aa] = Pv2s[Aa,0] + (Pv2s[Aa,1]-Pv2s[Aa,0])*sd2s[Aa,0]/(sd2s[Aa,0]-sd2s[Aa,1])
        t22s[Aa] = Pv2s[Aa,2] + (Pv2s[Aa,1]-Pv2s[Aa,2])*sd2s[Aa,2]/(sd2s[Aa,2]-sd2s[Aa,1])
        
        t21s[Bb] = Pv2s[Bb,0] + (Pv2s[Bb,2]-Pv2s[Bb,0])*sd2s[Bb,0]/(sd2s[Bb,0]-sd2s[Bb,2])
        t22s[Bb] = Pv2s[Bb,1] + (Pv2s[Bb,2]-Pv2s[Bb,1])*sd2s[Bb,1]/(sd2s[Bb,1]-sd2s[Bb,2])
        
        t21s[Cc] = Pv2s[Cc,2] + (Pv2s[Cc,0]-Pv2s[Cc,2])*sd2s[Cc,2]/(sd2s[Cc,2]-sd2s[Cc,0])
        t22s[Cc] = Pv2s[Cc,1] + (Pv2s[Cc,0]-Pv2s[Cc,1])*sd2s[Cc,1]/(sd2s[Cc,1]-sd2s[Cc,0])
    
        t11s,t12s = np.fmin(t11s,t12s),np.fmax(t11s,t12s)
        t21s,t22s = np.fmin(t21s,t22s),np.fmax(t21s,t22s)
        
        # Initialize Intersections Array
        Intersections = np.repeat(True,len(Tri1s))
        
        # Perform Checks
        edgeedgebool = np.repeat(edgeedge,len(signs1))
        coplanar = np.all(np.abs(sd1s) < eps, axis=1)
        checks = (np.all(signs1==1,axis=1) | np.all(signs1==-1,axis=1) |
                 np.all(signs2==1,axis=1) | np.all(signs2==-1,axis=1) |
                 (t12s-t21s <= eps) | (t22s-t11s <= eps) | 
                 (~edgeedgebool & (np.abs(t11s-t21s) < eps) & (np.abs(t12s-t22s) < eps)))

        Intersections[checks | coplanar] = False
        
        CoTri1s = Tri1s[coplanar]
        CoTri2s = Tri2s[coplanar]
        edges = np.array([[0,1],[1,2],[2,0]])
        edges1idx = np.array([edges[0],edges[1],edges[2],edges[0],edges[1],edges[2],edges[0],edges[1],edges[2]])
        edges2idx = np.array([edges[0],edges[1],edges[2],edges[1],edges[2],edges[0],edges[2],edges[0],edges[1]])
        edges1 = CoTri1s[:,edges1idx]
        edges2 = CoTri2s[:,edges2idx]

        coplanar_where = np.where(coplanar)[0] 

        edges1r = edges1.reshape(edges1.shape[0]*edges1.shape[1],edges1.shape[2],edges1.shape[3])
        edges2r = edges2.reshape(edges2.shape[0]*edges2.shape[1],edges2.shape[2],edges2.shape[3])
        intersectionsr = SegmentsSegmentsIntersection(edges1r,edges2r,return_intersection=False,eps=eps)
        
        intersections = intersectionsr.reshape(edges1.shape[0],edges1.shape[1])

        Intersections[coplanar_where] = np.any(intersections,axis=1)

        PtInTriChecks = coplanar_where[~Intersections[coplanar_where]]
        for i in PtInTriChecks:
            # Peform point-in-tri test
            alpha,beta,gamma = utils.BaryTri(Tri1s[i], Tri2s[i][0])
            if all([alpha>=0,beta>=0,gamma>=0]):
                Intersections[i]  = True
            else:
                alpha,beta,gamma = utils.BaryTri(Tri2s[i], Tri1s[i][0])
                if all([alpha>=0,beta>=0,gamma>=0]):
                    Intersections[i]  = True
        ###
        # coplanar_intersections = np.repeat(False,len(coplanar))
        # for i in range(len(edges1)):
        #     intersections = SegmentsSegmentsIntersection(edges1,edges2,return_intersection=False)
        #     if any(intersections):
        #         coplanar_intersections[coplanar_where[i]] = True                
        #     else:
        #         # Peform point-in-tri test
        #         alpha,beta,gamma = utils.BaryTri(Tri1s[coplanar_where[i]], Tri2s[coplanar_where[i]][0])
        #         if all([alpha>=0,beta>=0,gamma>=0]):
        #             coplanar_intersections[coplanar_where[i]]  = True
        #         else:
        #             alpha,beta,gamma = utils.BaryTri(Tri2s[coplanar_where[i]], Tri1s[coplanar_where[i]][0])
        #             if all([alpha>=0,beta>=0,gamma>=0]):
        #                 coplanar_intersections[coplanar_where[i]]  = True
        
    return Intersections
    
def TrianglesTrianglesIntersectionPts(Tri1s,Tri2s,eps=1e-14,edgeedge=False):
    """
    Vectorized intersection test for two sets of triangles that returns the intersection point(s) between each pair of triangles. 

    Möller, T. (1997). Fast triangle-triangle intersection test. Journal of Graphics Tools, 2(2), 25-30. https://doi.org/10.1080/10867651.1997.10487472
    :cite:p:`Moller1997`

    Parameters
    ----------
    Tri1s : array_like
        Coordinates of triangle vertices for each triangle in the format
        ``np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...)``.
        Should have shape (n,3,3) for n triangles.
    Tri2s : array_like
        Coordinates of triangle vertices for each triangle in the format
        ``np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...)``.
        Should have shape (n,3,3) for n triangles.
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-14
    edgeedge : bool, optional
        If ``edgeedge`` is true, two triangles that meet exactly at the edges will be counted as an intersection, by default False. This inclues two adjacent triangles that share an edge, but also cases where two points of Tri1 lie exactly on the edges of Tri2.

    Returns
    -------
    Intersections : np.ndarray
        Array of bools for each pair of triangles. True if there is an intersection, otherwise False.
    IntersectionPts : list
        List of intersection point(s) for each pair of triangle.
    """    
    # TODO: Currently considering coplanar as a non-intersection, need to implement a separate coplanar test
    
    # Plane2 (N2.X+d2):
    N2s = np.cross(np.subtract(Tri2s[:,1],Tri2s[:,0]),np.subtract(Tri2s[:,2],Tri2s[:,0]))
    d2s = -np.sum(N2s*Tri2s[:,0,:],axis=1)

    # Signed distances from vertices in Tri1 to Plane2:
    sd1s = np.array([np.sum(N2s*Tri1s[:,i],axis=1)+d2s for i in range(3)]).T
    signs1 = np.sign(sd1s)
    signs1[np.abs(sd1s) < eps] = 0
    
    # Plane1 (N1.X+d1): 
    N1s = np.cross(np.subtract(Tri1s[:,1],Tri1s[:,0]),np.subtract(Tri1s[:,2],Tri1s[:,0]))
    d1s = -np.sum(N1s*Tri1s[:,0,:],axis=1)
    
    # Signed distances from vertices in Tri1 to Plane2:
    sd2s = np.array([np.sum(N1s*Tri2s[:,i],axis=1)+d1s for i in range(3)]).T
    signs2 = np.sign(sd2s)
    signs2[np.abs(sd2s) < eps] = 0
    
    # Intersection line of Tri1 & Tri2: L = O+tD
    Ds = np.cross(N1s,N2s)
    norm = np.linalg.norm(Ds,axis=1)
    Ds = np.divide(Ds,norm[:,None],where=(norm>0)[:,None],out=Ds)
    # Dmaxs = np.max(Ds,axis=1)
    absDs = np.abs(Ds)

    O = np.nan*np.zeros((len(Tri1s),3))
    o1 = absDs[:,0] == np.max(absDs,axis=1) 
    o2 = absDs[:,1] == np.max(absDs,axis=1)
    o3 = absDs[:,2] == np.max(absDs,axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        O[o1] = np.array([
                np.zeros(np.sum(o1)),
                -(d1s[o1]*N2s[o1,2]-d2s[o1]*N1s[o1,2])/(N1s[o1,1]*N2s[o1,2] - N2s[o1,1]*N1s[o1,2]),
                -(d2s[o1]*N1s[o1,1]-d1s[o1]*N2s[o1,1])/(N1s[o1,1]*N2s[o1,2] - N2s[o1,1]*N1s[o1,2])
                ]).T
        O[o2] = np.array([
                -(d1s[o2]*N2s[o2,2]-d2s[o2]*N1s[o2,2])/(N1s[o2,0]*N2s[o2,2] - N2s[o2,0]*N1s[o2,2]),
                np.zeros(np.sum(o2)),
                -(d2s[o2]*N1s[o2,0]-d1s[o2]*N2s[o2,0])/(N1s[o2,0]*N2s[o2,2] - N2s[o2,0]*N1s[o2,2])
                ]).T
        O[o3] = np.array([
                -(d1s[o3]*N2s[o3,1]-d2s[o3]*N1s[o3,1])/(N1s[o3,0]*N2s[o3,1] - N2s[o3,0]*N1s[o3,1]),
                -(d2s[o3]*N1s[o3,0]-d1s[o3]*N2s[o3,0])/(N1s[o3,0]*N2s[o3,1] - N2s[o3,0]*N1s[o3,1]),
                np.zeros(np.sum(o3))
                ]).T
    
        # Projections of Tri1 to L
        Pv1s = np.array([np.sum(Ds*(Tri1s[:,i]-O),axis=1) for i in range(3)]).T
        # Projections of Tri2 to L
        Pv2s = np.array([np.sum(Ds*(Tri2s[:,i]-O),axis=1) for i in range(3)]).T

        t11s = np.zeros(len(Tri1s)); t12s = np.zeros(len(Tri1s))
        t21s = np.zeros(len(Tri1s)); t22s = np.zeros(len(Tri1s))
    
        a = (signs1[:,0] == signs1[:,2]) 
        b = (signs1[:,0] == signs1[:,1]) 
        c = (signs1[:,1] == signs1[:,2]) 

        A = ((signs1[:,1]!=0)) & ~(a|b|c)
        B = ((signs1[:,2]!=0)) & ~(a|b|c)
        C = ((signs1[:,0]!=0)) & ~(a|b|c)

        Aa = (A | a)
        Bb = (B | b) & ~Aa
        Cc = (C | c) & ~(Aa|Bb)
        
        t11s[Aa] = Pv1s[Aa,0] + (Pv1s[Aa,1]-Pv1s[Aa,0])*sd1s[Aa,0]/(sd1s[Aa,0]-sd1s[Aa,1])
        t12s[Aa] = Pv1s[Aa,2] + (Pv1s[Aa,1]-Pv1s[Aa,2])*sd1s[Aa,2]/(sd1s[Aa,2]-sd1s[Aa,1])
        
        t11s[Bb] = Pv1s[Bb,0] + (Pv1s[Bb,2]-Pv1s[Bb,0])*sd1s[Bb,0]/(sd1s[Bb,0]-sd1s[Bb,2])
        t12s[Bb] = Pv1s[Bb,1] + (Pv1s[Bb,2]-Pv1s[Bb,1])*sd1s[Bb,1]/(sd1s[Bb,1]-sd1s[Bb,2])
        
        t11s[Cc] = Pv1s[Cc,2] + (Pv1s[Cc,0]-Pv1s[Cc,2])*sd1s[Cc,2]/(sd1s[Cc,2]-sd1s[Cc,0])
        t12s[Cc] = Pv1s[Cc,1] + (Pv1s[Cc,0]-Pv1s[Cc,1])*sd1s[Cc,1]/(sd1s[Cc,1]-sd1s[Cc,0])
    
    
        a = (signs2[:,0] == signs2[:,2]) 
        b = (signs2[:,0] == signs2[:,1]) 
        c = (signs2[:,1] == signs2[:,2]) 

        A = ((signs2[:,1]!=0)) & ~(a|b|c)
        B = ((signs2[:,2]!=0)) & ~(a|b|c)
        C = ((signs2[:,0]!=0)) & ~(a|b|c)

        Aa = (A | a)
        Bb = (B | b) & ~Aa
        Cc = (C | c) & ~(Aa|Bb)

        t21s[Aa] = Pv2s[Aa,0] + (Pv2s[Aa,1]-Pv2s[Aa,0])*sd2s[Aa,0]/(sd2s[Aa,0]-sd2s[Aa,1])
        t22s[Aa] = Pv2s[Aa,2] + (Pv2s[Aa,1]-Pv2s[Aa,2])*sd2s[Aa,2]/(sd2s[Aa,2]-sd2s[Aa,1])
        
        t21s[Bb] = Pv2s[Bb,0] + (Pv2s[Bb,2]-Pv2s[Bb,0])*sd2s[Bb,0]/(sd2s[Bb,0]-sd2s[Bb,2])
        t22s[Bb] = Pv2s[Bb,1] + (Pv2s[Bb,2]-Pv2s[Bb,1])*sd2s[Bb,1]/(sd2s[Bb,1]-sd2s[Bb,2])
        
        t21s[Cc] = Pv2s[Cc,2] + (Pv2s[Cc,0]-Pv2s[Cc,2])*sd2s[Cc,2]/(sd2s[Cc,2]-sd2s[Cc,0])
        t22s[Cc] = Pv2s[Cc,1] + (Pv2s[Cc,0]-Pv2s[Cc,1])*sd2s[Cc,1]/(sd2s[Cc,1]-sd2s[Cc,0])
    
        t11s,t12s = np.fmin(t11s,t12s),np.fmax(t11s,t12s)
        t21s,t22s = np.fmin(t21s,t22s),np.fmax(t21s,t22s)
        
        # Initialize Intersections Array
        Intersections = np.repeat(True,len(Tri1s))
        
        # Perform Checks
        coplanar = np.all(np.abs(sd1s) < eps, axis=1)
        checks = (np.all(signs1==1,axis=1) | np.all(signs1==-1,axis=1) |
                 np.all(signs2==1,axis=1) | np.all(signs2==-1,axis=1) |
                 (t12s-t21s <= eps) | (t22s-t11s <= eps)) 
        if not edgeedge:
            edgeedgebool = (np.abs(t11s-t21s) < eps) & (np.abs(t12s-t22s) < eps)
            Intersections[checks | edgeedgebool | coplanar] = False
        else:
            Intersections[checks | coplanar] = False

        IntersectionPts = np.nan*np.ones((len(Intersections),18,3))
        # IntersectionPts = [[] for i in range(len(Intersections))]
        t1,t2 = np.sort([t11s,t12s,t21s,t22s],axis=0)[1:3]
        IntersectionPts[Intersections,0,:] = O[Intersections] + t1[Intersections,None]*Ds[Intersections]
        IntersectionPts[Intersections,1,:] = O[Intersections] + t2[Intersections,None]*Ds[Intersections]
        # Coplanar checks
        CoTri1s = Tri1s[coplanar]; CoTri2s = Tri2s[coplanar]
        edges = np.array([[0,1],[1,2],[2,0]])
        edges1idx = np.array([edges[0],edges[1],edges[2],edges[0],edges[1],edges[2],edges[0],edges[1],edges[2]])
        edges2idx = np.array([edges[0],edges[1],edges[2],edges[1],edges[2],edges[0],edges[2],edges[0],edges[1]])
        edges1 = CoTri1s[:,edges1idx]
        edges2 = CoTri2s[:,edges2idx]

        coplanar_where = np.where(coplanar)[0]

        ###
        edges1r = edges1.reshape(edges1.shape[0]*edges1.shape[1],edges1.shape[2],edges1.shape[3])
        edges2r = edges2.reshape(edges2.shape[0]*edges2.shape[1],edges2.shape[2],edges2.shape[3])
        intersectionsr,ptsr = SegmentsSegmentsIntersection(edges1r,edges2r,return_intersection=True,eps=eps)
        
        intersections = intersectionsr.reshape(edges1.shape[0],edges1.shape[1])
        pts = ptsr.reshape(edges1.shape[0],edges1.shape[1],ptsr.shape[1])

        ###
        edge1_ix = [[],[],[]]; edge1_ixpts = [[],[],[]]; edge1_ixcount = [[],[],[]]
        edge1_ix[0] = intersections[:,0::3]
        edge1_ix[1] = intersections[:,1::3]
        edge1_ix[2] = intersections[:,2::3]
        edge1_ixpts[0] = pts[:,0::3]#[edge1_ix[0]]
        edge1_ixpts[1] = pts[:,1::3]#[edge1_ix[1]]
        edge1_ixpts[2] = pts[:,2::3]#[edge1_ix[2]]
        edge1_ixcount[0] = np.sum(edge1_ix[0],axis=1)
        edge1_ixcount[1] = np.sum(edge1_ix[1],axis=1)
        edge1_ixcount[2] = np.sum(edge1_ix[2],axis=1)

        edge2_ix = [[],[],[]]; edge2_ixpts = [[],[],[]]; edge2_ixcount = [[],[],[]]
        edge2_ix[0] = intersections[:,[0,5,7]]
        edge2_ix[1] = intersections[:,[1,3,8]]
        edge2_ix[2] = intersections[:,[2,4,6]]
        edge2_ixpts[0] = pts[:,[0,5,7]]#[edge2_ix[0]]
        edge2_ixpts[1] = pts[:,[1,3,8]]#[edge2_ix[1]]
        edge2_ixpts[2] = pts[:,[2,4,6]]#[edge2_ix[2]]
        edge2_ixcount[0] = np.sum(edge2_ix[0],axis=1)
        edge2_ixcount[1] = np.sum(edge2_ix[1],axis=1)
        edge2_ixcount[2] = np.sum(edge2_ix[2],axis=1)

        # For edges that only interesect at one point, they way have a point inside the other triangle that needs to be accounted for
        for i in range(len(edge1_ixcount)):
            where1 = np.where(edge1_ixcount[i]==1)[0]
            es1 = edges1[where1][:,i]    # list of the first edges
            p11s = es1[:,0]   # First point in the edges
            p12s = es1[:,1]   # Second point in the edges
            tris1 = Tri2s[coplanar_where[where1]]    # Corresponding triangle
            In11 = PointsInTris(tris1,p11s,method='BaryArea') & (~np.any(np.all(np.abs(p11s[:,:,None] - edge1_ixpts[i][where1])<eps,axis=2),axis=1))
            In12 = PointsInTris(tris1,p12s,method='BaryArea') & (~np.any(np.all(np.abs(p12s[:,:,None] - edge1_ixpts[i][where1])<eps,axis=2),axis=1))

            nanidx1 = np.where(np.all(np.isnan(edge1_ixpts[i][where1]),axis=2).cumsum(axis=1).cumsum(axis=1) == 1)
            edge1_ixpts[i][where1[nanidx1[0][In11]],nanidx1[1][In11]] = p11s[In11]
            edge1_ixpts[i][where1[nanidx1[0][In12&~In11]],nanidx1[1][In12&~In11]] = p12s[In12&~In11]
            edge1_ixpts[i][where1[nanidx1[0][~In12&~In11]],nanidx1[1][~In12&~In11]] = edge1_ixpts[i][where1[~In12&~In11]][np.where(np.all(~np.isnan(edge1_ixpts[i][where1[~In12&~In11]]),axis=2).cumsum(axis=1).cumsum(axis=1) == 1)]
            #
            where2 = np.where(edge2_ixcount[i]==1)[0]
            es2 = edges2[where2][:,i]    # list of the first edges
            p21s = es2[:,0]   # First point in the edges
            p22s = es2[:,1]   # Second point in the edges
            tris2 = Tri1s[coplanar_where[where2]]    # Corresponding triangle
            In21 = PointsInTris(tris2,p21s,method='BaryArea') & (~np.any(np.all(np.abs(p21s[:,:,None] - edge2_ixpts[i][where2])<eps,axis=2),axis=1))
            In22 = PointsInTris(tris2,p22s,method='BaryArea') & (~np.any(np.all(np.abs(p22s[:,:,None] - edge2_ixpts[i][where2])<eps,axis=2),axis=1))

            nanidx2 = np.where(np.all(np.isnan(edge2_ixpts[i][where2]),axis=2).cumsum(axis=1).cumsum(axis=1) == 1)
            edge2_ixpts[i][where2[nanidx2[0][In21]],nanidx2[1][In21]] = p21s[In21]
            edge2_ixpts[i][where2[nanidx2[0][In22&~In21]],nanidx2[1][In22&~In21]] = p22s[In22&~In21]
            edge2_ixpts[i][where2[nanidx2[0][~In22&~In21]],nanidx2[1][~In22&~In21]] = edge2_ixpts[i][where2[~In22&~In21]][np.where(np.all(~np.isnan(edge2_ixpts[i][where2[~In22&~In21]]),axis=2).cumsum(axis=1).cumsum(axis=1) == 1)]


        # Collect the points so that the intersection edges 
        Edge1Stack = np.concatenate([edge1_ixpts[0],edge1_ixpts[1],edge1_ixpts[2]],axis=1)
        Edge2Stack = np.concatenate([edge2_ixpts[0],edge2_ixpts[1],edge2_ixpts[2]],axis=1)
        DoubleStack = np.concatenate([Edge1Stack,Edge2Stack],axis=1)

        NewDoubleStack = np.nan*np.ones(DoubleStack.shape)
        NewDoubleStack[np.flip(np.sort(np.all(~np.isnan(DoubleStack),axis=2),axis=1),axis=1)] = DoubleStack[np.all(~np.isnan(DoubleStack),axis=2)]

        Intersections[coplanar_where] = np.any(intersections,axis=1)
        IntersectionPts[coplanar_where] = NewDoubleStack

        # Check triangles with no edge intersections to see if one is completely within the other
        PtInTriChecks = coplanar_where[~Intersections[coplanar_where]]
        TwoInOne = PointsInTris(Tri1s[PtInTriChecks],Tri2s[PtInTriChecks,0],method='BaryArea',eps=eps,inclusive=False)
        OneInTwo = PointsInTris(Tri2s[PtInTriChecks],Tri1s[PtInTriChecks,0],method='BaryArea',eps=eps,inclusive=False)

        Intersections[PtInTriChecks] = OneInTwo | TwoInOne
        IntersectionPts[PtInTriChecks[TwoInOne],:6,:] = Tri2s[PtInTriChecks[TwoInOne]][:,[0,1,1,2,2,0]]
        IntersectionPts[PtInTriChecks[OneInTwo],:6,:] = Tri1s[PtInTriChecks[OneInTwo]][:,[0,1,1,2,2,0]]


    return Intersections, IntersectionPts

def TriangleBoxIntersection(TriCoords, xlim, ylim, zlim, TriNormal=None, BoxCenter=None):
    """
    Intersection test for detecting intersections between a triangle and a box.

    Akenine-Möller, T. (2005). Fast 3D triangle-box overlap testing. ACM SIGGRAPH 2005 Courses, SIGGRAPH 2005. https://doi.org/10.1145/1198555.1198747
    :cite:p:`Akenine-Moller2005`

    Parameters
    ----------
    TriCoords : array_like
        Coordinates of the three vertices of the triangle in the format
        ``np.array([[a, b, c], [d, e, f], [g, h, i]])``
    xlim : array_like
        2 element array of the lower and upper bounds of the box in the x direction ``[xmin, xmax]``
    ylim : array_like
        2 element array of the lower and upper bounds of the box in the y direction ``[ymin, ymax]``
    zlim : array_like
        2 element array of the lower and upper bounds of the box in the z direction ``[zmin, zmax]``
    TriNormal : array_like, optional
        Triangle normal vector, by default None. Will be computed if not provided.
    BoxCenter : array_like, optional
        Coordinates of the center of the box, by default None. Will be computed if not provided.

    Returns
    -------
    intersection : bool
        True if there is an intersection, otherwise False.
    """    
    # Akenine-Moller (2001) Fast 3D Triangle-Box Overlap Test
    if BoxCenter is None: BoxCenter = np.mean([xlim,ylim,zlim],axis=1)
    f0 = np.subtract(TriCoords[1],TriCoords[0])
    f1 = np.subtract(TriCoords[2],TriCoords[1])
    f2 = np.subtract(TriCoords[0],TriCoords[2])
    hx = (xlim[1]-xlim[0])/2
    hy = (ylim[1]-ylim[0])/2
    hz = (zlim[1]-zlim[0])/2
    # Move triangle so that the box is centered around the origin 
    [v0,v1,v2] = np.subtract(TriCoords,BoxCenter)
    
    # Test the box against the minimal Axis Aligned Bounding Box (AABB) of the tri
    if max(v0[0],v1[0],v2[0]) < -hx or min(v0[0],v1[0],v2[0]) > hx:
        return False
    if max(v0[1],v1[1],v2[1]) < -hy or min(v0[1],v1[1],v2[1]) > hy:
        return False
    if max(v0[2],v1[2],v2[2]) < -hz or min(v0[2],v1[2],v2[2]) > hz:
        return False
    
    # Test the normal of the triangle
    if TriNormal is None: 
        TriNormal = np.cross(f0,f1)
    elif type(TriNormal) is list:
        TriNormal = np.array(TriNormal)
    dist = np.dot(TriNormal,v0)
    r = hx*np.abs(TriNormal[0]) + hy*np.abs(TriNormal[1]) + hz*np.abs(TriNormal[2])
    if dist > r:
        return False
    
    # Test Axes
    # a00
    a00 = np.array([0,-f0[2],f0[1]])
    p0 = np.dot(v0,a00)
    # p1 = np.dot(v1,a00)
    p2 = np.dot(v2,a00)
    r = hy*np.abs(a00[1]) + hz*np.abs(a00[2])
    if min(p0,p2) > r or max(p0,p2) < -r:
        return False
    # a01
    a01 = np.array([0,-f1[2],f1[1]])
    p0 = np.dot(v0,a01)
    p1 = np.dot(v1,a01)
    # p2 = np.dot(v2,a01)
    r = hy*np.abs(a01[1]) + hz*np.abs(a01[2])
    if min(p0,p1) > r or max(p0,p1) < -r:
        return False
    # a02
    a02 = np.array([0,-f2[2],f2[1]])
    p0 = np.dot(v0,a02)
    p1 = np.dot(v1,a02)
    # p2 = np.dot(v2,a02)
    r = hy*np.abs(a02[1]) + hz*np.abs(a02[2])
    if min(p0,p1) > r or max(p0,p1) < -r:
        return False
    # a10
    a10 = np.array([f0[2],0,-f0[0]])
    p0 = np.dot(v0,a10)
    # p1 = np.dot(v1,a10)
    p2 = np.dot(v2,a10)
    r = hx*np.abs(a10[0]) + hz*np.abs(a10[2])
    if min(p0,p2) > r or max(p0,p2) < -r:
        return False
    # a11
    a11 = np.array([f1[2],0,-f1[0]])
    p0 = np.dot(v0,a11)
    p1 = np.dot(v1,a11)
    # p2 = np.dot(v2,a11)
    r = hx*np.abs(a11[0]) + hz*np.abs(a11[2])
    if min(p0,p1) > r or max(p0,p1) < -r:
        return False
    # a12
    a12 = np.array([f2[2],0,-f2[0]])
    p0 = np.dot(v0,a12)
    p1 = np.dot(v1,a12)
    # p2 = np.dot(v2,a10)
    r = hx*np.abs(a12[0]) + hz*np.abs(a12[2])
    if min(p0,p1) > r or max(p0,p1) < -r:
        return False
    # a20
    a20 = np.array([-f0[1],f0[0],0])
    p0 = np.dot(v0,a20)
    # p1 = np.dot(v1,a20)
    p2 = np.dot(v2,a20)
    r = hx*np.abs(a20[0]) + hy*np.abs(a20[1])
    if min(p0,p2) > r or max(p0,p2) < -r:
        return False
    # a21
    a21 = np.array([-f1[1],f1[0],0])
    p0 = np.dot(v0,a21)
    p1 = np.dot(v1,a21)
    # p2 = np.dot(v2,a21)
    r = hx*np.abs(a21[0]) + hy*np.abs(a21[1])
    if min(p0,p1) > r or max(p0,p1) < -r:
        return False
    # a22
    a22 = np.array([-f2[1],f2[0],0])
    p0 = np.dot(v0,a22)
    p1 = np.dot(v1,a22)
    # p2 = np.dot(v2,a22)
    r = hx*np.abs(a22[0]) + hy*np.abs(a22[1])
    if min(p0,p1) > r or max(p0,p1) < -r:
        return False
    
    return True

def BoxTrianglesIntersection(Tris, xlim, ylim, zlim, TriNormals=None, BoxCenter=None):
    """
    Intersection test for detecting intersections between a triangle and a box. A vectorized version of :func:`TriangleBoxIntersection` for one box and multiple triangles

    Akenine-Möller, T. (2005). Fast 3D triangle-box overlap testing. ACM SIGGRAPH 2005 Courses, SIGGRAPH 2005. https://doi.org/10.1145/1198555.1198747
    :cite:p:`Akenine-Moller2005`

    Parameters
    ----------
    Tris : array_like
        Coordinates of triangle vertices for each triangle in the format
        np.array([[[a, b, c], [d, e, f], [g, h, i]], [[...],[...],[...]], ...).
        Should have shape (n,3,3) for n triangles.
    xlim : array_like
        2 element array of the lower and upper bounds of the box in the x direction ``[xmin, xmax]``
    ylim : array_like
        2 element array of the lower and upper bounds of the box in the y direction ``[ymin, ymax]``
    zlim : array_like
        2 element array of the lower and upper bounds of the box in the z direction ``[zmin, zmax]``
    TriNormal : array_like, optional
        Triangle normal vector, by default None. Will be computed if not provided.
    BoxCenter : array_like, optional
        Coordinates of the center of the box, by default None. Will be computed if not provided.

    Returns
    -------
    intersection : bool
        True if there is an intersection, otherwise False.
    """    
    if BoxCenter is None: BoxCenter = np.mean([xlim,ylim,zlim],axis=1)
    
    if type(Tris) is list: Tris = np.array(Tris)
        
    f0 = Tris[:,1]-Tris[:,0]
    f1 = Tris[:,2]-Tris[:,1]
    f2 = Tris[:,0]-Tris[:,2]
    hx = (xlim[1]-xlim[0])/2
    hy = (ylim[1]-ylim[0])/2
    hz = (zlim[1]-zlim[0])/2
    
    # Move triangles so that the box is centered around the origin 
    diff = Tris - BoxCenter
    v0 = diff[:,0]; v1 = diff[:,1]; v2 = diff[:,2]
    
    if TriNormals is None: 
        TriNormals = np.cross(f0,f1)
    elif type(TriNormals) is list:
        TriNormals = np.array(TriNormals)
    
    dist = np.sum(TriNormals*v0,axis=1)
    r0 = hx*np.abs(TriNormals[:,0]) + hy*np.abs(TriNormals[:,1]) + hz*np.abs(TriNormals[:,2])
    
    # Test Axes
    # a00
    a00 = np.vstack([np.zeros(len(f0)), -f0[:,2], f0[:,1]]).T
    p0 = np.sum(v0*a00,axis=1)
    p2 = np.sum(v2*a00,axis=1)
    r1 = hy*np.abs(a00[:,1]) + hz*np.abs(a00[:,2])
    ps1 = (p0,p2)
    
    # a01
    a01 = np.vstack([np.zeros(len(f1)), -f1[:,2], f1[:,1]]).T
    p0 = np.sum(v0*a01,axis=1)
    p1 = np.sum(v1*a01,axis=1)
    r2 = hy*np.abs(a01[:,1]) + hz*np.abs(a01[:,2])
    ps2 = (p0,p1)
    
    # a02
    a02 = np.vstack([np.zeros(len(f2)), -f2[:,2], f2[:,1]]).T
    p0 = np.sum(v0*a02,axis=1)
    p1 = np.sum(v1*a02,axis=1)
    r3 = hy*np.abs(a02[:,1]) + hz*np.abs(a02[:,2])
    ps3 = (p0,p1)
    
    # a10
    a10 = np.vstack([f0[:,2], np.zeros(len(f0)), -f0[:,0]]).T
    p0 = np.sum(v0*a10,axis=1)
    p2 = np.sum(v2*a10,axis=1)
    r4 = hx*np.abs(a10[:,0]) + hz*np.abs(a10[:,2])
    ps4 = (p0,p2)
    
    # a11
    a11 = np.vstack([f1[:,2], np.zeros(len(f1)), -f1[:,0]]).T
    p0 = np.sum(v0*a11,axis=1)
    p1 = np.sum(v1*a11,axis=1)
    r5 = hx*np.abs(a11[:,0]) + hz*np.abs(a11[:,2])
    ps5 = (p0,p1)
    
    # a12
    a12 = np.vstack([f2[:,2], np.zeros(len(f2)), -f2[:,0]]).T
    p0 = np.sum(v0*a12,axis=1)
    p1 = np.sum(v1*a12,axis=1)
    r6 = hx*np.abs(a12[:,0]) + hz*np.abs(a12[:,2])
    ps6 = (p0,p1)
    # a20
    a20 = np.vstack([-f0[:,1], f0[:,0], np.zeros(len(f0))]).T
    p0 = np.sum(v0*a20,axis=1)
    p2 = np.sum(v2*a20,axis=1)
    r7 = hx*np.abs(a20[:,0]) + hy*np.abs(a20[:,1])
    ps7 = (p0,p2)
    
    # a21
    a21 = np.vstack([-f1[:,1], f1[:,0], np.zeros(len(f1))]).T
    p0 = np.sum(v0*a21,axis=1)
    p1 = np.sum(v1*a21,axis=1)
    r8 = hx*np.abs(a21[:,0]) + hy*np.abs(a21[:,1])
    ps8 = (p0,p1)
    
    # a22
    a22 = np.vstack([-f2[:,1], f2[:,0], np.zeros(len(f2))]).T
    p0 = np.sum(v0*a22,axis=1)
    p1 = np.sum(v1*a22,axis=1)
    r9 = hx*np.abs(a22[:,0]) + hy*np.abs(a22[:,1])
    ps9 = (p0,p1)
    
    
    Intersections = np.repeat(True,len(Tris))
    
    checks = (
        # Test the box against the minimal Axis Aligned Bounding Box (AABB) of the tri
        (np.amax([v0[:,0],v1[:,0],v2[:,0]],axis=0) < -hx) | 
        (np.amin([v0[:,0],v1[:,0],v2[:,0]],axis=0) >  hx) |
        (np.amax([v0[:,1],v1[:,1],v2[:,1]],axis=0) < -hy) | 
        (np.amin([v0[:,1],v1[:,1],v2[:,1]],axis=0) >  hy) |
        (np.amax([v0[:,2],v1[:,2],v2[:,2]],axis=0) < -hz) | 
        (np.amin([v0[:,2],v1[:,2],v2[:,2]],axis=0) >  hz) |
        # Test normal of the triangle
        (dist > r0) |
        # Test Axes
        (np.minimum(*ps1) > r1) | (np.maximum(*ps1) < -r1) |
        (np.minimum(*ps2) > r2) | (np.maximum(*ps2) < -r2) |
        (np.minimum(*ps3) > r3) | (np.maximum(*ps3) < -r3) |
        (np.minimum(*ps4) > r4) | (np.maximum(*ps4) < -r4) |
        (np.minimum(*ps5) > r5) | (np.maximum(*ps5) < -r5) |
        (np.minimum(*ps6) > r6) | (np.maximum(*ps6) < -r6) |
        (np.minimum(*ps7) > r7) | (np.maximum(*ps7) < -r7) |
        (np.minimum(*ps8) > r8) | (np.maximum(*ps8) < -r8) |
        (np.minimum(*ps9) > r9) | (np.maximum(*ps9) < -r9)
        )
    
    
    Intersections[checks] = False
    return Intersections

@try_njit    
def BoxBoxIntersection(box1, box2):

    x1lim, y1lim, z1lim = box1
    x2lim, y2lim, z2lim = box2

    xIx = ((x1lim[0] < x2lim[0]) and (x1lim[1] > x2lim[0])) or ((x1lim[0] < x2lim[1]) and (x1lim[1] > x2lim[1])) or ((x2lim[0] < x1lim[0]) and (x2lim[1] > x1lim[0])) or ((x2lim[0] < x1lim[1]) and (x2lim[1] > x1lim[1]))
    yIx = ((y1lim[0] < y2lim[0]) and (y1lim[1] > y2lim[0])) or ((y1lim[0] < y2lim[1]) and (y1lim[1] > y2lim[1])) or ((y2lim[0] < y1lim[0]) and (y2lim[1] > y1lim[0])) or ((y2lim[0] < y1lim[1]) and (y2lim[1] > y1lim[1]))
    zIx = ((z1lim[0] < z2lim[0]) and (z1lim[1] > z2lim[0])) or ((z1lim[0] < z2lim[1]) and (z1lim[1] > z2lim[1])) or ((z2lim[0] < z1lim[0]) and (z2lim[1] > z1lim[0])) or ((z2lim[0] < z1lim[1]) and (z2lim[1] > z1lim[1]))

    Ix = xIx and yIx and zIx

    return Ix

def SegmentSegmentIntersection(s1,s2,return_intersection=False,endpt_inclusive=True,eps=0):
    # https://mathworld.wolfram.com/Line-LineIntersection.html
    # Goldman (1990)
    [p1,p2] = np.array(s1)
    [p3,p4] = np.array(s2)
    
    a = p2-p1; b = p4-p3; c = p3-p1
    axb = np.cross(a,b)
    axbnorm2 = (np.linalg.norm(axb))**2
    s = np.dot(np.cross(c,b),axb)/axbnorm2
    t = np.dot(np.cross(c,a),axb)/axbnorm2
    
    if endpt_inclusive:
        Intersection = (0 <= s <= 1) and (0 <= t <= 1) & (axbnorm2 > eps)
    else:
        Intersection = (0+eps < s < 1-eps) and (0+eps < t < 1-eps) & (axbnorm2 > eps)

    if return_intersection:
        pt = p1 + a*s
        return Intersection, pt

    return Intersection

def SegmentsSegmentsIntersection(s1,s2,return_intersection=False,endpt_inclusive=True,eps=0):
    # https://mathworld.wolfram.com/Line-LineIntersection.html
    # Goldman (1990)
    if type(s1) is list: s1 = np.array(s1)
    if type(s2) is list: s2 = np.array(s2)
    p1 = s1[:,0]; p2 = s1[:,1]
    p3 = s2[:,0]; p4 = s2[:,1]
    
    a = p2-p1; b = p4-p3; c = p3-p1
    axb = np.cross(a,b,axis=1)
    cxb = np.cross(c,b,axis=1)
    cxa = np.cross(c,a,axis=1)
    axbnorm2 = np.sum(axb**2,axis=1) #+ 1e-32
    with np.errstate(divide='ignore', invalid='ignore'):
        s = np.sum(cxb*axb,axis=1)/axbnorm2
        t = np.sum(cxa*axb,axis=1)/axbnorm2
    # Collinear: Currently not getting intersection points for perfectly collinear lines
    if endpt_inclusive:
        Intersections = (0-eps <= s) & (s <= 1+eps) & (0-eps <= t) & (t <= 1+eps) & (axbnorm2 > eps**2) ## DON'T GET RID OF THE LAST CHECK
        # Intersections = (0 <= s) & (s <= 1) & (0 <= t) & (t <= 1) & (axbnorm2 > eps**2)
        ###

        # Collinear = (axbnorm2 <= eps**2)
        # np.linalg.norm(axb/(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1))[:,None],axis=1)
        
    else:
        Intersections = (0+eps < s) & (s < 1-eps) & (0+eps < t) & (t < 1-eps) & (axbnorm2 > eps**2)
    if return_intersection:
        ### Without collinear:
        pts = np.nan*np.ones((len(Intersections),3))
        pts[Intersections] = p1[Intersections] + a[Intersections]*s[Intersections,None]
        ###

        ### With collinear: (TBD)
        # pts = np.nan*np.ones((len(Intersections),2,3))
        ###
        return Intersections, pts
    return Intersections

def SegmentsSegmentsIntersection2(s1,s2,return_intersection=False,endpt_inclusive=True,eps=1e-14):
    # https://mathworld.wolfram.com/Line-LineIntersection.html
    # Goldman (1990)
    if type(s1) is list: s1 = np.array(s1)
    if type(s2) is list: s2 = np.array(s2)
    
    x1,x2 = s1[:,0],s1[:,1]
    x3,x4 = s2[:,0],s2[:,1]
    p1 = x1; V1 = x2-x1
    p2 = x3; V2 = x4-x3
    V1xV2 = np.cross(V1,V2,axis=1)
    denom = np.linalg.norm(V1xV2,axis=1)**2

    t = np.linalg.det(np.array([p2-p1,V2,V1xV2]).swapaxes(0,1))/denom
    s = np.linalg.det(np.array([p2-p1,V1,V1xV2]).swapaxes(0,1))/denom
    s = np.clip(s,0,1)
    t = np.clip(t,0,1)
    
    x1 = p1+V1*t[:,None]
    x2 = p2+V2*s[:,None]
    # print((np.linalg.norm(x1-s1[:,0],axis=1)))
    # print((np.linalg.norm(x1-s1[:,1],axis=1)))
    if endpt_inclusive:
        Intersections = (np.linalg.norm(x2-x1,axis=1) == 0)
    else:
        Intersections = (np.linalg.norm(x2-x1,axis=1) == 0) & ~((np.linalg.norm(x1-s1[:,0],axis=1) <= eps) | (np.linalg.norm(x1-s1[:,1],axis=1) <= eps))
    if return_intersection:
        pts = np.nan*np.ones((len(Intersections),3))
        pts[Intersections] = x1[Intersections]
        return Intersections, pts
    return Intersections

def RaySegmentsIntersection(pt, ray, segments, return_intersection=False, eps=1e-14):
    if type(segments) is list: segments = np.array(segments)
    
    x1,x2 = segments[:,0],segments[:,1]
    p1 = x1; V1 = x2-x1
    p2 = pt; V2 = ray
    V1xV2 = np.cross(V1,V2)
    denom = np.linalg.norm(V1xV2,axis=1)**2

    t = np.linalg.det(np.array([p2-p1,np.repeat([V2],len(V1),axis=0),V1xV2]).swapaxes(0,1))/denom
    s = np.linalg.det(np.array([p2-p1,V1,V1xV2]).swapaxes(0,1))/denom
    
    x1 = p1+V1*t[:,None]
    x2 = p2+V2*s[:,None]

    Intersections = (t <= 0) & (s <= 1) & (s >= 0)
    if return_intersection:
        pts = np.nan*np.ones((len(Intersections),3))
        pts[Intersections] = x1[Intersections]
        return Intersections, pts
    return Intersections
    
def RaySurfIntersection(pt, ray, NodeCoords, SurfConn, eps=1e-14, Octree='generate'):
    """
    Identify intersections between a ray and a triangular surface mesh. 

    Parameters
    ----------
    pt : array_like
        3D point coordinate (shape = (3,))
    ray : array_like
        3D vector (shape = (3,))
    NodeCoords : array_like
        nx3 list of node coordinates
    SurfConn : array_like
        List of surface element connectivities. This should be a strictly
        triangular mesh. See :func:`~mymesh.converter.surf2tris` for conversion.
    eps : float, optional
        Small tolerance parameter, by default 1e-14
    Octree : str, octree.OctreeNode, or NoneType, optional
        Specify whether to use an octree structure for acceleration of 
        intersection tests. An octree previously constructed using 
        :func:`~mymesh.octree.Surface2Octree` can be used, or one can be
        generated by default 'generate'.

        - 'generate' : Create an octree
        - 'None' or None : Don't use an octree
        - octree.OctreeNode : Use this octree

    Returns
    -------
    intersections : np.ndarray
        Indices of triangles that are intersected by ray.
    distances : np.ndarray
        Distances between the point and the intersection point.
    intersectionPts : np.ndarray
        Coordinates of intersection points for each intersection.
    
    
    """    
    def test(pt, ray, nodes):
        iPt = RayTriangleIntersection(pt, ray, nodes, bidirectional=True)
        return iPt
    ArrayCoords = np.array(NodeCoords)
    if type(pt) is list: pt = np.array(pt)
    if type(ray) is list: ray = np.array(ray)
    if Octree == None or Octree == 'None' or Octree == 'none':
        # Won't use any octree structure to accelerate intersection tests
        intersections,intersectionPts = RayTrianglesIntersection(pt, ray, ArrayCoords[SurfConn], bidirectional=True, eps=eps)
        distances = np.sum(ray*(intersectionPts-pt),axis=1)
    elif Octree == 'generate' or type(Octree) == octree.OctreeNode:
        if Octree == 'generate':
            # Create an octree structure based on the provided structure
            root = octree.Surface2Octree(NodeCoords,SurfConn)
        else:
            # Using an already generated octree structure
            # If this is the case, it should conform to the same structure and labeling as one generated with octree.Surface2Octree
            root = Octree
            
        # Proceeding with octree-accelerated intersection test
        intersection_leaves = RayOctreeIntersection(pt, ray, root) 
        TriIds = [tri for node in intersection_leaves for tri in node.data]
        
        Tris = ArrayCoords[np.asarray(SurfConn)[TriIds]]
        intersections,intersectionPts = RayTrianglesIntersection(pt, ray, Tris, bidirectional=True, eps=eps)
        intersections = np.array(TriIds)[intersections]
        distances = np.sum(ray*(intersectionPts-pt),axis=1)
    else:
        raise Exception('Invalid octree argument given')
        
    return intersections, distances, intersectionPts

def RaysSurfIntersection(pts, rays, NodeCoords, SurfConn, bidirectional=True, eps=1e-14, Octree='generate'):
    """
    Identify intersections between rays and a triangular surface mesh. 

    Parameters
    ----------
    pts : array_like
        3D point coordinates (shape = (m,3))
    ray : array_like
        3D vectors (shape = (m,3))
    NodeCoords : array_like
        nx3 list of node coordinates
    SurfConn : array_like
        List of surface element connectivities. This should be a strictly
        triangular mesh. See :func:`~mymesh.converter.surf2tris` for conversion.
    bidirectional : bool
        Determines whether to check for intersections only in the direction the 
        ray is pointing, or in both directions (±ray), by default False.
    eps : float, optional
        Small tolerance parameter, by default 1e-14
    Octree : str, octree.OctreeNode, or NoneType, optional
        Specify whether to use an octree structure for acceleration of 
        intersection tests. An octree previously constructed using 
        :func:`~mymesh.octree.Surface2Octree` can be used, or one can be
        generated by default 'generate'.

        - 'generate' : Create an octree
        - 'None' or None : Don't use an octree
        - octree.OctreeNode : Use this octree

    Returns
    -------
    intersections : np.ndarray
        Indices of triangles that are intersected by ray.
    distances : np.ndarray
        Distances between the point and the intersection point.
    intersectionPts : np.ndarray
        Coordinates of intersection points for each intersection.
    
    
    """ 
    ArrayCoords = np.array(NodeCoords)
    if type(pts) is list: pts = np.array(pts)
    if type(rays) is list: rays = np.array(rays)
    if Octree == None or Octree == 'None' or Octree == 'none':
        # Won't use any octree structure to accelerate intersection tests
        inpts = np.repeat(pts,len(SurfConn),axis=0)
        inrays = np.repeat(rays,len(SurfConn),axis=0)
        RayIds = np.repeat(np.arange(len(rays),dtype=int),len(SurfConn),axis=0)

        Tris = np.tile(ArrayCoords[SurfConn], (len(pts),1,1))
        TriIds = np.tile(np.arange(len(SurfConn),dtype=int), len(pts))
        
        outintersections,outintersectionPts = RaysTrianglesIntersection(inpts, inrays, Tris, bidirectional=bidirectional, eps=eps)
        outdistances = np.sum(inrays[outintersections]*(outintersectionPts-inpts[outintersections]),axis=1)

    elif Octree == 'generate' or type(Octree) == octree.OctreeNode:
        if Octree == 'generate':
            # Create an octree structure based on the provided structure
            root = octree.Surface2Octree(NodeCoords,SurfConn)
        else:
            # Using an already generated octree structure
            # If this is the case, it should conform to the same structure and labeling as one generated with octree.Surface2Octree
            root = Octree
        # Proceeding with octree-accelerated intersection test
        # Assemble pairwise list of rays and tris
        TriIds = [[] for i in range(len(pts))]
        RayIds = [[] for i in range(len(pts))]
        for i in range(len(rays)):
            intersection_leaves = RayOctreeIntersection(pts[i], rays[i], root) 
            iTris = [tri for node in intersection_leaves for tri in node.data]
            TriIds[i] = iTris
            RayIds[i] = np.repeat(i,len(iTris))
        TriIds = np.array([x for y in TriIds for x in y]) # flattening
        RayIds = np.array([x for y in RayIds for x in y]) # flattening
        
        if len(TriIds) == 0:
            # No intersections with the octree
            intersections = [np.array([],dtype=np.int32) for i in range(len(rays))]
            distances = [np.array([],dtype=np.float64) for i in range(len(rays))]
            intersectionPts = [np.empty((0,3)) for i in range(len(rays))]

            return intersections, distances, intersectionPts

        Tris = ArrayCoords[np.asarray(SurfConn)[TriIds]]
        inpts = pts[RayIds]
        inrays = rays[RayIds]
        outintersections,outintersectionPts = RaysTrianglesIntersection(inpts, inrays, Tris, bidirectional=bidirectional, eps=eps)
        outdistances = np.sum(inrays[outintersections]*(outintersectionPts-inpts[outintersections]),axis=1)

    else:
        raise Exception('Invalid octree argument given')
        
    spintersections = scipy.sparse.lil_matrix((len(pts),len(SurfConn)),dtype=int)
    spdistances = scipy.sparse.lil_matrix((len(pts),len(SurfConn)))
    spintersectionPtsX = scipy.sparse.lil_matrix((len(pts),len(SurfConn)))
    spintersectionPtsY = scipy.sparse.lil_matrix((len(pts),len(SurfConn)))
    spintersectionPtsZ = scipy.sparse.lil_matrix((len(pts),len(SurfConn)))

    spintersections[RayIds[outintersections],TriIds[outintersections]] = TriIds[outintersections]+1 # +1 so that TriId = 0 doesn't get lost in sparse
    spdistances[RayIds[outintersections],TriIds[outintersections]] = outdistances+1e-32
    spintersectionPtsX[RayIds[outintersections],TriIds[outintersections]] = outintersectionPts[:,0]+1e-32
    spintersectionPtsY[RayIds[outintersections],TriIds[outintersections]] = outintersectionPts[:,1]+1e-32
    spintersectionPtsZ[RayIds[outintersections],TriIds[outintersections]] = outintersectionPts[:,2]+1e-32

    intersections = [x.toarray()[x.nonzero()]-1 for x in spintersections.tocsr()]
    distances = [(x.toarray()[x.nonzero()]-1e-32) for x in spdistances.tocsr()]        
    intersectionPts = [np.vstack([x.toarray()[x.nonzero()],y.toarray()[y.nonzero()],z.toarray()[z.nonzero()]]).T-1e-32 for x,y,z in zip(spintersectionPtsX.tocsr(),spintersectionPtsY.tocsr(),spintersectionPtsZ.tocsr())]

    return intersections, distances, intersectionPts

def RayOctreeIntersection(pt, ray, Octree):
    """
    Test for identifying intersections between a ray and an octree.

    Parameters
    ----------
    pt : array_like
        3D point coordinate (shape = (3,))
    ray : array_like
        3D vector (shape = (3,))
    Octree : octree.OctreeNode
        Root node of the octree data structure

    Returns
    -------
    intersection_leaves : list
        List of octree leaf nodes that the ray intersects.
    """
    root = Octree
    [xlim,ylim,zlim] = root.getLimits()
    intersection_leaves = []
    if not RayBoxIntersection(pt, ray, xlim, ylim, zlim):
        return intersection_leaves
    elif root.state == 'leaf':
        intersection_leaves.append(root)
        return intersection_leaves

    children = np.array(root.children,dtype=object)
    while len(children) > 0:
        limits = np.array([node.getLimits() for node in children])
        xlims = limits[:,0,:]
        ylims = limits[:,1,:]
        zlims = limits[:,2,:]

        intersections = RayBoxesIntersection(pt, ray, xlims, ylims, zlims)

        nodes = children[intersections]
        intersection_leaves += [node for node in nodes if node.state == 'leaf']

        children = np.array([child for parent in nodes for child in parent.children], dtype=object)

    return intersection_leaves

def SurfSelfIntersection(NodeCoords, SurfConn, Octree='generate', eps=1e-14, return_pts=False):
    """
    Identify self intersections in a mesh

    Parameters
    ----------
    NodeCoords : array_like
        Node coordinates
    SurfConn : array_like
        Node connectivity of a triangular surface mesh
    Octree : str, octree.OctreeNode, optional
        Octree node (generated by octree.Surf2Octree), 'generate',
        or None, by default 'generate'. 
    eps : float, optional
        Small tolerance parameter, by default 1e-14
    return_pts : bool, optional
        If true, return the coordinates of intersections, by default False

    Returns
    -------
    IntersectionPairs : np.ndarray
        Array of indices indicating pairs of elements that interesect each other
    IntersectionPoints : np.ndarray, optional
        Coordinates of intersections, returned if return_pts=True.
        Intersection points are given for each intersection pair in a 3d (n,m,3)
        array where n = len(IntersectionPairs) and the second axis is padded
        with np.nan to ensure a rectangular array. 

    """    
    if Octree == None or Octree == 'None' or Octree == 'none':
        # Won't use any octree structure to accelerate intersection tests
        root = None
    elif Octree == 'generate':
        # Create an octree structure based on the provided structure
        root = octree.Surface2Octree(NodeCoords,SurfConn)
    elif type(Octree) == octree.OctreeNode:
        # Using an already generated octree structure
        # If this is the case, it should conform to the same structure and labeling as one generated with octree.Surface2Octree
        root = Octree
    else:
        raise Exception('Invalid Octree argument given: '+str(Octree))
    
    Points = np.array(NodeCoords)[np.array(SurfConn)]   
    if root == None:
        combinations = list(itertools.combinations(range(len(SurfConn)),2))
        idx1,idx2 = zip(*combinations)
        Tri1s = Points[np.array(idx1)]; Tri2s = Points[np.array(idx2)]
    else:
        leaves = octree.getAllLeaf(root)
        combinations = []
        for leaf in leaves:
            combinations += list(itertools.combinations(leaf.data,2))
        
        idx1,idx2 = zip(*combinations)
        Tri1s = Points[np.array(idx1)]; Tri2s = Points[np.array(idx2)]

    if return_pts:
        intersections,intersectionPts = TrianglesTrianglesIntersectionPts(Tri1s,Tri2s,eps=eps)
        IntersectionPairs = np.array(combinations)[intersections].tolist()
        IntersectionPoints = intersectionPts[intersections]
        return IntersectionPairs, IntersectionPoints
        
    else:
        intersections = TrianglesTrianglesIntersection(Tri1s,Tri2s,eps=eps)
        IntersectionPairs = np.array(combinations)[intersections].tolist()
            
    return IntersectionPairs
    
def SurfSurfIntersection(NodeCoords1, SurfConn1, NodeCoords2, SurfConn2, eps=1e-14, return_pts=False):
    """
    Identify intersections between two surface meshes.

    Parameters
    ----------
    NodeCoords1 : array_like
        Node coordinates of the first mesh
    SurfConn1 : list, array_like
        Node connectivity of the first mesh
    NodeCoords2 : array_like
        Node coordinates of the second mesh
    SurfConn2 : list, array_like
        Node connectivity of the second mesh
    eps : float, optional
        Small tolerance parameter, by default 1e-14, by default 1e-14
    return_pts : bool, optional
        If true, will return intersection points, by default False.

    Returns
    -------
    Surf1Intersections : list
        Element ids from the first mesh that intersect with the second
    Surf2Intersections : list
        Element ids from the second mesh that intersect with the first
    IntersectionPoints : list, optional
        Coordinates of intersections (returned if return_pts=True)
    """
    MergeCoords,MergeConn = utils.MergeMesh(NodeCoords1, SurfConn1, NodeCoords2, SurfConn2, cleanup=False)
    root = octree.Surface2Octree(MergeCoords,MergeConn)
    
    Points = np.array(MergeCoords)[np.array(MergeConn)]   
    if root == None:
        combinations = list(itertools.combinations(range(len(MergeConn)),2))
        idx1,idx2 = zip(*combinations)
        Tri1s = Points[np.array(idx1)]; Tri2s = Points[np.array(idx2)]
    else:
        leaves = octree.getAllLeaf(root)
        combinations = []
        for leaf in leaves:
            combinations += list(itertools.combinations(leaf.data,2))
        
        idx1,idx2 = zip(*combinations)
        Tri1s = Points[np.array(idx1)]; Tri2s = Points[np.array(idx2)]

    if return_pts:
        intersections,intersectionPts = TrianglesTrianglesIntersectionPts(Tri1s,Tri2s,eps=eps,edgeedge=True)
        IntersectionPairs = np.array(combinations)[intersections].tolist()
        IPoints = intersectionPts[intersections]
        IPoints[np.isnan(IPoints)] = np.inf
        IPoints = utils.ExtractRagged(IPoints, delval=np.inf)

        # TODO: I'm being lazy here
        Surf1Intersections = []; Surf2Intersections = []; IntersectionPoints = []
        for i in range(len(IntersectionPairs)):
            if IntersectionPairs[i][0] < len(SurfConn1) and IntersectionPairs[i][1] >= len(SurfConn1):
                Surf1Intersections.append(IntersectionPairs[i][0])
                Surf2Intersections.append(IntersectionPairs[i][1]-len(SurfConn1))
                IntersectionPoints.append(IPoints[i])
            elif IntersectionPairs[i][1] < len(SurfConn1) and IntersectionPairs[i][0] >= len(SurfConn1):
                Surf1Intersections.append(IntersectionPairs[i][1])
                Surf2Intersections.append(IntersectionPairs[i][0]-len(SurfConn1))
                IntersectionPoints.append(IPoints[i])
            # Ignoring self intersections
        return Surf1Intersections, Surf2Intersections, IntersectionPoints
        
    else:
        intersections = TrianglesTrianglesIntersection(Tri1s,Tri2s,eps=eps,edgeedge=True)
        IntersectionPairs = np.array(combinations)[intersections].tolist()
        # TODO: I'm being lazy here
        Surf1Intersections = []; Surf2Intersections = []
        for i in range(len(IntersectionPairs)):
            if IntersectionPairs[i][0] < len(SurfConn1) and IntersectionPairs[i][1] >= len(SurfConn1):
                Surf1Intersections.append(IntersectionPairs[i][0])
                Surf2Intersections.append(IntersectionPairs[i][1]-len(SurfConn1))
            elif IntersectionPairs[i][1] < len(SurfConn1) and IntersectionPairs[i][0] >= len(SurfConn1):
                Surf1Intersections.append(IntersectionPairs[i][1])
                Surf2Intersections.append(IntersectionPairs[i][0]-len(SurfConn1))
            
    return Surf1Intersections, Surf2Intersections

def PlaneSurfIntersection(pt, Normal, NodeCoords, SurfConn, eps=1e-14):

    NodeCoords = np.asarray(NodeCoords)
    SurfConn = np.asarray(SurfConn)
    pt = np.asarray(pt)
    Normal = np.asarray(Normal)

    Intersections = PlaneTrianglesIntersection(pt, Normal, NodeCoords[SurfConn], eps=eps)
    return Intersections

## Inside/Outside Tests
def PointInSurf(pt, NodeCoords, SurfConn, ElemNormals, Octree=None, eps=1e-8, ray=np.random.rand(3)):
    """
    Test to determine whether a point is inside a surface mesh.

    Parameters
    ----------
    pt : array_like
        3D coordinates for point shape=(3,).
    NodeCoords : array_like
        List of node coordinates of the surface
    SurfConn : array_like
        Node connectivity of elements. This function is only valid for triangular surface meshes.
    ElemNormals : array_like
        Element normal vectors 
    Octree : None, str, or octree.octreeNode, optional
        Determines whether to use/generate an octree data structure for acceleration of the intersection testing, by default None. 
        'generate' - Will generate an octree structure of the surface
        None - Will not use an octree structure
        octree.octreeNode - Octree data structure precomputed using :func:`mymesh.octree.Surface2Octree`
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-8
    ray : array_like, optional
        Ray that will be cast to determine whether the point is inside or outside the surface, by default np.random.rand(3). For a closed, manifold surface, the choice of ray shouldn't matter.

    Returns
    -------
    inside : bool
        True if the point is inside the surface, otherwise False.
    """    
    root = OctreeInputProcessor(NodeCoords, SurfConn, Octree)
        
    intersections, distances, _ = RaySurfIntersection(pt,ray,NodeCoords,SurfConn,Octree=root)
    posDistances = np.array([d for d in distances if d > eps])
    zero = np.any(np.abs(distances)<eps)
    
    # Checking unique to not double count instances where ray intersects an edge
    if len(np.unique(np.round(posDistances/eps)))%2 == 0 and not zero:
        # No intersection
        inside = False
        return inside
    else:
        dist = min(np.abs(distances))
        if dist < eps:
            closest = np.array(intersections)[np.abs(distances)==dist][0]
            dot = np.dot(ray,ElemNormals[closest])
            return dot
        else:
            # Inside
            inside = True
            return inside

def PointsInSurf(pts, NodeCoords, SurfConn, ElemNormals=None, Octree='generate', eps=1e-8, rays=None):
    """
    Test to determine whether points are inside a surface mesh.

    Parameters
    ----------
    pts : array_like
        3D coordinates for the points shape=(n,3).
    NodeCoords : array_like
        List of node coordinates of the surface
    SurfConn : array_like
        Node connectivity of elements. This function is only valid for triangular surface meshes.
    ElemNormals : array_like, NoneType, optional
        Element normal vectors. If None are provided, they will be calculated.
    Octree : None, str, or octree.octreeNode, optional
        Determines whether to use/generate an octree data structure for acceleration of the intersection testing, by default None. 
        'generate' - Will generate an octree structure of the surface
        None - Will not use an octree structure
        octree.octreeNode - Octree data structure precomputed using :func:`mymesh.octree.Surface2Octree`
    eps : float, optional
        Small parameter used to determine if a value is sufficiently close to 0, by default 1e-8
    rays : array_like, optional
        Rays that will be cast to determine whether the points are inside or outside the surface, by default np.random.rand(3). For a closed, manifold surface, the choice of ray shouldn't matter.

    Returns
    -------
    inside : bool
        True if the point is inside the surface, otherwise False.
    """  
    if rays is None: 
        rays = np.random.rand(len(pts),3)
        rays /= np.linalg.norm(rays,axis=1)[:,None]
    if ElemNormals is None:
        ElemNormals = utils.CalcFaceNormal(NodeCoords, SurfConn)
    root = OctreeInputProcessor(NodeCoords, SurfConn, Octree)
    intersections, distances, _ = RaysSurfIntersection(pts,rays,NodeCoords,SurfConn,Octree=root) 
    Insides = np.repeat(False,len(pts))
    for i in range(len(intersections)):
        posDistances = distances[i][distances[i] > eps]
        zero = np.any(np.abs(distances[i])<eps)
        if len(np.unique(np.round(posDistances/eps)))%2 == 0 and not zero:
            Insides[i] = False
        else:
            dist = min(np.abs(distances[i]))
            if dist < eps:
                # On surface
                closest = intersections[i][np.abs(distances[i])==dist][0]
                dot = np.dot(rays[i],ElemNormals[closest])
                Insides[i] = dot
            else:
                # Inside
                Insides[i] = True
    return Insides

@try_njit
def PointInBox(pt, xlim, ylim, zlim, inclusive=True):
    """
    Test whether a point is inside a box

    Parameters
    ----------
    pt : array_like
        3D coordinates of a point, shape=(3,)
    xlim : array_like
        Lower and upper x limits (e.g. [xmin, xmax])
    ylim : array_like
        Lower and upper y limits (e.g. [ymin, ymax])
    zlim : array_like
        Lower and upper z limits (e.g. [zmin, zmax])

    Returns
    -------
    inside : bool
        True if the point is in the box.
    """    
    lims = [xlim,ylim,zlim]
    inside = True
    for d in range(3):
        if inclusive:
            if not lims[d][0] <= pt[d] <= lims[d][1]:
                inside = False
                break
        else:
            if not lims[d][0] < pt[d] < lims[d][1]:
                inside = False
                break
    return inside

def PointsInVoxel(pts, VoxelCoords, VoxelConn, inclusive=True):    
    """
    Test to determine whether points are inside a voxel mesh

    Parameters
    ----------
    pts : array_like
        3D coordinates of points, shape=(n,3)
    VoxelCoords : array_like
        Node coordinates of the voxel mesh
    VoxelConn : array_like
        Node connectivity of the hexahedral voxel mesh.
    inclusive : bool, optional
        Specifies whether points exactly on the boundary should be included, by
        default True

    Returns
    -------
    inside : list
        List of bools specifying whether each point is inside the mesh.
    """    
    Root = octree.Voxel2Octree(VoxelCoords, VoxelConn)
    inside = [False for i in range(len(pts))]
    for i,pt in enumerate(pts):
        inside[i] = octree.isInsideOctree(pt, Root, inclusive=inclusive)    
    
    return inside
        
def PointInTri(Tri,pt,method='BaryArea',eps=1e-12,inclusive=True):

    if method == 'Normal':
        pts = np.vstack([Tri,pt])
        conn = [[0,1,3],[1,2,3],[2,0,3]]
        normals = utils.CalcFaceNormal(pts,conn)
        if np.dot(normals[0],normals[1]) < 0:
            In = False
        elif np.dot(normals[1],normals[2]) < 0:
            In = False
        else:
            In = True
    elif method == 'Bary':
        alpha,beta,gamma = utils.BaryTri(Tri,pt)
        In = all([alpha>=0,beta>=0,gamma>=0])
    elif method == 'BaryArea':
        A = Tri[0]
        B = Tri[1]
        C = Tri[2]
        AB = np.subtract(A,B)
        AC = np.subtract(A,C)
        PA = np.subtract(pt,A)
        PB = np.subtract(pt,B)
        PC = np.subtract(pt,C)

        Area2 = np.linalg.norm(np.cross(AB,AC))
        
        denom = 1/Area2
        alpha = np.linalg.norm(np.cross(PB,PC))*denom
        beta = np.linalg.norm(np.cross(PC,PA))*denom
        gamma = np.linalg.norm(np.cross(PA,PB))*denom
        if inclusive:
            In = all([alpha>=0,beta>=0,gamma>=0]) and np.abs(alpha+beta+gamma-1) < eps
        else:
            In = all([alpha>=eps,beta>=eps,gamma>=eps]) and np.abs(alpha+beta+gamma-1) < eps
    return In

def PointsInTris(Tris,pts,method='BaryArea',eps=1e-12,inclusive=True):
    # Pairwise comparisons between each triangle in tris and its corresponding point in pts
    if method == 'BaryArea':
        A = Tris[:,0]
        B = Tris[:,1]
        C = Tris[:,2]
        AB = np.subtract(A,B)
        AC = np.subtract(A,C)
        PA = np.subtract(pts,A)
        PB = np.subtract(pts,B)
        PC = np.subtract(pts,C)

        Area2 = np.linalg.norm(np.cross(AB,AC),axis=1)

        
        denom = 1/Area2
        alpha = np.linalg.norm(np.cross(PB,PC),axis=1)*denom
        beta = np.linalg.norm(np.cross(PC,PA),axis=1)*denom
        gamma = np.linalg.norm(np.cross(PA,PB),axis=1)*denom
        # print(alpha,beta,gamma)
        if inclusive:
            In = np.all([alpha>=0,beta>=0,gamma>=0],axis=0) & (np.abs(alpha+beta+gamma-1) <= eps)
        else:
            In = np.all([alpha>=eps,beta>=eps,gamma>=eps],axis=0) & (np.abs(alpha+beta+gamma-1) <= eps)
    return In

@try_njit
def PointInTet(pt,Tet):

    alpha,beta,gamma,delta = utils.BaryTet(Tet,pt)
    In = True
    if alpha < 0:
        In = False
    elif beta < 0:
        In = False
    elif gamma < 0:
        In = False
    elif delta < 0:
        In = False

    return In

def OctreeInputProcessor(NodeCoords, SurfConn, Octree):
    
    if Octree == None or Octree == 'None' or Octree == 'none':
        # Won't use any octree structure to accelerate intersection tests
        root = None
    elif Octree == 'generate':
        # Create an octree structure based on the provided structure
        root = octree.Surface2Octree(NodeCoords,SurfConn)
    elif type(Octree) == octree.OctreeNode:
        # Using an already generated octree structure
        # If this is the case, it should conform to the same structure and labeling as one generated with octree.Surface2Octree
        root = Octree
    else:
        raise Exception('Invalid octree argument given: '+str(Octree))
        
    return root