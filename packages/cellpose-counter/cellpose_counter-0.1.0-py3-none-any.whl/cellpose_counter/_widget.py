from typing import TYPE_CHECKING

from magicgui.widgets import (
    CheckBox,
    Combobox,
    Container,
    LineEdit,
    PushButton,
    create_widget,
)
from napari.utils import notifications
from napari.layers import Labels, Points

if TYPE_CHECKING:
    import napari
    import numpy as np



CP_MODELS = ["nuclei", "cyto3", "cyto2", "cyto"]
RESTORE_MODELS = [
    "denoise_nuclei",
    "deblur_nuclei",
    "upsample_nuclei",
    "oneclick_nuclei",
    "denoise_cyto3",
    "deblur_cyto3",
    "upsample_cyto3",
    "oneclick_cyto3",
    "denoise_cyto2",
    "deblur_cyto2",
    "upsample_cyto2",
    "oneclick_cyto2",
    "None"
]


class Counter(Container):
    """
    Counter widget for Napari

    count cells and nuclei from images using cellpose models.
    """
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer
        # add a default ROI layer
        self._viewer.add_shapes(
            name="ROI",
            face_color="white",
            edge_color="red",
            edge_width=3,
            opacity=0.20,
            blending="additive",
        )

        # create widgets
        self._image_layer_combo = create_widget(
            label="Image Layer", annotation="napari.layers.Image"
        )
        self._roi_layer_combo = create_widget(
            label="ROI Layer", annotation="napari.layers.Shapes"
        )
        self._cp_models = Combobox(label="Cellpose Model", value="nuclei", choices=CP_MODELS)
        self._restore_models = Combobox(label="Restore Model", value="oneclick_nuclei", choices=RESTORE_MODELS)
        self._diam = LineEdit(label="Diameter", value="17")
        self._use_gpu = CheckBox(text="Use GPU", value=True)
        self._diam_estimate_btn = PushButton(label="Estimate Diameter")
        self._get_count_btn = PushButton(text="Get Initial Count")
        self._count_display = LineEdit(label="Total Count", value="0")
        self._manual_count_layer = create_widget(label="Manual Counts", annotation="napari.layers.Points")
        self._update_count_btn = PushButton(text="Update Count")

        # callbacks
        self._diam_estimate_btn.changed.connect(self._estimate_diam)
        self._get_count_btn.changed.connect(self._get_count)
        self._update_count_btn.changed.connect(self._update_count)

        # append into/extend the container with widgets
        self.extend([
            self._image_layer_combo,
            self._roi_layer_combo,
            self._cp_models,
            self._restore_models,
            self._diam,
            self._use_gpu,
            self._diam_estimate_btn,
            self._get_count_btn,
            self._count_display,
            self._manual_count_layer,
            self._update_count_btn
        ])


    def _display_diam(self, diam: float):
        """Purely for updating the diameter value"""
        self._diam.value = diam


    def _display_count(self, result: tuple[list["np.ndarray"], list[tuple[int, int]], float]):
        """Display count and add segmentation results"""
        masks, mask_offsets, count = result
        self._count_display.value = count
        for idx, (mask, mask_offset) in enumerate(zip(masks, mask_offsets)):
            self._viewer.add_labels(mask, translate=mask_offset, name=f"Masks-[{idx}]")

        self._viewer.add_points(name="Manual Counts", size=float(self._diam.value))
        notifications.show_info("Updated total count.")


    def _estimate_diam(self):
        """Estimate diameter of objects with Cellpose size models"""
        image_layer = self._image_layer_combo.value
        if image_layer is None:
            notifications.show_error("No image selected.")
            return

        from .counter import estimate_diameter
        estimate_diam_worker = estimate_diameter(image_layer.data, self._cp_models.value, self._use_gpu.value)
        estimate_diam_worker.returned.connect(self._display_diam)
        estimate_diam_worker.start()


    def _get_count(self):
        """Count cells/nuclei inside an ROI for a given image using cellpose"""
        notifications.show_info("Counting objects...")
        image = self._image_layer_combo.value
        roi = self._roi_layer_combo.value

        if image is None:
            notifications.show_error("No image found in viewer.")
            return

        from .counter import count_objects
        count_objects_worker = count_objects(
            image,
            roi,
            self._cp_models.value,
            self._restore_models.value,
            self._use_gpu.value,
            float(self._diam.value)
        )
        count_objects_worker.returned.connect(self._display_count)
        count_objects_worker.start()


    def _update_count(self):
        """Update total number of cells from automatic and manual counting"""
        count = 0
        for layer in self._viewer.layers:
            if "Masks" in layer.name and isinstance(layer, Labels):
                count += layer.data.max()


        points_layer = self._viewer.layers["Manual Counts"]
        if points_layer is not None:
            count += len(points_layer.data)

        self._count_display.value = count
        notifications.show_info("Total count updated successfully.")



