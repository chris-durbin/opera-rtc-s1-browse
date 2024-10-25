# opera-rtc-s1-browse

A tool for creating OPERA RTC Sentinel-1 browse images for [NASA Worldview](https://worldview.earthdata.nasa.gov).

## Usage
Once installed (see below for details) you can run the tool using the command:
```bash
create_browse OPERA_L2_RTC-S1_T035-073251-IW2_20240113T020816Z_20240113T113128Z_S1A_30_v1.0_VV.tif OPERA_L2_RTC-S1_T035-073251-IW2_20240113T020816Z_20240113T113128Z_S1A_30_v1.0_VH.tif
```

To explore the available options, run:
```
$ create_browse --help
usage: create_browse [-h] co_pol_path cross_pol_path

positional arguments:
  co_pol_path     Path to the co-polarization (VV) RTC image
  cross_pol_path  Path to the cross-polarization (VH) RTC image

options:
  -h, --help      show this help message and exit
```

## Setup
### Installation
1. Ensure that conda is installed on your system (we recommend using [mambaforge](https://github.com/conda-forge/miniforge#mambaforge) to reduce setup times).
2. Download a local version of the `opera-rtc-s1-browse` repository (`git clone git@github.com:ASFHyP3/opera-rtc-s1-browse.git`)
3. In the base directory for this project, call `mamba env create -f environment.yml` to create your Python environment and activate it (`mamba activate opera-rtc-s1-browse`)
4. Install the opera-rtc-s1-browse package in your conda environment via `python -m pip install -e ".[develop]"`

To run all commands in sequence use:
```bash
git clone git@github.com:ASFHyP3/opera-rtc-s1-browse.git
cd opera-rtc-s1-browse
mamba env create -f environment.yml
mamba activate opera-rtc-s1-browse
python -m pip install -e ".[develop]"
```

## License
`opera-rtc-s1-browse` is licensed under the BSD 2-Clause License. See the LICENSE file for more details.

## Contributing
Contributions to this project are welcome! If you would like to contribute, please submit a pull request on the GitHub repository.

## Contact Us
Want to talk about `opera-rtc-s1-browse`? We would love to hear from you!

Found a bug? Want to request a feature?
[open an issue](https://github.com/ASFHyP3/opera-rtc-s1-browse/issues/new)

General questions? Suggestions? Or just want to talk to the team?
[chat with us on gitter](https://gitter.im/ASFHyP3/community)
