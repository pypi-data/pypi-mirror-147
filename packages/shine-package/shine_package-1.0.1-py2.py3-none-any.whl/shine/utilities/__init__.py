import numpy as np
from scipy.linalg import eigh
import _shine

def compiled_with_sl():
    return hasattr(_shine, 'new_blacs_context')

def dagger(a):
    return np.conj(a.T)

def dotdot(a, b, c):
    return np.dot(np.dot(a,b),c)

def fermidistribution(energy, kt):
    #fermi level is fixed to zero
    return 1.0 / (1.0 + np.exp(energy / kt))

def is_contiguous(array, dtype=None):
    """Check for contiguity and type."""
    if dtype is None:
        return array.flags.c_contiguous
    else:
        return array.flags.c_contiguous and array.dtype == dtype

def monkhorst_pack(size, odds=[True,True,True]):
    """Construct a uniform sampling of k-space of given size."""
    if np.less_equal(size, 0).any():
        raise ValueError('Illegal size: %s' % list(size))
    kpts = np.indices(size).transpose((1, 2, 3, 0)).reshape((-1, 3))
    kpts =  (kpts + 0.5) / size - 0.5
    for i in range(3):
        if not odds[i]:
            kpts[:,i] -= 0.5 / size[i]
    return kpts

def calculate_density_matrix(Hmm, Smm, fermi, ne, molecule):
    Hmm = (Hmm + dagger(Hmm)) / 2
    Smm = (Smm + dagger(Smm)) / 2
    D,V = eigh(Hmm,Smm)
    E_min = np.min(D)
    E_max = np.max(D)
    dD = np.zeros([Hmm.shape[-1]])
    if molecule:
        ind = np.argsort(D)
        dD[ind[np.arange(ne/2)]] = 1
    else:    
        dD[np.nonzero(D<fermi)] = 1  #how about =fermi?
    Dmm = dotdot(V, np.diag(dD), dagger(V))
    return Dmm, E_min, E_max

def r2k2(s_rmm, R_vector, kvector=(0,0,0), symmetrize=True):
    phase_k = np.dot(2 * np.pi * R_vector, kvector)
    c_k = np.exp(-1.0j * phase_k)
    c_k.shape = (len(R_vector), 1, 1)
    nbf = s_rmm.shape[-1]
    s_mm = np.zeros((nbf, nbf), complex)
    for i in range(len(R_vector)):
        tmp = s_rmm[i,:,:]*c_k[i]
        if symmetrize and R_vector[i,:].any():
            s_mm = s_mm + tmp + dagger(tmp)
        else:
            s_mm = s_mm + tmp
    return s_mm

def get_matrix_index(ind1, ind2=None):
    if ind2 is None:
        dim1 = len(ind1)
        return np.resize(ind1, (dim1, dim1))
    else:
        dim1 = len(ind1)
        dim2 = len(ind2)
    return np.resize(ind1, (dim2, dim1)).T, np.resize(ind2, (dim1, dim2))

