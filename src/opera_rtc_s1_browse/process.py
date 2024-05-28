"""
opera-rtc-s1-browse processing
"""

import argparse
import logging
from pathlib import Path

from opera_rtc_s1_browse import __version__


log = logging.getLogger(__name__)


def process_opera_rtc_s1_browse(greeting: str = 'Hello world!') -> Path:
    """Create a greeting product

    Args:
        greeting: Write this greeting to a product file (Default: "Hello world!" )
    """
    log.debug(f'Greeting: {greeting}')
    product_file = Path('greeting.txt')
    product_file.write_text(greeting)
    return product_file


def main():
    """process_opera_rtc_s1_browse entrypoint"""
    parser = argparse.ArgumentParser(
        prog='process_opera_rtc_s1_browse',
        description=__doc__,
    )
    parser.add_argument('--greeting', default='Hello world!', help='Write this greeting to a product file')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    process_opera_rtc_s1_browse(**args.__dict__)


if __name__ == '__main__':
    main()
