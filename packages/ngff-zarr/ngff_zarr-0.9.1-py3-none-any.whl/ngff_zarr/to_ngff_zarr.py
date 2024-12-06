import sys
from collections.abc import MutableMapping
from dataclasses import asdict
from pathlib import Path, PurePosixPath
from typing import Optional, Union

if sys.version_info < (3, 10):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

import dask.array
import numpy as np
import zarr
from itkwasm import array_like_to_numpy_array
from zarr.storage import BaseStore

from .config import config
from .memory_usage import memory_usage
from .methods._support import _dim_scale_factors
from .multiscales import Multiscales
from .rich_dask_progress import NgffProgress, NgffProgressCallback
from .to_multiscales import to_multiscales


def _pop_metadata_optionals(metadata_dict):
    for ax in metadata_dict["axes"]:
        if ax["unit"] is None:
            ax.pop("unit")

    if metadata_dict["coordinateTransformations"] is None:
        metadata_dict.pop("coordinateTransformations")

    return metadata_dict


def _prep_for_to_zarr(
    store: Union[MutableMapping, str, Path, BaseStore], arr: dask.array.Array
) -> dask.array.Array:
    try:
        importlib_metadata.distribution("kvikio")
        _KVIKIO_AVAILABLE = True
    except importlib_metadata.PackageNotFoundError:
        _KVIKIO_AVAILABLE = False

    if _KVIKIO_AVAILABLE:
        from kvikio.zarr import GDSStore

        if not isinstance(store, GDSStore):
            arr = dask.array.map_blocks(
                array_like_to_numpy_array,
                arr,
                dtype=arr.dtype,
                meta=np.empty(()),
            )
        return arr
    return dask.array.map_blocks(
        array_like_to_numpy_array, arr, dtype=arr.dtype, meta=np.empty(())
    )


def to_ngff_zarr(
    store: Union[MutableMapping, str, Path, BaseStore],
    multiscales: Multiscales,
    overwrite: bool = True,
    chunk_store: Optional[Union[MutableMapping, str, Path, BaseStore]] = None,
    progress: Optional[Union[NgffProgress, NgffProgressCallback]] = None,
    **kwargs,
) -> None:
    """
    Write an image pixel array and metadata to a Zarr store with the OME-NGFF standard data model.

    :param store: Store or path to directory in file system.
    :type  store: MutableMapping, str or Path, zarr.storage.BaseStore

    :param multiscales: Multiscales OME-NGFF image pixel data and metadata. Can be generated with ngff_zarr.to_multiscales.
    :type  multiscales: Multiscales

    :param overwrite: If True, delete any pre-existing data in `store` before creating groups.
    :type  overwrite: bool, optional

    :param chunk_store: Separate storage for chunks. If not provided, `store` will be used
        for storage of both chunks and metadata.
    :type  chunk_store: MutableMapping, str or Path, zarr.storage.BaseStore, optional

    :type  progress: RichDaskProgress
    :param progress: Optional progress logger

    :param **kwargs: Passed to the zarr.creation.create() function, e.g., compression options.
    """

    metadata_dict = asdict(multiscales.metadata)
    metadata_dict = _pop_metadata_optionals(metadata_dict)
    metadata_dict["@type"] = "ngff:Image"
    root = zarr.group(store, overwrite=overwrite, chunk_store=chunk_store)
    root.attrs["multiscales"] = [metadata_dict]

    nscales = len(multiscales.images)
    if progress:
        progress.add_multiscales_task("[green]Writing scales", nscales)
    next_image = multiscales.images[0]
    dims = next_image.dims
    previous_dim_factors = {d: 1 for d in dims}
    for index in range(nscales):
        if progress:
            progress.update_multiscales_task_completed(index + 1)
        image = next_image
        arr = image.data
        path = multiscales.metadata.datasets[index].path
        parent = str(PurePosixPath(path).parent)
        if parent not in (".", "/"):
            array_dims_group = root.create_group(parent)
            array_dims_group.attrs["_ARRAY_DIMENSIONS"] = image.dims

        if index > 0 and index < nscales - 1 and multiscales.scale_factors:
            dim_factors = _dim_scale_factors(
                dims, multiscales.scale_factors[index], previous_dim_factors
            )
        else:
            dim_factors = {d: 1 for d in dims}
        previous_dim_factors = dim_factors

        if memory_usage(image) > config.memory_target and multiscales.scale_factors:
            shrink_factors = []
            for dim in dims:
                if dim in dim_factors:
                    shrink_factors.append(dim_factors[dim])
                else:
                    shrink_factors.append(1)

            chunks = tuple([c[0] for c in arr.chunks])
            zarr_array = zarr.creation.open_array(
                shape=arr.shape,
                chunks=chunks,
                dtype=arr.dtype,
                store=store,
                path=path,
                mode="a",
                dimension_separator="/",
            )

            shape = image.data.shape
            x_index = dims.index("x")
            y_index = dims.index("y")
            if "z" in dims:
                z_index = dims.index("z")
                # TODO address, c, t, large 2D
                slice_bytes = memory_usage(image, {"z"})
                slab_slices = min(
                    int(np.ceil(config.memory_target / slice_bytes)), arr.shape[z_index]
                )
                z_chunks = chunks[z_index]
                slice_planes = False
                if slab_slices < z_chunks:
                    slab_slices = z_chunks
                    slice_planes = True
                if slab_slices > arr.shape[z_index]:
                    slab_slices = arr.shape[z_index]
                slab_slices = int(slab_slices / z_chunks) * z_chunks
                num_z_splits = int(np.ceil(shape[z_index] / slab_slices))
                while num_z_splits % shrink_factors[z_index] > 1:
                    num_z_splits += 1
                num_y_splits = 1
                num_x_splits = 1
                regions = []
                for slab_index in range(num_z_splits):
                    if slice_planes:
                        plane_bytes = memory_usage(image, {"z", "y"})
                        plane_slices = min(
                            int(np.ceil(config.memory_target / plane_bytes)),
                            arr.shape[y_index],
                        )
                        y_chunks = chunks[y_index]
                        slice_strips = False
                        if plane_slices < y_chunks:
                            plane_slices = y_chunks
                            slice_strips = True
                        if plane_slices > arr.shape[y_index]:
                            plane_slices = arr.shape[y_index]
                        plane_slices = int(plane_slices / y_chunks) * y_chunks
                        num_y_splits = int(np.ceil(shape[y_index] / plane_slices))
                        while num_y_splits % shrink_factors[y_index] > 1:
                            num_y_splits += 1
                        if slice_strips:
                            strip_bytes = memory_usage(image, {"z", "y", "x"})
                            strip_slices = min(
                                int(np.ceil(config.memory_target / strip_bytes)),
                                arr.shape[x_index],
                            )
                            x_chunks = chunks[x_index]
                            strip_slices = max(strip_slices, x_chunks)
                            slice_strips = False
                            if strip_slices > arr.shape[x_index]:
                                strip_slices = arr.shape[x_index]
                            strip_slices = int(strip_slices / x_chunks) * x_chunks
                            num_x_splits = int(np.ceil(shape[x_index] / strip_slices))
                            while num_x_splits % shrink_factors[x_index] > 1:
                                num_x_splits += 1
                            for plane_index in range(num_y_splits):
                                for strip_index in range(num_x_splits):
                                    region = [
                                        slice(arr.shape[i]) for i in range(arr.ndim)
                                    ]
                                    region[z_index] = slice(
                                        slab_index * z_chunks,
                                        min(
                                            (slab_index + 1) * z_chunks,
                                            arr.shape[z_index],
                                        ),
                                    )
                                    region[y_index] = slice(
                                        plane_index * y_chunks,
                                        min(
                                            (plane_index + 1) * y_chunks,
                                            arr.shape[y_index],
                                        ),
                                    )
                                    region[x_index] = slice(
                                        strip_index * x_chunks,
                                        min(
                                            (strip_index + 1) * x_chunks,
                                            arr.shape[x_index],
                                        ),
                                    )
                                    regions.append(tuple(region))
                        else:
                            for plane_index in range(num_y_splits):
                                region = [slice(arr.shape[i]) for i in range(arr.ndim)]
                                region[z_index] = slice(
                                    slab_index * z_chunks,
                                    min(
                                        (slab_index + 1) * z_chunks, arr.shape[z_index]
                                    ),
                                )
                                region[y_index] = slice(
                                    plane_index * y_chunks,
                                    min(
                                        (plane_index + 1) * y_chunks, arr.shape[y_index]
                                    ),
                                )
                                regions.append(tuple(region))
                    else:
                        region = [slice(arr.shape[i]) for i in range(arr.ndim)]
                        region[z_index] = slice(
                            slab_index * z_chunks,
                            min((slab_index + 1) * z_chunks, arr.shape[z_index]),
                        )
                        regions.append(tuple(region))
                regions = tuple(regions)
                for region_index, region in enumerate(regions):
                    if isinstance(progress, NgffProgressCallback):
                        progress.add_callback_task(
                            f"[green]Writing scale {index+1} of {nscales}, region {region_index+1} of {len(regions)}"
                        )
                    arr_region = arr[region]
                    arr_region = _prep_for_to_zarr(store, arr_region)
                    optimized = dask.array.Array(
                        dask.array.optimize(
                            arr_region.__dask_graph__(), arr_region.__dask_keys__()
                        ),
                        arr_region.name,
                        arr_region.chunks,
                        meta=arr_region,
                    )
                    dask.array.to_zarr(
                        optimized,
                        zarr_array,
                        region=region,
                        component=path,
                        overwrite=False,
                        compute=True,
                        return_stored=False,
                        dimension_separator="/",
                        **kwargs,
                    )
        else:
            if isinstance(progress, NgffProgressCallback):
                progress.add_callback_task(
                    f"[green]Writing scale {index+1} of {nscales}"
                )
            arr = _prep_for_to_zarr(store, arr)
            dask.array.to_zarr(
                arr,
                store,
                component=path,
                overwrite=False,
                compute=True,
                return_stored=False,
                dimension_separator="/",
                **kwargs,
            )

        # Minimize task graph depth
        if (
            index > 1
            and index < nscales - 2
            and multiscales.scale_factors
            and multiscales.method
            and multiscales.chunks
            and multiscales.scale_factors
        ):
            for callback in image.computed_callbacks:
                callback()
            image.computed_callbacks = []

            image.data = dask.array.from_zarr(store, component=path)
            next_multiscales_factor = multiscales.scale_factors[index]
            if isinstance(next_multiscales_factor, int):
                next_multiscales_factor = (
                    next_multiscales_factor // multiscales.scale_factors[index - 1]
                )
            else:
                updated_factors = {}
                for d, f in next_multiscales_factor.items():
                    updated_factors[d] = f // multiscales.scale_factors[index - 1][d]
                next_multiscales_factor = updated_factors

            next_multiscales = to_multiscales(
                image,
                scale_factors=[
                    next_multiscales_factor,
                ],
                method=multiscales.method,
                chunks=multiscales.chunks,
                progress=progress,
                cache=False,
            )
            multiscales.images[index + 1] = next_multiscales.images[1]
            next_image = next_multiscales.images[1]
        elif index < nscales - 1:
            next_image = multiscales.images[index + 1]

    for image in multiscales.images:
        for callback in image.computed_callbacks:
            callback()
        image.computed_callbacks = []

    zarr.consolidate_metadata(store)
