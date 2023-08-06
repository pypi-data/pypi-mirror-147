__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import json
import logging
import pickle
import sys
from argparse import ArgumentParser
from bz2 import open as bzopen
from calendar import timegm
from datetime import date, datetime
from glob import glob
from gzip import open as gzopen
from lzma import open as xzopen
from os import environ
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Union

from pylast import LastFMNetwork, User, PyLastError

from media_tools.util.logging import setup_logging

MAX_RETRY_WAIT = 1024
OPEN_FUNCTIONS: Dict[str, Callable] = {
    'bz2': bzopen,
    'gz': gzopen,
    'xz': xzopen,
}
DUMP_PARAMS = {
    'json': dict(dump=json.dump, mode='wt', kwargs=dict(default=str)),
    'pickle': dict(dump=pickle.dump, mode='wb', kwargs={})
}


def parse():
    parser = ArgumentParser(
        description="Creates a pickle or JSON file from a last.fm user's data"
    )
    parser.add_argument(
        '-l', '--limit', type=int, default=None,
        help='Max. number of entries to request'
    )
    parser.add_argument(
        '-y', '--year', type=int, default=None,
        help='Year the data is requested for'
    )
    parser.add_argument(
        '-c', '--combine', action='store_true',
        help='Combine data sets present in current folder'
    )
    parser.add_argument(
        '-o', '--output', type=str, default=None,
        help='output file name'
    )
    args = parser.parse_args()
    return args


def from_datetime(convert_datetime: datetime) -> int:
    return timegm(convert_datetime.utctimetuple())


def year_range(year: Optional[int]) -> Dict[str, int]:
    start = None if year is None else from_datetime(datetime(year, 1, 1, 0, 0, 0))
    end = None if year is None else from_datetime(datetime(year, 12, 31, 23, 59, 59, 999999))
    return dict(time_from=start, time_to=end)


def start_year(user: User) -> int:
    return date.fromtimestamp(user.get_unixtime_registered()).year


def get_and_wait(
        values: Optional[List], function: Callable, wait_time: int, **kwargs
) -> Union[List[Any], Any]:
    if values is None:
        values = function(**kwargs)
        logging.info('waiting %ss', str(wait_time))
        sleep(wait_time)
    return values


def get_data(  # pylint: disable=too-many-arguments
        user: User, year: Optional[int], limit: Optional[int], wait_time: int = 0,
        tracks: Optional[List[str]] = None, loved: Optional[List[str]] = None,
        top_tracks: Optional[List[str]] = None
) -> Dict:
    logging.info("get_data(user=%s, year=%s, limit=%s, wait=%s)", user.name, year, limit, wait_time)
    year_dates = year_range(year)
    try:
        play_count = user.get_playcount()
        tracks = get_and_wait(tracks, user.get_recent_tracks, wait_time, limit=limit, **year_dates)
        loved = get_and_wait(loved, user.get_loved_tracks, wait_time, limit=limit)
        top_tracks = get_and_wait(top_tracks, user.get_top_tracks, wait_time, limit=limit)
        top_artists = get_and_wait(None, user.get_top_artists, wait_time, limit=limit)
        top_albums = get_and_wait(None, user.get_top_albums, wait_time, limit=limit)
        top_tags = user.get_top_tags(limit=limit)
        return dict(
            time=datetime.now(),
            play_count=play_count,
            tracks=tracks,
            loved=loved,
            top_tracks=top_tracks,
            top_artists=top_artists,
            top_albums=top_albums,
            top_tags=top_tags,
        )
    # pylast has a feature to deal with rate limiting, but it doesn't seem to work reliably
    except PyLastError as error:
        logging.info("%s: %s", type(error).__name__, str(error))
        if wait_time <= MAX_RETRY_WAIT:
            next_wait_time = 1 if wait_time == 0 else 2 * wait_time
            logging.warning("%s, retrying with %ss wait time", type(error).__name__, next_wait_time)
            return get_data(
                user, year, limit, next_wait_time,
                tracks=tracks, loved=loved, top_tracks=top_tracks
            )
        logging.error('Rate limiting still active after %ss - giving up', MAX_RETRY_WAIT)
        raise


def combine_data() -> None:
    separate_user_data = {}
    user_data = {}
    for filename in glob('backup_lastfm_20??.pickle'):
        with open(filename, 'rb') as file:
            separate_user_data[filename] = pickle.load(file)
        user_data = separate_user_data[filename]
    user_data['tracks'] = sum([data['tracks'] for data in separate_user_data.values()], [])
    with open('backup_lastfm_all.pickle', 'wb') as backup_file:
        pickle.dump(user_data, backup_file)


def get_output_filename(year: Optional[int], filename: Optional[str]) -> str:
    if filename is None:
        year_string = "all" if year is None else str(year)
        filename = f'backup_lastfm_{year_string}.pickle.bz2'
    return filename


def get_and_dump(
        user: User, year: Optional[int], limit: Optional[int], filename: Optional[str] = None
):
    user_data = get_data(user, year, limit)
    backup_filename = get_output_filename(year, filename)
    dump(user_data, backup_filename)


def dump(user_data, backup_filename):
    filename_parts = backup_filename.split('.')
    extension = filename_parts[-1].lower()
    dump_format = extension if extension in DUMP_PARAMS else filename_parts[-2].lower()
    dump_params = DUMP_PARAMS.get(dump_format, DUMP_PARAMS['pickle'])
    dump_func = dump_params['dump']
    mode = dump_params['mode']
    kwargs = dump_params['kwargs']
    with OPEN_FUNCTIONS.get(extension, open)(backup_filename, mode) as backup_file:
        dump_func(user_data, backup_file, **kwargs)


def main() -> None:
    """
    Usage:
    $ export PYLAST_USERNAME=ENTER_YOURS_HERE
    $ export PYLAST_API_KEY=ENTER_YOURS_HERE
    $ export PYLAST_API_SECRET=ENTER_YOURS_HERE
    $ python backup_lastfm_data [options]
    """
    args = parse()
    setup_logging(args)

    if args.combine:
        combine_data()
        sys.exit(0)

    network = LastFMNetwork(
        api_key=environ['PYLAST_API_KEY'], api_secret=environ['PYLAST_API_SECRET']
    )
    user = network.get_user(environ['PYLAST_USERNAME'])

    if args.year is None:
        get_and_dump(user, None, args.limit, args.output)
    else:
        years = [args.year] if args.year else range(start_year(user), datetime.now().year)
        for year in years:
            get_and_dump(user, year, args.limit, args.output)


if __name__ == '__main__':
    main()
