
from cellpose_counter._widget import (
    Counter,
)

SMALL_IMAGE = "src/cellpose_counter/_tests/data/image_small_512.tif"
LARGE_IMAGE = "src/cellpose_counter/_tests/data/image_large_1024.tif"

# make_napari_viewer is a pytest fixture that returns a napari viewer object
# you don't need to import it, as long as napari is installed
# in your testing environment
def test_diameter_estimate(make_napari_viewer):
    viewer = make_napari_viewer()
    image_layer = viewer.open(SMALL_IMAGE)
    counter = Counter(viewer)
    counter._use_gpu.value = False

    # because we saved our widgets as attributes of the container
    # we can set their values without having to "interact" with the viewer
    #counter._image_layer_combo.value = image_layer

    # this allows us to run our functions directly and ensure
    # correct results
    counter._estimate_diam()
    assert counter._diam.value == 7.0
    # assert len(viewer.layers) == 2


# capsys is a pytest fixture that captures stdout and stderr output streams
# def test_example_q_widget(make_napari_viewer, capsys):
#     # make viewer and add an image layer using our fixture
#     viewer = make_napari_viewer()
#     viewer.add_image(np.random.random((100, 100)))
#
#     # create our widget, passing in the viewer
#     my_widget = ExampleQWidget(viewer)
#
#     # call our widget method
#     my_widget._on_click()
#
#     # read captured output and check that it's as we expected
#     captured = capsys.readouterr()
#     assert captured.out == "napari has 1 layers\n"
