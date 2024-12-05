from typing import Dict, Union

import numpy as np
import scipy.sparse


def arrays_equal(
    arr1: Union[np.ndarray, scipy.sparse.csr_array],
    arr2: Union[np.ndarray, scipy.sparse.csr_array],
) -> bool:
    if isinstance(arr1, np.ndarray) and isinstance(arr2, np.ndarray):
        return np.array_equal(arr1, arr2, equal_nan=True)
    if (
        scipy.sparse.issparse(arr1)
        and scipy.sparse.issparse(arr2)
        and type(arr1) == type(arr2)
        and arr1.shape == arr2.shape
    ):
        # convert the arrays to a canonical format for comparison
        # for non-CSR arrays this is somewhat inefficient
        # CSR arrays will be the most common
        arr1_: scipy.sparse.csr_array = arr1.tocsr(copy=True)
        arr2_: scipy.sparse.csr_array = arr2.tocsr(copy=True)
        arr1_.sum_duplicates()
        arr2_.sum_duplicates()
        return all(
            [
                np.all(arr1_.data == arr2_.data),
                np.all(arr1_.indices == arr2_.indices),
                np.all(arr1_.indptr == arr2_.indptr),
            ]
        )
    return False


def array_dicts_equal(d1: Dict[str, np.ndarray], d2: Dict[str, np.ndarray]) -> bool:
    if d1.keys() != d2.keys():
        return False
    return all(arrays_equal(d1[k], d2[k]) for k in d1)
