"""Visualization routines for MedicalVolume."""
import copy
from copy import deepcopy
from typing import Mapping, Sequence, Tuple, Union

import numpy as np
import seaborn as sns

from dosma.core.med_volume import MedicalVolume

# SamplesPerPixel, PhotometricIntepretation, BitsAllocated, BitsStored, HighBit
_COLORIZATION_MAP = {0x00280004: "RGB", 0x00280002: 3, 0x00280100: 8, 0x00280101: 8, 0x00280102: 7}
_RGB_FLOAT = Tuple[float, float, float]


def colorize_mask(
    seg: MedicalVolume,
    is_onehot: bool,
    palette: Union[str, Sequence[_RGB_FLOAT], Mapping[int, _RGB_FLOAT]] = None,
    bg_value: int = 0,
    include_bg: bool = False,
):
    """Colorizes a segmentation mask.

    Args:
        seg (dm.MedicalVolume): A categorical segmentation mask.
          This can either be one-hot encoded where the last dimension is the
          category dimension (preferred) or it can be a categorical tensor.
        is_onehot (bool): Whether the segmentation mask is one-hot encoded.
        palette (str | Sequence | Dict[int, Tuple[int|float]]): List of colors
          to use for segmentation labels. Each color should be a tuple of
          float RGB values (see :cls:`seaborn.color_palette`). If it is a string,
          it should correspond to a seaborn palette. Note, seaborn must be installed
          to use this functionality.
        bg_value (int): Value of background label if `seg` is categorical.
        include_bg (bool): Whether to include the background label in the overlay.

    Returns:
        dm.MedicalVolume: RGB-colorized segmentation
    """
    num_classes = int(seg.shape[-1] if is_onehot else seg.A.max() + int(include_bg))
    palette = "bright" if palette is None else copy.copy(palette)
    if isinstance(palette, str):
        palette = sns.color_palette(palette, n_colors=num_classes)
    if isinstance(palette, Sequence):
        for i in range(len(palette)):
            palette[i] = tuple(palette[i])

    ndim = seg.ndim if not is_onehot else seg.ndim - 1

    seg_colored = np.zeros(seg.shape[:ndim] + (3,), dtype=np.float32)
    for i in range(num_classes):
        if is_onehot:
            seg_colored[seg[..., i]] = palette[i]
        else:
            if i == bg_value:
                continue
            seg_colored[seg == i] = palette[i]
    seg_colored *= 255.0

    seg_colored = np.round(seg_colored).astype(np.uint8)
    seg_colored = seg._partial_clone(volume=seg_colored, headers=True)
    # Set dicom header values to be in accordance with Voxel decoding.
    for k, v in _COLORIZATION_MAP.items():
        seg_colored.set_metadata(k, v, force=True)

    return seg_colored


def overlay_mask(
    image: MedicalVolume,
    seg: MedicalVolume,
    alpha: float = 0.7,
):
    """Overlay segmentation mask onto the image with alpha-blending.

    Args:
        image (dm.MedicalVolume): Image to overlay on. Must be a grayscale image.
        seg (dm.MedicalVolume): Segmentation mask to overlay.
          This can either be one-hot encoded where the last dimension is the
          category dimension (preferred) or it can be a categorical tensor.
        alpha (float): Alpha value for blending.

    Returns:
        dm.MedicalVolume: Image with segmentation overlay.
    """
    for k, v in _COLORIZATION_MAP.items():
        if seg.get_metadata(k, type(v), None) != v:
            raise ValueError("Segmentation mask must be colorized using `colorize_mask`.")
    seg = seg.reformat_as(image)
    if seg.shape[:-1] != image.shape:
        raise ValueError("Segmentation mask must have same spatial dimensions as image.")

    img_arr = image.A.astype(np.float32)
    img_arr = (img_arr - np.min(img_arr)) / (np.max(img_arr) - np.min(img_arr)) * 255.0
    img_arr = np.stack([img_arr] * 3, axis=-1)

    img_arr_colored = img_arr * (1 - alpha) + seg.A.astype(np.float32) * alpha
    img_arr_colored = np.where(seg.A == 0, img_arr, img_arr_colored)
    img_arr_colored = np.round(img_arr_colored).astype(np.uint8)
    image_colored = image._partial_clone(
        volume=img_arr_colored, headers=deepcopy(image.headers())[..., np.newaxis]
    )

    # Set dicom header values to be in accordance with Voxel decoding.
    for k, v in _COLORIZATION_MAP.items():
        image_colored.set_metadata(k, v, force=True)

    return image_colored
