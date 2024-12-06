import itertools
from typing import Any, Iterator, TYPE_CHECKING

import numpy as np
from accelerate import find_executable_batch_size
from napari.layers import Image, Shapes
from napari.qt.threading import thread_worker
from napari.utils import notifications
from skimage.transform import resize

if TYPE_CHECKING:
    import cellpose


def get_image_roi(image: np.ndarray, rois: list[np.ndarray]) -> Iterator[tuple[np.ndarray, tuple[int, int]]]:
    """
    Get ROI from image

    :param image: Image data (np.ndarray)
    :param rois: List of ROI coordinates (list[np.ndarray])

    :returns:
        Iterator of tuples containing image ROIs (np.ndarray) and ROI offsets (tuple[int, int])
    """

    for coords in rois:

        minr, minc = np.min(coords, axis=0).astype(int)
        maxr, maxc = np.max(coords, axis=0).astype(int)

        yield image[minr:maxr, minc:maxc], (minr, minc)


def estimate_diameter(image: np.ndarray, model_type: str, use_gpu: bool) -> np.ndarray[Any, np.dtype[np.float16]]:
    """
    Estimate diameters using cellpose size models.

    :param image: Image data (np.ndarray)
    :param model_type: Cellpose model type (str)
    :param use_gpu: whether to use gpu acceleration (bool)

    :returns:
        Estimated diameter (np.ndarray[Any, np.dtype[np.float16]])
    """

    from cellpose import models
    model = models.Cellpose(model_type=model_type, gpu=use_gpu)
    diameter = model.sz.eval(image, channels=[0,0], channel_axis=-1)[0]
    diameter = np.round(diameter, 2)

    del model
    notifications.show_info(f"Estimated Diameter (px): {diameter}")
    return diameter


def get_image_patches(
    image: np.ndarray,
    image_patch_dim: tuple[int, int],
    split_image_threshold: tuple[float, float],
) -> Iterator[tuple[np.ndarray, tuple[int, int]]]:
    """
    Split image into N patches for processing.

    :param image: 2D image array (np.ndarray)
    :param image_patch_dim: Dimension of the image patches (tuple[int, int])
    :param split_image_threshold:
        At which scale relative to the image_patch_dim should images be split (tuple[float, float]).
        For (1.5, 1.5) images are split if their height and width are 1.5X larger than `image_patch_dim`.

    :returns:
        Iterator over image patches as numpy arrays.
    """

    image_height, image_width = image.shape
    target_image_height, target_image_width = image_patch_dim
    scale = (
        image_height / target_image_height,
        image_width / target_image_width,
    )
    if scale <= split_image_threshold:
        yield image, (0, 0)
    else:
        notifications.show_info("Processing image in batches...")
        for i, j in itertools.product(
            range(0, image_height, target_image_height),
            range(0, image_width, target_image_width),
        ):
            yield image[i : i + target_image_height, j : j + target_image_width], (i, j)


def count_objects(image: Image, rois: Shapes | None, model_type: str, restore_type: str | None, use_gpu: bool, batch_size: int, diameter: float):
    """
    Count objects in an image, or selected ROIs is available.

    :param image: Image layer  (napari.layers.Image)
    :param rois: ROI layer if selected (napari.layers.Shapes | None)
    :param model_type: Segmentation model type (str)
    :param restore_type: Image restoration model type (str)
    :param use_gpu: Whether to use GPU acceleration (bool)
    :param diameter: Object diameter (float)

    :returns:
        Segmentation masks (napari.layers.Labels).
        Total number of objects can be accessed with masks.max()
    """

    if restore_type is None:
        from cellpose import models
        segmentation_model = models.Cellpose(model_type=model_type, gpu=use_gpu)
    else:
        from cellpose import denoise
        segmentation_model = denoise.CellposeDenoiseModel(model_type=model_type, restore_type=restore_type, gpu=use_gpu)

    @find_executable_batch_size(starting_batch_size=batch_size)
    def compute_masks(batch_size, model=None):
        masks = list()
        mask_offsets = list()
        count = 0
        if rois is None:
            masks0, _, _, _ = model.eval(image.data, channels=[0,0], diameter=diameter, batch_size=batch_size)
            del model
            return [masks0], [(0, 0)], masks0.max()
        else:
            # image_rois, offsets = get_image_roi(image.data, rois.data)
            # raw_masks, _, _, _ = model.eval(image_rois, channels=[0,0], diameter=diameter, batch_size=batch_size)
            # # resize masks
            #
            # del model
            # return raw_masks, list(offsets), count

            for idx, coords in enumerate(rois.data):
                min_row, min_col = np.min(coords, axis=0).astype(int)
                max_row, max_col = np.max(coords, axis=0).astype(int)
                #image_roi = image.data[min_row:max_row, min_col:max_col]
                image_roi, roi_offset = get_image_roi(image.data, coords)
                raw_masks, _, _, _ = model.eval(image_roi, channels=[0, 0], diameter=diameter, batch_size=batch_size)
                resized_masks = resize(raw_masks, image_roi.shape, order=0, preserve_range=True, anti_aliasing=False).astype(int)
                mask_offsets.append(roi_offset)
                count += resized_masks.max()
                masks.append(resized_masks)

        return masks, mask_offsets, count

    masks, mask_offsets, count = compute_masks(model=segmentation_model)
    return masks, mask_offsets, count
