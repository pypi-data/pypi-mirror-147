"""
Handling n-dimensional spherical coordinates
"""

import numpy as np

from dreye.api.utils import l2norm


def spherical_to_cartesian(Y):
    """
    Convert from spherical to cartesian coordinates. 
    
    Parameters
    ----------
    Y : array-like (..., ndim)
        Array where the last axis corresponds to the dimensions of each spherical coordinate
        starting with the radius and ending with the angle that spans 2pi. The other angles
        only span pi. All angle dimensions must be in radians.
        
    Returns
    -------
    X : array-like (..., ndim)
        `Y` in cartesian corrdinates.
    """
    if Y.shape[-1] == 1:
        return Y
    
    # first dimension are the radii, the rest are angles
    angles = Y[..., 1:]
    r = Y[..., :1]
    
    # cosine and sine of all angle values
    cosx = np.cos(angles)
    sinx = np.sin(angles)
    
    X = np.zeros(Y.shape)
    # first dimension
    X[..., 0] = cosx[..., 0]
    # second to second to last
    for i in range(1, Y.shape[-1] - 1):
        X[..., i] = cosx[..., i] * np.prod(sinx[..., :i], axis=-1)
    # last
    X[..., -1] = np.prod(sinx, axis=-1)
    
    return X * r


def cartesian_to_spherical(X):
    """
    Convert from cartesian to spherical coordinates.
    
    Parameters
    ----------
    X : array-like (..., ndim)
        Array where the last axis corresponds to the dimensions in cartesian coordinates.
        
    Returns
    -------
    Y : array-like (..., ndim)
        Array where the last axis corresponds to the dimensions of each spherical coordinate
        starting with the radius and ending with the angle that spans 2pi. The other angles
        only span pi. All angle dimensions must be in radians.
    """
    
    if X.shape[-1] == 1:
        return X
    
    r = l2norm(X, axis=-1)
    Y = np.zeros(X.shape)
    Y[..., 0] = r
    d = X.shape[1] - 1
    zeros = (X == 0)
    
    for i in range(d-1):
        Y[..., i+1] = np.where(
            zeros[:, i:].all(-1),
            0,
            np.arccos(X[..., i]/l2norm(X[..., i:], axis=-1))
        )
    
    lasty = np.arccos(X[..., -2]/l2norm(X[..., -2:], axis=-1))
    Y[..., -1] = np.where(
        zeros[:, -2:].all(-1), 
        0, 
        np.where(
            X[..., -1] >= 0, 
            lasty, 
            2*np.pi - lasty
        )
    )
    return Y