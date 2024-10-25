from pathlib import Path

import numpy as np

from opera_rtc_s1_browse import create_browse


def test_normalize_image_array():
    input_array = np.arange(0, 3) ** 2
    golden_array = np.array([0, 128, 255])
    output_array = create_browse.normalize_image_array(input_array, 0, 2)
    assert np.array_equal(output_array, golden_array)

    input_array = np.append(input_array.astype(float), np.nan)
    golden_array = np.append(golden_array, 0)
    output_array = create_browse.normalize_image_array(input_array, 0, 2)
    assert np.array_equal(output_array, golden_array)


def test_create_browse_array():
    vv_min, vv_max = 0.14, 0.52
    test_vv = np.array([[0, vv_min**2, ((vv_min + vv_max - 0.001) / 2) ** 2, vv_max**2, np.nan]])
    vh_min, vh_max = 0.05, 0.259
    test_vh = np.array([[np.nan, 0, vh_min**2, ((vh_min + vh_max - 0.001) / 2) ** 2, vh_max**2]])
    output_array = create_browse.create_browse_array(test_vv, test_vh)
    assert output_array.shape == (1, 5, 4)
    assert np.array_equal(output_array[:, :, 0], np.array([[0, 0, 127, 255, 0]]))
    assert np.array_equal(output_array[:, :, 1], np.array([[0, 0, 0, 127, 255]]))
    assert np.array_equal(output_array[:, :, 2], np.array([[0, 0, 127, 255, 0]]))
    assert np.array_equal(output_array[:, :, 3], np.array([[0, 255, 255, 255, 0]]))


def test_create_browse_image(tmp_path):
    datadir = Path.cwd() / 'tests' / 'data'

    co_pol_path = datadir / 'test_VV.tif'
    cross_pol_path = datadir / 'test_VH.tif'

    output_path = create_browse.create_browse_image(co_pol_path, cross_pol_path, tmp_path)
    assert output_path == tmp_path / 'test_rgb.tif'

    expected_image = datadir / 'test_rgb.tif'
    assert output_path.read_bytes() == expected_image.read_bytes()
