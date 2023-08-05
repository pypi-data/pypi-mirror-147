from typing import Dict, Any
import sys
from pathlib import Path
import datetime
import gzip
import lzma
import json
from tempfile import gettempdir
from uuid import uuid4
from asyncio import to_thread

# Package imports
from target.logger import get_logger

LOGGER = get_logger()


def config_file(config_path: str, datetime_format: Dict = {
        'date_time_format': ''}) -> Dict:

    config: Dict[str, Any] = {
        'path_template': '{stream}-{date_time%s}.json' % datetime_format['date_time_format'],
        'memory_buffer': 64e6
    }

    with open(config_path) as input_file:
        config.update(json.load(input_file))

    config['path_template'] = config['path_template'] \
        .replace('{date_time}', '{date_time%s}' % datetime_format['date_time_format'])

    # NOTE: Use the system specific temp directory if no custom work_dir provided
    work_path = Path(config.get('work_dir', gettempdir())).expanduser()
    config['work_path'] = work_path

    timezone = datetime.timezone(datetime.timedelta(hours=config['timezone_offset'])) if config.get('timezone_offset') is not None else None
    config['date_time'] = datetime.datetime.now(timezone)

    return config


def config_compression(config_default: Dict) -> Dict:
    config: Dict[str, Any] = {
        'compression': 'none'
    }
    config.update(config_default)

    if f"{config.get('compression')}".lower() == 'gzip':
        config['open_func'] = gzip.open
        config['path_template'] = config['path_template'] + '.gz'

    elif f"{config.get('compression')}".lower() == 'lzma':
        config['open_func'] = lzma.open
        config['path_template'] = config['path_template'] + '.xz'

    elif f"{config.get('compression')}".lower() in {'', 'none'}:
        config['open_func'] = open

    else:
        raise NotImplementedError(
            "Compression type '{}' is not supported. "
            "Expected: 'none', 'gzip', or 'lzma'"
            .format(f"{config.get('compression')}".lower()))

    return config


def get_relative_path(stream: str, config: Dict[str, Any], date_time: datetime.datetime) -> str:
    '''Creates and returns an S3 key for the stream

    Parameters
    ----------
    stream : str
        incoming stream name that is written in the file
    config : dict
        configuration dictionary
    date_time : datetime
        Date used in the path template

    Returns
    -------
    out : ``str``
        The formatted path.
    '''

    # NOTE: Replace dynamic tokens
    key = config['path_template'].format(stream=stream, date_time=date_time, uuid=uuid4())

    prefix = config.get('key_prefix', '')
    return str(Path(key).parent / f'{prefix}{Path(key).name}') if prefix else key


def set_schema_file(stream: str, config: Dict, file_data: Dict) -> None:
    # NOTE: get the file key. Persistent array data storage.
    if stream not in file_data:
        relative_path = get_relative_path(stream=stream, config=config, date_time=config['date_time'])
        file_data[stream] = {
            'stream': stream,
            'relative_path': relative_path,
            'absolute_path': config['work_path'] / relative_path,
            'file_data': []}

        file_data[stream]['absolute_path'].unlink(missing_ok=True)
        file_data[stream]['absolute_path'].parent.mkdir(parents=True, exist_ok=True)


async def save_jsonl_file(message_type: str, config: Dict[str, Any], file_data: Dict) -> None:
    # NOTE: write the lines into the temporary file when received data over 64Mb default memory buffer
    if (sys.getsizeof(file_data['file_data']) >= config.get('memory_buffer', 0) or message_type is None) \
       and any(file_data['file_data']):
        with config['open_func'](file_data['absolute_path'], 'at', encoding='utf-8') as output_file:
            await to_thread(output_file.writelines, (json.dumps(record) + '\n' for record in file_data['file_data']))

        del file_data['file_data'][:]
        LOGGER.debug("'{}' file saved using open_func '{}'".format(file_data['absolute_path'], config['open_func'].__name__))
