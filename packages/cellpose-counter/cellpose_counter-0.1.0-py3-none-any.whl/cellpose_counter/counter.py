from typing import Any

import numpy as np
from napari.layers import Image, Shapes
from napari.qt.threading import thread_worker
from napari.utils import notifications
from skimage.transform import resize


@thread_worker
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


@thread_worker
def count_objects(image: Image, rois: Shapes | None, model_type: str, restore_type: str | None, use_gpu: bool, diameter: float):
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

    masks = list()
    mask_offsets = list()
    target_shape = tuple()
    count = 0
    if rois is None:
        target_shape = image.data.shape
        masks0, _, _, _ = segmentation_model.eval(image.data, channels=[0,0], diameter=diameter)
        masks.append(masks0)
        mask_offsets.append((0, 0))
        count += masks0.max()
    else:
        for idx, coords in enumerate(rois.data):
            min_row, min_col = np.min(coords, axis=0).astype(int)
            max_row, max_col = np.max(coords, axis=0).astype(int)
            image_roi = image.data[min_row:max_row, min_col:max_col]
            raw_masks, _, _, _ = segmentation_model.eval(image_roi, channels=[0, 0], diameter=diameter,)
            resized_masks = resize(raw_masks, image_roi.shape, order=0, preserve_range=True, anti_aliasing=False).astype(int)
            mask_offsets.append((min_row, min_col))
            count += resized_masks.max()
            masks.append(resized_masks)

    del segmentation_model
    return masks, mask_offsets, count
