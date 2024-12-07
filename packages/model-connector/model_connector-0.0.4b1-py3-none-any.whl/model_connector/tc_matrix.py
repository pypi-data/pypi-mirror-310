"""Model connector for TC matrix management such as DLL loading, common constants, and common classes."""

import ctypes
from enum import Enum
from pathlib import Path
from typing import Optional

import numpy as np

from model_connector.tc_matrix_dll import _BaseMatrixTC

_MAX_FLABEL = 64
_MAX_PATH = 260


class _MatrixDim(Enum):
    ROW = 0
    COL = 1


class _ControlType(Enum):
    FALSE = 0
    TRUE = 1
    NEVER = 2
    ALWAYS = 3
    AUTOMATIC = 4


class ConvertMissing(Enum):
    ZERO = 0  # Convert missing data to zero
    NAN = 1  # Convert missing data to NaN
    IGNORE = 2  # Ignore missing data, leaving sentinel values


class _DataType(Enum):
    UNKNOWN_TYPE = 0
    SHORT_TYPE = 1
    LONG_TYPE = 2
    FLOAT_TYPE = 3
    DOUBLE_TYPE = 4


_np_dtype: dict[_DataType, np.dtype] = {
    _DataType.SHORT_TYPE: np.dtype(np.int16),
    _DataType.LONG_TYPE: np.dtype(np.int32),
    _DataType.FLOAT_TYPE: np.dtype(np.float32),
    _DataType.DOUBLE_TYPE: np.dtype(np.float64),
}

_missing: dict[_DataType, np.int16 | np.int32 | np.float32 | np.float64] = {
    _DataType.SHORT_TYPE: np.int16(-32767),
    _DataType.LONG_TYPE: np.int32(-2147483647),
    _DataType.FLOAT_TYPE: np.float32(-3.402823466e38),
    _DataType.DOUBLE_TYPE: np.float64(-1.7976931348623158e308),
}


def read_matrix_tc(
    matrix_file: Path | str,
    missing: ConvertMissing = ConvertMissing.ZERO,
    cores: list[str] | None = None,
    row_index: int | None = None,
    col_index: int | None = None,
) -> dict[str, np.ndarray]:
    """Read a TransCAD matrix file and returns a dictionary of numpy arrays.

    Parameters
    ----------
    matrix_file : Path | str
        The path to the TransCAD matrix file.
    missing : ConvertMissing, optional
        Specifies how to handle missing values. Defaults to
        ConvertMissing.ZERO.
    cores : list[str], optional
        A list of core names to read from the matrix file. If None, all cores
        are read. Defaults to None.
    row_index : int, optional
        The row index to set for the matrix. If None, use the base index.
        Defaults to None.
    col_index : int, optional
        The column index to set for the matrix. If None, use the base index.
        Defaults to None.

    Returns
    -------
        dict[str, np.ndarray]
            A dictionary where keys are core names and values are numpy arrays
            representing the matrix data.

    The row and column index values must be provided as integers, as index names
    are not currently supported.

    The default behavior is to convert missing data to zero. Missing data can only
    be set to NaN for floating point data types or an error will be raised.
    Convert missing to NAN by setting missing=ConvertMissing.NAN.
    """

    matrix_file = Path(matrix_file)
    mat_dict = {}

    with OpenMatrixTC(matrix_file, missing=missing) as mat:

        mat_cores = mat.core_names
        if cores is not None:
            _validate_cores(mat_cores, cores)
            mat_cores = cores

        if row_index is not None or col_index is not None:
            mat.set_index(row_index, col_index)

        for core in mat_cores:
            mat_dict[core] = mat[core]

    return mat_dict


def _validate_cores(available_cores, requested_cores):
    """Validate that the requested cores are available in the matrix."""
    for core in requested_cores:
        if core not in available_cores:
            raise ValueError(f"Core {core} not found in the matrix.")


class MatrixTC:
    def __init__(
        self,
        handle: ctypes.c_void_p,
        tcw: ctypes.WinDLL,
        filename: Path,
        missing: ConvertMissing = ConvertMissing.ZERO,
    ):
        self.handle: ctypes.c_void_p = handle
        self.tcw: ctypes.WinDLL = tcw
        self.filename: Path = filename
        self._missing: ConvertMissing = missing
        self._dtype: Optional[_DataType] = None
        self._core_count: Optional[int] = None
        self._core_names: Optional[list[str]] = None
        self._shape: Optional[tuple[int, int]] = None
        self._index_count: Optional[tuple[int, int]] = None
        self._index: Optional[tuple[int, int]] = None
        self._row_ids: Optional[np.ndarray] = None
        self._col_ids: Optional[np.ndarray] = None

    def clear_cache(self):
        """Clear cached properties."""
        self._dtype = None
        self._core_count = None
        self._core_names = None
        self._shape = None
        self._index_count = None
        self._index = None
        self._row_ids = None
        self._col_ids = None

    @property
    def missing(self) -> ConvertMissing:
        """Get the missing data conversion setting."""
        return self._missing

    @missing.setter
    def missing(self, value: ConvertMissing) -> None:
        """Set the missing data conversion setting."""
        if value == ConvertMissing.NAN and (
            self.dtype == _DataType.SHORT_TYPE or self.dtype == _DataType.LONG_TYPE
        ):
            raise ValueError("Cannot convert missing to NaN for integer matrix files.")
        self._missing = value

    @property
    def dtype(self) -> _DataType:
        """Get the TransCAD data type of the matrix."""
        if self._dtype is None:
            self._dtype = self._get_dtype()

        return self._dtype

    def _get_dtype(self) -> _DataType:
        dtype = self.tcw.MATRIX_GetDataType(self.handle)
        if dtype == _DataType.UNKNOWN_TYPE.value:
            raise OSError(f"Failed to get data type from matrix {self.filename}.")
        return _DataType(dtype)

    @property
    def np_dtype(self) -> np.dtype:
        """Get the numpy data type of the matrix."""
        return _np_dtype[self.dtype]

    @property
    def shape(self) -> tuple[int, int]:
        """Get the shape of the matrix, using the current index."""
        if self._shape is None:
            self._shape = self._get_shape()
        return self._shape

    def _get_shape(self) -> tuple[int, int]:
        n_rows = self.tcw.MATRIX_GetNRows(self.handle)
        if not n_rows:
            raise OSError(f"Failed to get row  count from matrix {self.filename}.")

        n_cols = self.tcw.MATRIX_GetNCols(self.handle)
        if not n_cols:
            raise OSError(f"Failed to get column count from matrix {self.filename}.")

        return (n_rows, n_cols)

    @property
    def core_count(self) -> int:
        """Get the number of cores in the matrix."""
        if self._core_count is None:
            self._core_count = self._get_core_count()
        return self._core_count

    def _get_core_count(self) -> int:
        core_count = self.tcw.MATRIX_GetNCores(self.handle)
        if not core_count:
            raise OSError(f"Failed to get core count from matrix {self.filename}.")
        return core_count

    @property
    def core_names(self) -> list[str]:
        """Get a list of core names in the matrix."""
        if self._core_names is None:
            self._core_names = self._get_cores()
        return self._core_names

    def _get_cores(self) -> list[str]:
        core_names = []
        sz_label = ctypes.create_string_buffer(_MAX_FLABEL)
        for core_index in range(self.core_count):
            self.tcw.MATRIX_GetLabel(self.handle, core_index, sz_label)
            core_names.append(sz_label.value.decode("utf-8"))

        self._core_names = core_names
        return core_names

    @property
    def index_count(self) -> tuple[int, int]:
        """Get the number of matrix (row, column) indices."""
        if self._index_count is None:
            self._index_count = self._get_index_count()
        return self._index_count

    def _get_index_count(self) -> tuple[int, int]:
        row_count = self.tcw.MATRIX_GetNIndices(self.handle, _MatrixDim.ROW.value)
        col_count = self.tcw.MATRIX_GetNIndices(self.handle, _MatrixDim.COL.value)

        return (row_count, col_count)

    @property
    def index(self) -> tuple[int, int]:
        """Get the current matrix (row, column) index ids."""
        if self._index is None:
            self._index = self._get_index()
        return self._index

    def _get_index(self) -> tuple[int, int]:
        row_index = self.tcw.MATRIX_GetCurrentIndexPos(
            self.handle, _MatrixDim.ROW.value
        )
        col_index = self.tcw.MATRIX_GetCurrentIndexPos(
            self.handle, _MatrixDim.COL.value
        )
        return (row_index, col_index)

    def set_index(self, row_index: Optional[int], col_index: Optional[int]) -> None:
        """Set the current matrix (row, column) index ids. None will leave the index unchanged."""

        self.clear_cache()

        if row_index is not None:
            if row_index < 0 or row_index >= self.index_count[0]:
                raise IndexError(f"Row index {row_index} out of range.")
            self.tcw.MATRIX_SetIndex(self.handle, _MatrixDim.ROW.value, row_index)
        if col_index is not None:
            if col_index < 0 or col_index >= self.index_count[1]:
                raise IndexError(f"Column index {col_index} out of range.")
            self.tcw.MATRIX_SetIndex(self.handle, _MatrixDim.COL.value, col_index)

    @property
    def row_ids(self) -> np.ndarray:
        """Get the row ids for the current matrix index."""
        if self._row_ids is None:
            self._row_ids = self._get_ids(_MatrixDim.ROW)
        return self._row_ids

    @property
    def col_ids(self) -> np.ndarray:
        """Get the column ids for the current matrix index."""
        if self._col_ids is None:
            self._col_ids = self._get_ids(_MatrixDim.COL)
        return self._col_ids

    def _get_ids(self, dimension: _MatrixDim) -> np.ndarray:
        count = self.shape[dimension.value]
        ids = np.zeros(count, np.int32)
        ids_p = ids.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        self.tcw.MATRIX_GetIDs(self.handle, dimension.value, ids_p)
        return ids

    def __getitem__(self, key: str | int) -> np.ndarray:
        """Get a numpy array of matrix data given a string (core name)
        or integer (zero-based core index)."""
        if isinstance(key, str):
            data = self._read_core(key)
        elif isinstance(key, int):
            data = self._read_core_by_index(key)
        else:
            raise TypeError(
                "Key must be a string (core name) or integer (zero-based core index)."
            )

        match self._missing:
            case ConvertMissing.ZERO:
                self._set_missing_zero(data)  # Modifies data inplace to avoid a copy
            case ConvertMissing.NAN:
                if (
                    self.dtype == _DataType.SHORT_TYPE
                    or self.dtype == _DataType.LONG_TYPE
                ):
                    raise ValueError(
                        "Cannot convert missing to NaN for integer matrix files."
                    )
                self._set_missing_nan(data)  # Modifies data inplace to avoid a copy

        return data

    def _read_core(self, core_name: str) -> np.ndarray:
        """Read a core from a TransCAD matrix file given the core name."""
        try:
            core_index = self.core_names.index(core_name)
        except ValueError:
            raise KeyError(
                f"Core name {core_name} not found in matrix {self.filename}."
            )
        return self._read_core_by_index(core_index)

    def _read_core_by_index(self, core_index: int) -> np.ndarray:
        """Read a core from a TransCAD matrix file given the core index."""

        if core_index < 0 or core_index >= self.core_count:
            raise IndexError(
                f"Core index {core_index} out of range for matrix {self.filename}."
            )

        buffer = np.empty(self.shape, self.np_dtype)
        with _CoreAccess(self, core_index):
            if self.index == (0, 0):
                self._read_base_data(core_index, buffer)
            else:
                self._read_indexed_data(core_index, buffer)

        return buffer

    def _read_base_data(self, core_index: int, buffer) -> None:

        for row in range(buffer.shape[0]):
            row_array_p = buffer[row].ctypes.data_as(ctypes.c_void_p)
            rv = self.tcw.MATRIX_GetBaseVector(
                self.handle,
                row,
                _MatrixDim.ROW.value,
                self.dtype.value,
                row_array_p,
            )

            assert rv == 0, f"Failed to read row {row} from core {core_index}."

    def _read_indexed_data(self, core_index: int, buffer) -> None:
        """Read data using the current index."""

        row_ids = self.row_ids
        for row in range(buffer.shape[0]):
            row_array_p = buffer[row].ctypes.data_as(ctypes.c_void_p)
            rv = self.tcw.MATRIX_GetVector(
                self.handle,
                row_ids[row],
                _MatrixDim.ROW.value,
                self.dtype.value,
                row_array_p,
            )

            assert rv == 0, f"Failed to read row {row} from core {core_index}."

    def _set_missing_zero(self, data: np.ndarray) -> None:
        """Convert missing data indicators to zero."""
        np.putmask(data, data == _missing[self.dtype], 0)

    def _set_missing_nan(self, data: np.ndarray) -> None:
        """Convert missing data indicators to NaN."""
        np.putmask(data, data == _missing[self.dtype], np.nan)


class OpenMatrixTC(_BaseMatrixTC):
    """Context manager to open a TransCAD matrix file and close it when done."""

    def __init__(
        self, matrix_file: Path | str, missing: ConvertMissing = ConvertMissing.ZERO
    ):
        # Check for a valid matrix file before proceeding
        # Exit if not found
        matrix_file = Path(matrix_file)
        if not matrix_file.exists():
            raise FileNotFoundError(f"Matrix file not found: {matrix_file}")

        super().__init__(matrix_file)
        self._missing = missing

    def __enter__(self):

        # Open the matrix file
        self.mat = self._open_matrix()

        mat_obj = MatrixTC(self.mat, self._tcw, self._file, self._missing)

        if self._missing == ConvertMissing.NAN and (
            mat_obj.dtype == _DataType.SHORT_TYPE
            or mat_obj.dtype == _DataType.LONG_TYPE
        ):
            self.__exit__(None, None, None)
            raise ValueError("Cannot convert missing to NAN for integer matrix files.")

        return mat_obj

    def __exit__(self, exc_type, exc_value, traceback) -> bool:

        # Release the matrix
        self._close_matrix()

        # Run the parent class exit method
        super().__exit__(exc_type, exc_value, traceback)

        # Returning False propagates exceptions, True suppresses them
        return False

    def _open_matrix(self) -> ctypes.c_void_p:
        """Open a TransCAD matrix file using
        MATRIX  MATRIX_LoadFromFile(char *szFileName, CONTROL_TYPE FileBased);"""

        mat = self._tcw.MATRIX_LoadFromFile(self._file_b, _ControlType.TRUE.value)
        if not mat:
            raise OSError(f"Failed to open matrix file: {self._file}")

        return ctypes.c_void_p(mat)

    def _close_matrix(self) -> None:
        """Close a transcad matrix file using
        short   MATRIX_Done(MATRIX  hMatrix);"""

        rv = self._tcw.MATRIX_Done(self.mat)

        if rv:
            raise OSError(f"Failed to release matrix file: {self._file}")


class _CoreAccess:
    """Context manager to access a specific core in a matrix file.
    - Sets the core index on entry and restores it on exit.
    - Uses OpenFile to increase matrix access speed."""

    def __init__(self, mat: MatrixTC, core_index: int):
        self.mat = mat
        self.core_index = core_index
        self.orig_core = None

    def __enter__(self):
        self.orig_core = self.mat.tcw.MATRIX_GetCore(self.mat.handle)
        self.mat.tcw.MATRIX_OpenFile(self.mat.handle, True)
        self.mat.tcw.MATRIX_SetCore(self.mat.handle, self.core_index)
        return None

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.mat.tcw.MATRIX_SetCore(self.mat.handle, self.orig_core)
        self.mat.tcw.MATRIX_CloseFile(self.mat.handle)
        return False  # Propagate exceptions
