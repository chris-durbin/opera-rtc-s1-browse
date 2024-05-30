"""
opera-rtc-s1-browse processing
"""
import logging

from opera_rtc_s1_browse import create_browse


def main():
    """
    Entrypoint for opera_rtc_s1_browse
    """
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO
    )
    create_browse.main()


if __name__ == '__main__':
    main()
