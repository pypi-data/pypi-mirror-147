import numpy as np
import pytest
from PIL import Image

from pierogis.ingredients import Resize


@pytest.fixture
def array():
    return np.asarray([[[200, 200, 200], [30, 30, 30]],
                       [[130, 130, 130], [60, 60, 60]],
                       [[20, 40, 100], [10, 20, 200]]]).astype(np.dtype('uint8'))


def test_cook_width(array):
    """
    provide only width
    """
    width = 100
    aspect = array.shape[0] / array.shape[1]

    resize = Resize(width=width)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == width
    assert cooked_array.shape[1] == int(width / aspect)


def test_cook_height(array):
    """
    provide only height
    """
    height = 100
    aspect = array.shape[0] / array.shape[1]

    resize = Resize(height=height)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == int(aspect * height)
    assert cooked_array.shape[1] == height


def test_cook_width_height(array):
    """
    provide height and width
    """
    width = 200
    height = 100

    resize = Resize(width=width, height=height)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == width
    assert cooked_array.shape[1] == height


def test_cook_width_scale(array):
    """
    provide width and scale
    """
    width = 100
    scale = 2
    aspect = array.shape[0] / array.shape[1]

    resize = Resize(width=width, scale=scale)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == scale * width
    assert cooked_array.shape[1] == int(scale * width / aspect)


def test_cook_height_scale(array):
    """
    provide height and scale
    """
    height = 100
    scale = 2
    aspect = array.shape[0] / array.shape[1]

    resize = Resize(height=height, scale=scale)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == int(height * aspect * scale)
    assert cooked_array.shape[1] == height * scale


def test_cook_scale(array):
    """
    provide only scale
    """
    scale = 2

    resize = Resize(scale=2)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == array.shape[0] * scale
    assert cooked_array.shape[1] == array.shape[1] * scale


def test_cook_height_width_scale(array):
    """
    provide height, width, and scale
    """
    width = 100
    height = 200
    scale = 2

    resize = Resize(width=width, height=height, scale=scale)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == width * scale
    assert cooked_array.shape[1] == height * scale


def test_cook_height_width_scale_resample(array):
    """
    provide height, width, scale, and resample
    """
    width = 100
    height = 200
    scale = 2

    resize = Resize(width=width, height=height, scale=scale, resample=Image.BILINEAR)
    cooked_array = resize.cook(array)

    assert cooked_array.shape[0] == width * scale
    assert cooked_array.shape[1] == height * scale
