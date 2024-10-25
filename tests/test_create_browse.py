from pathlib import Path

import numpy as np

from opera_rtc_s1_browse import create_browse


def test_normalize_image_array():
    input_array = np.array([0.0, 1.0, 2.0, np.nan])
    output_array = create_browse.normalize_image_array(input_array, 0, 2)
    assert np.array_equal(output_array, np.array([0, 128, 255, 0]))

    input_array = np.array([-10.0, -0.001, 0.0, 0.0001, 0.04, 2.0, 5.0, 9.999, 10.0, 10.001, 94.0, np.nan])
    output = create_browse.normalize_image_array(input_array, 0.0, 10.0)
    assert np.array_equal(output, np.array([0, 0, 0, 0, 1, 51, 128, 255, 255, 255, 255, 0]))

    output = create_browse.normalize_image_array(input_array, 1.0, 9.0)
    assert np.array_equal(output, np.array([0, 0, 0, 0, 0, 32, 128, 255, 255, 255, 255, 0]))


def test_create_browse_array():
    test_vv = np.array([[0, 0.0196, 0.10857025, 0.2704, np.nan]])
    test_vh = np.array([[np.nan, 0.0, 0.0025, 0.023716, 0.067081]])
    output_array = create_browse.create_browse_array(test_vv, test_vh)
    assert output_array.shape == (1, 5, 4)
    assert np.array_equal(output_array[:, :, 0], np.array([[0, 0, 127, 255, 0]]))
    assert np.array_equal(output_array[:, :, 1], np.array([[0, 0, 0, 127, 255]]))
    assert np.array_equal(output_array[:, :, 2], np.array([[0, 0, 127, 255, 0]]))
    assert np.array_equal(output_array[:, :, 3], np.array([[0, 255, 255, 255, 0]]))


def test_create_browse_image(tmp_path):
    datadir = Path(__file__).parent / 'data'

    co_pol_path = datadir / 'test_VV.tif'
    cross_pol_path = datadir / 'test_VH.tif'

    output_path = create_browse.create_browse_image(co_pol_path, cross_pol_path, tmp_path)
    assert output_path == tmp_path / 'test_rgb.tif'

    expected_image = datadir / 'test_rgb.tif'
    assert output_path.read_bytes() == expected_image.read_bytes()
