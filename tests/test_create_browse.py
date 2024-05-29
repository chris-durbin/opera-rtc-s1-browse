import numpy as np

from opera_rtc_s1_browse import create_browse


def test_normalize_image_array():
    input_array = np.arange(0, 10)
    golden_array = np.array([0, 75, 115, 145, 169, 191, 210, 227, 244, 255])
    output_array = create_browse.normalize_image_array(input_array)
    assert np.array_equal(output_array, golden_array)

    input_array = np.append(input_array.astype(float), np.nan)
    golden_array = np.append(golden_array, 0)
    output_array = create_browse.normalize_image_array(input_array)
    assert np.array_equal(output_array, golden_array)


def test_create_browse_arry():
    test_vv = np.array([[0, 1], [2, 3], [np.nan, np.nan]])
    test_vh = np.array([[np.nan, np.nan], [4, 5], [6, 7]])
    output_array = create_browse.create_browse_array(test_vv, test_vh)
    assert output_array.shape == (3, 2, 4)
    assert np.array_equal(output_array[:, :, 0], np.array([[0, 145], [210, 255], [0, 0]]))
    assert np.array_equal(output_array[:, :, 1], np.array([[0, 0], [0, 145], [210, 255]]))
    assert np.array_equal(output_array[:, :, 0], output_array[:, :, 2])
    assert np.array_equal(output_array[:, :, 3], np.array([[0, 0], [255, 255], [0, 0]]))
