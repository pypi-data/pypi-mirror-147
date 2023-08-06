import numpy as np

def running_mean(x, N):
    '''

    Parameters
    ----------
    x : ndarray
        1d array.
    N : int
        Number of elements used to smooth.

    Returns
    -------
    1d array
        Smoothed array.

    '''
    cumsum = np.nancumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def nanravel(matrix):
    '''
    Return a contiguous flattened array without nan.

    Parameters
    ----------
    matrix : ndarray
        Input array.

    Returns
    -------
    matrix : 1d array
        Flattened array.

    '''
    matrix = np.ravel(matrix)
    matrix = matrix[np.logical_not(np.isnan(matrix))]
    return matrix

def listdir(path, suffix, suffix_on=1, prefix_on=0):
    '''
    Return a list containing the names of the files in the directory.
    Filter path with specific suffix(or prefix). This is a improved version of os.listdir

    Parameters
    ----------
    path : string
        Input path.
    suffix : string
        Suffix or prefix.
    suffix_on : bool, optional
        Whether to use suffix. The default is 1.
    prefix : TYPE, optional
        Whether to use suffix. The default is 0.

    Returns
    -------
    ls : list
        A list containing the names of the files in the directory with specific suffix or prefix.

    '''
    if prefix_on == 1:
        num = len(suffix)
        ls = np.array([])
        for p in tem:
            if p[:num] == suffix:
                ls = np.append(ls, p)
    else:
        tem = os.listdir(path)
        if suffix_on == 1:
            num = len(suffix)
            ls = np.array([])
            for p in tem:
                if p[-num:] == suffix:
                    ls = np.append(ls, p)

    return ls



def nanaverage(data,weights=0,axis=9999):
    '''
    Weighted mean for array with nan.

    Parameters
    ----------
    data : ndarray
        Input data.
    weights : nadarry, optional
        DESCRIPTION. The default is 0.
    axis : TYPE, optional
        DESCRIPTION. The default is 100.

    Raises
    ------
    ValueError
        the data and weights are expected to have the same shape and nan values.

    Returns
    -------
    TYPE
        Weighted mean.

    '''
    axis = np.array([axis])
    if np.all(axis == 9999):
        axis = np.arange(len(data.shape))
    if np.all(weights==0):
        weights = np.copy(data)
        weights[:]=1
    if data.shape != weights.shape:
        raise ValueError('data and weights have different shape')
    weights[np.isnan(data)]=np.nan
    if len(nanravel(weights)) != len(nanravel(data)):
        raise ValueError('data and weights have different nan')
    tem1 = np.nansum(data*weights,axis=tuple(axis))
    tem2 = np.nansum(weights,axis=tuple(axis))
    return tem1/tem2

array = np.zeros(1)
def arrayinfo(array,detail=False):
    '''
    Print array info for ndarray.

    Parameters
    ----------
    array : ndarray
        Input array.
    detail : bool, optional
        Whether to print detailed info of the array. The default is False.

    Returns
    -------
    None.

    '''
    if type(array) != np.ndarray:
        print("It's not an numpy.ndarray")
        return None
    array_max = np.max(array)
    if np.isnan(array_max):
        print('Nan exists\nmaxium:{:.2f}'.format(np.nanmax(array)))
        print('minmium:{:.2f}'.format(np.nanmin(array)))
    else:
        print('Nan not exists\nmaxium:{:.2f}'.format(array_max))
        print('minmium:{:.2f}'.format(np.min(array)))
    print('shape:', array.shape)
    print('dtype:', array.dtype)
    if detail:
        print('Unique value:',np.unique(array))
        print('Mean:',np.nanmean(array))
        print('Std:',np.nanstd(array))


def fslice(file,ncore=100):
    '''
    Return file index for mpi parallel computing

    Parameters
    ----------
    file : list
        Results from os.listdir.
    ncore : int, optional
        The number of cpu core used for parallel computing. The default is 100.

    Returns
    -------
    npath : ndarray
        File index for mpi parallel computing.

    '''
    number = len(file_edge)
    npath0 = np.linspace(0, number, ncore + 1, dtype='int32')
    npath = np.array(number,2)
    for i in range(number):
        npath[i,0] = npath0[i]
        npath[i,1] = npath0[i+1]
    return npath

def exclude_outlier(in_array):
    '''
    Exclude outlier (3 sigma)

    Parameters
    ----------
    array : 1d array
        Input data.

    Returns
    -------
    array : 1d array
        Output data with outlier=np.nan.

    '''
    array = np.copy(in_array)
    arraystd = np.nanstd(array, ddof=1)
    arraymean = np.nanmean(array)
    arrayoutlier = np.where(np.abs(array - arraymean) > (3 * arraystd))
    print(array[arrayoutlier])
    print(arraystd)
    array[arrayoutlier] = np.nan
    return array

'''
220422 
It seems that the outlier will be eventually excluded in a few loops
n = np.zeros((1000))
for i in range(1000):
    aa = np.random.normal(100,10,20000)
    bb = exclude_outlier(aa)
    while np.nanstd(aa, ddof=1) != np.nanstd(bb, ddof=1):
        aa = bb
        bb = exclude_outlier(aa)
        n[i] = n[i]+1
'''







