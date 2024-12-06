
import numpy as np
from skimage import io

from cellpose_counter.counter import estimate_diameter, get_image_roi

SMALL_IMAGE_PATH = "src/cellpose_counter/_tests/data/image_small_512.tif"
LARGE_IMAGE_PATH = "src/cellpose_counter/_tests/data/image_large_1024.tif"

SMALL_IMAGE = io.imread(SMALL_IMAGE_PATH, as_gray=True)
LARGE_IMAGE = io.imread(LARGE_IMAGE_PATH, as_gray=True)

SMALL_ROI_LAYER = [np.array([[0.0, 256.0], [0.0, 512.0], [256.0, 512.0], [256.0, 256.0]])]
LARGE_ROI_LAYER = [np.array([[0.0, 0.0], [0.0, 1024.0], [1024.0, 1024.0], [1024.0, 0.0]])]

# Targets
SMALL_IMAGE_DIAMETER = np.float64(7.0)
SMALL_ROI_SHAPE = (
    (SMALL_ROI_LAYER[0][1][1] - SMALL_ROI_LAYER[0][0][1]).astype(int),
    (SMALL_ROI_LAYER[0][2][1] - SMALL_ROI_LAYER[0][3][1]).astype(int),
)

def test_roi_extraction():
    roi, _ = get_image_roi(SMALL_IMAGE, SMALL_ROI_LAYER[0])
    assert roi.shape == SMALL_ROI_SHAPE

def test_estimate_diameter():
    model_type = "nuclei"
    use_gpu = False # for testing
    diam = estimate_diameter(SMALL_IMAGE, model_type, use_gpu)
    assert diam == SMALL_IMAGE_DIAMETER


