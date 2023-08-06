import numpy as np
from func import nanaverage

def upscaling_2d(matrix, rstep, cstep, func=np.mean, weights=9999,return_w=False):
    '''
    Resample 2d-array data.

    Parameters
    ----------
    matrix : 2d-array
        Input data.
    rstep : int
        Scaling factor for row.
    cstep : int
        Scaling factor for colunm.
    func : TYPE, optional
        DESCRIPTION. The default is np.mean.
    weights : ndarray, optional
        Weights that should have the same shape as matrix. The default is 9999.
    return_w : bool, optional
        Whethert to return resampled weights. The default is False.

    Returns
    -------
    2d-array
        Resampled data.

    '''
    row, col = np.shape(matrix)
    temp = matrix.reshape(int(row / rstep), rstep, int(col / cstep), cstep)
    if np.all(weights==9999):
        temp = func(temp, axis=1)
        temp = func(temp, axis=2)
    else:
        weights = weights.reshape(int(row / rstep), rstep, int(col / cstep), cstep)
        temp = func(temp, axis=1,weights = weights)
        weights = np.nansum(weights, axis=1)
        temp = func(temp, axis=2,weights = weights)
        weights = np.nansum(weights, axis=2)
    return temp


def upscaling(matrix, rstep, cstep, func=np.mean, weights=9999,return_w=False):
    '''
    Resample data with dimension less than 5 to reduce resolution.

    Parameters
    ----------
    matrix : ndarray
        Input data.
    rstep : int
        Scaling factor for row.
    cstep : int
        Scaling factor for colunm.
    func : TYPE, optional
        DESCRIPTION. The default is np.mean.
    weights : ndarray, optional
        Weights that should have the same shape as matrix. The default is 9999.
    return_w : bool, optional
        Whethert to return resampled weights. The default is False.

    Raises
    ------
    ValueError
        The dimension of input data should be less than 5.

    Returns
    -------
    ndarray
        Resampled data.

    '''
    ndim = np.array(matrix.shape)
    ndim[-1] = ndim[-1]/cstep 
    ndim[-2] = ndim[-2]/rstep 
    if len(ndim)==2:
        temp = upscaling_2d(matrix, rstep, cstep, func=func, weights=weights,return_w=return_w)
    if len(ndim)==3:
        temp = np.zeros(ndim)
        for i in range(ndim[0]):
            temp[i] = upscaling_2d(matrix[i], rstep, cstep, func=func, weights=weights,return_w=return_w)
    if len(ndim)==4:
        temp = np.zeros(ndim)
        for i in range(ndim[0]):
            for j in range(ndim[1]):
                temp[i,j] = upscaling_2d(matrix[i,j], rstep, cstep, func=func, weights=weights,return_w=return_w)
    if len(matrix.shape)>4:
        raise ValueError('The dimension of input data should be less than 5.')
    return temp
        

def downscaling(matrix, rstep, cstep):
    '''
    

    Parameters
    ----------
    matrix : TYPE
        DESCRIPTION.
    rstep : TYPE
        DESCRIPTION.
    cstep : TYPE
        DESCRIPTION.

    Returns
    -------
    temp : TYPE
        DESCRIPTION.

    '''
    row, col = np.shape(matrix)
    temp = np.ravel(matrix)
    #Reduce the dimension of the array to one dimension
    temp = np.array([temp[int(i / cstep):int(i / cstep) + 1]
        for i in range(cstep * len(temp))])  #Operate horizontally
    temp = temp.reshape(row, int(col * cstep))
    temp = temp.T
    temp = np.ravel(temp)
    temp = np.array([temp[int(i / rstep):int(i / rstep) + 1]
        for i in range(rstep * len(temp))])  #Operate vetically
    temp = temp.reshape(int(col * cstep), int(row * rstep))
    temp = temp.T
    return temp

    