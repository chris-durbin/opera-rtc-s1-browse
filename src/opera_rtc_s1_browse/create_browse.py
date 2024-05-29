"""
opera-rtc-s1-browse processing
"""

import argparse
import logging
from pathlib import Path
from typing import Optional

import asf_search
import numpy as np
from osgeo import gdal

from opera_rtc_s1_browse.auth import get_earthdata_credentials


log = logging.getLogger(__name__)
gdal.UseExceptions()


def download_data(granule: str, working_dir: Path):
    result = asf_search.granule_search([granule])[0]
    urls = result.properties['additionalUrls']
    urls.append(result.properties['url'])

    co_pol = [x for x in urls if 'VV' in x]
    if not co_pol:
        raise ValueError('No co-pol found in granule.')
    co_pol = co_pol[0]

    cross_pol = [x for x in urls if 'VH' in x]
    if not cross_pol:
        raise ValueError('No cross-pol found in granule.')
    cross_pol = cross_pol[0]

    username, password = get_earthdata_credentials()
    session = asf_search.ASFSession().auth_with_creds(username, password)
    asf_search.download_urls(urls=[co_pol, cross_pol], path=working_dir, session=session)

    co_pol_path = working_dir / Path(co_pol).name
    cross_pol_path = working_dir / Path(cross_pol).name
    return co_pol_path, cross_pol_path


def normalize_image_band(band_image: np.ndarray) -> np.ndarray:
    """Function to normalize a browse image band.
    Taken from OPERA-ADT/RTC.

    Args:
        band_image: Input image to be normalized.

    Returns
        The normalized image
    """
    min_percentile = 3
    max_percentile = 97
    vmin = np.nanpercentile(band_image, min_percentile)
    vmax = np.nanpercentile(band_image, max_percentile)

    # gamma correction: 0.5
    is_not_negative = band_image - vmin >= 0
    is_negative = band_image - vmin < 0
    band_image[is_not_negative] = np.sqrt((band_image[is_not_negative] - vmin) / (vmax - vmin))
    band_image[is_negative] = 0
    band_image[np.isnan(band_image)] = 0
    band_image = np.round(np.clip(band_image, 0, 1) * 255).astype(np.uint8)
    return band_image


def create_browse_array(co_pol_array, cross_pol_array):
    co_pol_nodata = ~np.isnan(co_pol_array)
    co_pol = normalize_image_band(co_pol_array)

    cross_pol_nodata = ~np.isnan(cross_pol_array)
    cross_pol = normalize_image_band(cross_pol_array)

    no_data = (np.logical_and(co_pol_nodata, cross_pol_nodata) * 255).astype(np.uint8)
    browse_image = np.stack([co_pol, cross_pol, co_pol, no_data], axis=-1)
    return browse_image


def create_browse_image(co_pol_path: Path, cross_pol_path: Path, working_dir: Path) -> Path:
    """Create browse images for an OPERA S1 RTC granule."""
    co_pol_ds = gdal.Open(str(co_pol_path))
    co_pol = co_pol_ds.GetRasterBand(1).ReadAsArray()

    cross_pol_ds = gdal.Open(str(cross_pol_path))
    cross_pol = cross_pol_ds.GetRasterBand(1).ReadAsArray()

    browse_array = create_browse_array(co_pol, cross_pol)

    tmp_browse_path = working_dir / f'{co_pol_path.stem}_tmp.tif'
    driver = gdal.GetDriverByName('GTiff')
    browse_ds = driver.Create(str(tmp_browse_path), browse_array.shape[1], browse_array.shape[0], 4, gdal.GDT_Byte)
    browse_ds.SetGeoTransform(co_pol_ds.GetGeoTransform())
    browse_ds.SetProjection(co_pol_ds.GetProjection())
    for i in range(4):
        browse_ds.GetRasterBand(i + 1).WriteArray(browse_array[:, :, i])

    co_pol_ds = None
    cross_pol_ds = None
    browse_ds = None

    browse_path = working_dir / f'{co_pol_path.stem}_browse.tif'
    gdal.Warp(
        browse_path,
        tmp_browse_path,
        dstSRS='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs',
        xRes=2.74658203125e-4,
        yRes=2.74658203125e-4,
        format='GTiff',
        creationOptions=['COMPRESS=LZW', 'TILED=YES'],
    )
    tmp_browse_path.unlink()
    return browse_path


def create_browse_and_upload(
    granule: str,
    earthdata_username: str = None,
    earthdata_password: str = None,
    bucket: str = None,
    bucket_prefix: str = '',
    working_dir: Optional[Path] = None,
) -> Path:
    """Create browse images for an OPERA S1 RTC granule.

    Args:
        granule: The granule to create browse images for.
        earthdata_username: Username for NASA's EarthData.
        earthdata_password: Password for NASA's EarthData.
        bucket: AWS S3 bucket for upload the final product(s).
        bucket_prefix: Add a bucket prefix to product(s).
        working_dir: Working directory to store intermediate files.
    """
    if working_dir is None:
        working_dir = Path.cwd()

    # download_data(granule, working_dir)
    co_pol_path = working_dir / f'{granule}_VV.tif'
    cross_pol_path = working_dir / f'{granule}_VH.tif'
    create_browse_image(co_pol_path, cross_pol_path, working_dir)
    return None


def main():
    """opera_rtc_s1_browse entrypoint

    Example:
        create_browse OPERA_L2_RTC-S1_T035-073251-IW2_20240113T020816Z_20240113T113128Z_S1A_30_v1.0
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--earthdata-username', default=None, help="Username for NASA's EarthData")
    parser.add_argument('--earthdata-password', default=None, help="Password for NASA's EarthData")
    parser.add_argument('--bucket', help='AWS S3 bucket HyP3 for upload the final product(s)')
    parser.add_argument('--bucket-prefix', default='', help='Add a bucket prefix to product(s)')
    parser.add_argument('granule', type=str, help='OPERA S1 RTC granule to create a browse imagery for.')
    args = parser.parse_args()

    create_browse_and_upload(**args.__dict__)


if __name__ == '__main__':
    main()
