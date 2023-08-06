"""
Plot barycentric
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D, art3d
from scipy.spatial import ConvexHull
from itertools import combinations
import seaborn as sns
import matplotlib.pyplot as plt

from dreye.api.plotting.basic import gradient_color_lineplot
from dreye.api.barycentric import (
    barycentric_dim_reduction, 
    barycentric_to_cartesian, 
    barycentric_to_cartesian_transformer
)


def plot_simplex(
    n=4,
    points=None,
    hull=None,
    gradient_line=None, 
    lines=True,
    ax=None,
    line_color='black',
    hull_color='gray',
    labels=None,
    label_size=16,
    point_colors='blue',
    hull_kws={},
    point_scatter_kws={},
    gradient_line_kws={}, 
    gradient_color=None,
    fig_kws={},
    remove_axes=True
):
    """Plot simplex of points and/or convex hull

    Parameters
    ----------
    n : int, optional
        [description], by default 4
    points : [type], optional
        [description], by default None
    hull : [type], optional
        [description], by default None
    gradient_line : [type], optional
        [description], by default None
    lines : bool, optional
        [description], by default True
    ax : [type], optional
        [description], by default None
    line_color : str, optional
        [description], by default 'black'
    hull_color : str, optional
        [description], by default 'gray'
    labels : [type], optional
        [description], by default None
    label_size : int, optional
        [description], by default 16
    point_colors : str, optional
        [description], by default 'blue'
    hull_kws : dict, optional
        [description], by default {}
    point_scatter_kws : dict, optional
        [description], by default {}
    gradient_line_kws : dict, optional
        [description], by default {}
    gradient_color : [type], optional
        [description], by default None
    fig_kws : dict, optional
        [description], by default {}
    remove_axes : bool, optional
        [description], by default True

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    ValueError
        [description]
    ValueError
        [description]
    """
    hull_kws = hull_kws.copy()
    hull_color = hull_kws.pop('color', hull_color)

    point_scatter_kws = point_scatter_kws.copy()
    point_colors = point_scatter_kws.pop('c', point_colors)
    point_colors = point_scatter_kws.pop('color', point_colors)

    assert n in {2, 3, 4}

    if ax is None:
        if n == 4:
            fig = plt.figure(**fig_kws)
            ax = Axes3D(fig, auto_add_to_figure=False)
            fig.add_axes(ax)
        else:
            fig = plt.figure(**fig_kws)
            ax = plt.subplot(111)

    if hull is not None:
        if n == 2:
            if hull.shape[1] == n:
                pts = barycentric_dim_reduction(hull)
            else:
                pts = hull
        else:
            if not isinstance(hull, ConvexHull):
                if hull.shape[1] == n:
                    hull = barycentric_dim_reduction(hull)
                assert hull.shape[1] == (n-1)
                hull = ConvexHull(hull)
            pts = hull.points
        
        if n == 3:
            for simplex in hull.simplices:
                ax.plot(
                    pts[simplex, 0], pts[simplex, 1],
                    color=hull_color, **hull_kws
                )
        elif n == 2:
            hull_kws['linewidth'] = 3
            ax.plot(
                pts, np.ones(pts.size)*0.2,
                color=hull_color, **hull_kws
            )
        else:
            org_triangles = [pts[s] for s in hull.simplices]
            f = Faces(org_triangles)
            g = f.simplify()

            hull_kws_default = {
                'facecolors': hull_color,
                'edgecolor': 'lightgray',
                'alpha': 0.8
            }
            hull_kws = {**hull_kws_default, **hull_kws}
            pc = art3d.Poly3DCollection(g, **hull_kws)
            ax.add_collection3d(pc)

    if points is not None:
        if points.shape[1] == n:
            X = barycentric_dim_reduction(points)
        elif points.shape[1] == (n-1):
            X = points
        else:
            raise ValueError(
                "`points` argument is the wrong dimension, "
                f"must be `{n}` or `{n-1}`, but is `{points.shape[1]}`."
            )
        if n == 2:
            ax.scatter(X.squeeze(), np.ones(X.size)*0.25, c=point_colors, **point_scatter_kws)
        else:
            ax.scatter(
                *X.T, c=point_colors, **point_scatter_kws
            )

    if lines:
        A = barycentric_to_cartesian_transformer(n)
        lines = combinations(A, 2)
        for line in lines:
            line = np.transpose(np.array(line))
            if n == 4:
                ax.plot3D(*line, c=line_color)
            elif n == 2:
                ax.plot(line.squeeze(), np.ones(line.size)*0.35, c=line_color, linewidth=3)
            else:
                ax.plot(*line, c=line_color)

    if gradient_line is not None:
        if gradient_line.shape[1] == n:
            X = barycentric_dim_reduction(gradient_line)
        elif gradient_line.shape[1] == (n-1):
            X = gradient_line
        else:
            raise ValueError(
                "`points` argument is the wronge dimension, "
                f"must be `{n}` or `{n-1}`, but is `{gradient_line.shape[1]}`."
            )

        if gradient_color is None:
            gradient_color = np.linspace(0, 1, X.shape[0])

        if n == 2:
            gradient_line_kws['linewidth'] = 3
            gradient_color_lineplot(X.squeeze(), np.ones(X.size)*0.3, c=gradient_color, **gradient_line_kws, ax=ax)
        else:
            if n == 4:
                # TODO currently color bar cannot be shown on 3D
                gradient_line_kws['add_colorbar'] = False
            gradient_color_lineplot(*X.T, c=gradient_color, **gradient_line_kws, ax=ax)

    if labels is not None and n != 2:
        eye = np.eye(n)
        eye_cart = barycentric_to_cartesian(eye)
        for idx, (point, label) in enumerate(zip(eye_cart, labels)):
            text_kws = {}
            if idx == 0:
                text_kws['ha'] = 'right'
                text_kws['va'] = 'center'
            elif (idx+1) == n:
                text_kws['ha'] = 'center'
                text_kws['va'] = 'bottom'
            else:
                text_kws['ha'] = 'left'
                text_kws['va'] = 'center'

            ax.text(*point, label, size=label_size, **text_kws)

    if remove_axes:
        if n == 4:
            ax._axis3don = False
        else:
            ax.set_xticks([])
            ax.set_yticks([])
            sns.despine(left=True, bottom=True, ax=ax)
            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, 1.1)
            ax.set_aspect('equal', adjustable='box')

    return ax


class Faces:
    """
    Get faces for 3D convex hull.

    From: https://stackoverflow.com/questions/49098466/plot-3d-convex-closed-regions-in-matplot-lib/49115448
    """

    def __init__(self, tri, sig_dig=12, method="convexhull"):
        self.method = method
        self.tri = np.around(np.array(tri), sig_dig)
        self.grpinx = list(range(len(tri)))
        norms = np.around([self.norm(s) for s in self.tri], sig_dig)
        _, self.inv = np.unique(norms, return_inverse=True, axis=0)

    def norm(self, sq):
        cr = np.cross(sq[2]-sq[0], sq[1]-sq[0])
        return np.abs(cr/np.linalg.norm(cr))

    def isneighbor(self, tr1, tr2):
        a = np.concatenate((tr1, tr2), axis=0)
        return len(a) == len(np.unique(a, axis=0))+2

    def order(self, v):
        if len(v) <= 3:
            return v
        v = np.unique(v, axis=0)
        n = self.norm(v[:3])
        y = np.cross(n, v[1]-v[0])
        y = y/np.linalg.norm(y)
        c = np.dot(v, np.c_[v[1]-v[0], y])
        if self.method == "convexhull":
            h = ConvexHull(c)
            return v[h.vertices]
        else:
            mean = np.mean(c, axis=0)
            d = c-mean
            s = np.arctan2(d[:, 0], d[:, 1])
            return v[np.argsort(s)]

    def simplify(self):
        for i, tri1 in enumerate(self.tri):
            for j, tri2 in enumerate(self.tri):
                if j > i:
                    if (
                        self.isneighbor(tri1, tri2)
                        and
                        self.inv[i] == self.inv[j]
                    ):
                        self.grpinx[j] = self.grpinx[i]
        groups = []
        for i in np.unique(self.grpinx):
            u = self.tri[self.grpinx == i]
            u = np.concatenate([d for d in u])
            u = self.order(u)
            groups.append(u)
        return groups
