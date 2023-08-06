"""Store xarray Datasets using PyTables, with support for `attrs`.

This is admittedly a bit hackish, but makes it easier to store Datasets and
DataFrames together in the same HDF5 file. If you just have Datasets, you should
use NETCDF.
"""
import importlib.resources
import typing as t

import h5py
import pandas as pd
import xarray as xr

__version__ = importlib.resources.read_text(__name__, '__version__')


def dataset_to_dataframe(ds: xr.Dataset, dim_order: t.List[str] = None):
    """Convert an xarray Dataset to a pandas DataFrame.

    Stores Dataset attributes and fixes the merged/expand_dims dimension names
    bug.

    Parameters
    ----------
    ds : xr.Dataset
        The Dataset to convert.
    dim_order : list[str], optional
        The order of the dimensions. If provided, must use all dimensions in the
        dataset. If not provided, use alphabetical order.

    Attributes
    ----------
    Pandas doesn't have great support for attributes. Indexes don't support
    them, they vanish easily, and serialization has varying support. To get
    around this, attributes are named using the following convention::

        'dataset_attrs::{varname}::{attr}'

    So for a dataset that has:

    - coordinate variables 'time' and 'node',
    - data variables 'disp' and 'force',
    - and 'units' attributes on all its variables except for 'node',

    the resulting attrs dict will look like::

        {
            'dataset_attrs::time::units': 's',
            'dataset_attrs::disp::units': 'm',
            'dataset_attrs::force::units': 'N',
        }
    """
    if dim_order is None:
        dim_order = sorted(ds.dims)
    df = ds.to_dataframe(dim_order)

    # Make sure that indexes are actually named; if `ds` has merged dimensions,
    # or possibly
    # those names aren't carried over by `to_dataframe`. Probably a bug.
    df.index.names = dim_order

    # Store top-level attributes
    for attr, value in ds.attrs.items():
        df.attrs[attr] = value

    # Store variable attributes; since `Index` objects don't support `attrs`,
    # store everything on the top-level DataFrame
    for varname, var in ds.variables.items():
        for attr, value in var.attrs.items():
            df.attrs[f'dataset_attrs::{varname}::{attr}'] = value

    return df


def dataframe_to_dataset(df: pd.DataFrame):
    """Convert a DataFrame to a Dataset, respecting the attribute naming
    convention of `dataset_to_dataframe`.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to convert.
    """
    ds = xr.Dataset.from_dataframe(df)

    for attr, value in df.attrs.items():
        if isinstance(attr, str) and attr.startswith('dataset_attrs::'):
            _, varname, ds_attr = attr.split('::', maxsplit=2)
            ds[varname].attrs[ds_attr] = value
        else:
            ds.attrs[attr] = value

    return ds


def dataframe_to_hdf(df: pd.DataFrame,
                     filename: str,
                     key: str,
                     mode: str = 'a',
                     compress: bool = False,
                     format: str = None,
                     save_attrs: bool = True):
    """Convenience wrapper around DataFrame.to_hdf that supports serializing
    attributes.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to store.
    filename : str
        The file to store in.
    key : str
        The HDF5 key to store the DataFrame in.
    mode : str = 'a'
        The mode to open `filename` in.
    compress : bool = False
        If True, compress using BLOSC. Implies ``format='table'``.
    format : {'fixed', 'table'} = None
        Format to store in. 'fixed' is faster, but doesn't allow compression or
        partial reads.
    save_attrs : bool = True
        If True, save the attributes of `df` as well. Some may not serialize
        well, so this is optional.
    """
    if compress:
        options = dict(complib='blosc', complevel=9, format='table')
    else:
        options = dict(format=format)

    df.to_hdf(filename, key, mode, **options)

    if save_attrs:
        with h5py.File(filename, mode='a') as file:
            for attr, value in df.attrs.items():
                if isinstance(attr, str):
                    h5attr_name = f'dataframe_attrs::{attr}'
                    file[key].attrs[h5attr_name] = value


def hdf_to_dataframe(filename: str, key: str):
    """Read a DataFrame stored by dataframe_to_hdf, including attributes.

    Parameters
    ----------
    filename : str
        File to read from.
    key : str
        HDF key to read from.
    """
    df: pd.DataFrame = pd.read_hdf(filename, key)

    with h5py.File(filename, mode='r') as file:
        attr: str
        for attr in file[key].attrs:
            if attr.startswith('dataframe_attrs::'):
                value = file[key].attrs[attr]
                _, name = attr.split('::', maxsplit=1)
                df.attrs[name] = value

    return df


def dataset_to_hdf(ds: xr.Dataset,
                   filename: str,
                   key: str,
                   mode: str = 'a',
                   compress: bool = False,
                   format: str = None,
                   save_attrs: bool = True):
    """Store an xarray Dataset in an HDF5 file using PyTables.

    Parameters
    ----------
    ds : xr.Dataset
        The Dataset to store.
    filename : str
        The file to store in.
    key : str
        The HDF5 key to store the Dataset in.
    mode : str = 'a'
        The mode to open `filename` in.
    compress : bool = False
        If True, compress using BLOSC. Implies ``format='table'``.
    format : {'fixed', 'table'} = None
        Format to store in. 'fixed' is faster, but doesn't allow compression or
        partial reads.
    save_attrs : bool = True
        If True, save the attributes of `ds` as well. Some may not serialize
        well, so this is optional.
    """
    df = dataset_to_dataframe(ds)
    dataframe_to_hdf(df,
                     filename,
                     key,
                     mode,
                     compress=compress,
                     format=format,
                     save_attrs=save_attrs)


def hdf_to_dataset(filename: str, key: str):
    """Load an xarray Dataset from an HDF5 file, including attributes.

    Parameters
    ----------
    filename : str
        File to read from.
    key : str
        HDF key to read from.
    """
    df = hdf_to_dataframe(filename, key)
    ds = dataframe_to_dataset(df)

    return ds
