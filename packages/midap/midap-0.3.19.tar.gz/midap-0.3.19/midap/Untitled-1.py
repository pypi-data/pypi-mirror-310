
from pathlib import Path

from midap.utils import get_inheritors
from midap.segmentation import *
from midap.segmentation import base_segmentator
from midap.apps import segment_cells

# define variables
postprocessing = False
network_name = None
img_threshold = 255
segmentation_class = "UNetSegmentation"
path_midap = "/Users/franziskaoschmann/Documents/midap"

if segmentation_class == "OmniSegmentation":
    path_model_weights = Path(path_midap).joinpath(
        "model_weights", "model_weights_omni"
    )
else:
    path_model_weights = Path(path_midap).joinpath(
        "model_weights", "model_weights_legacy"
    )

# get the right subclass
class_instance = None
for subclass in get_inheritors(base_segmentator.SegmentationPredictor):
    if subclass.__name__ == segmentation_class:
        class_instance = subclass

# throw an error if we did not find anything
if class_instance is None:
    raise ValueError(f"Chosen class does not exist: {segmentation_class}")

# get the Predictor
pred = class_instance(
    path_model_weights=path_model_weights,
    postprocessing=postprocessing,
    model_weights=network_name,
    img_threshold=img_threshold,
    jupyter=False,
)