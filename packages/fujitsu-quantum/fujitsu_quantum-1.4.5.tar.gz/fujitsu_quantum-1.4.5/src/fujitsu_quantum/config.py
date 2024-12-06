# (C) 2024 Fujitsu Limited

import dataclasses
from pathlib import Path

import pyjson5


@dataclasses.dataclass
class _Config:
    config_dir: str
    auth_pool_id: str
    auth_sdk_client_id: str
    api_base: str
    result_polling_interval: int
    retry_max_attempts: int


DEFAULT_RETRY_MAX_ATTEMPTS = 10


def load_config() -> _Config:
    config_dir = Path.home() / '.fujitsu-quantum'
    config_file_path = config_dir / 'config.json'

    if config_file_path.exists():
        with open(config_file_path, "r", encoding='utf-8') as f:
            conf_data = pyjson5.decode_io(f)

        if not isinstance(conf_data, dict):
            raise ValueError(f"Invalid config file: {config_file_path}")

        conf = conf_data
    else:
        conf = {}

    available_keys = {'authPoolId', 'authSdkClientId', 'apiBase', 'resultPollingInterval', 'retryMaxAttempts'}
    invalid_keys = conf.keys() - available_keys
    if invalid_keys:
        raise ValueError(f'Invalid parameter names in config.json: {invalid_keys}\n'
                         f'config.json path: {config_file_path}')

    # validate the config values
    result_polling_interval = conf.get('resultPollingInterval', 5)
    if result_polling_interval < 1:
        raise ValueError('Invalid value in config.json: resultPollingInterval must be >= 1.\n'
                         f'config.json path: {config_file_path}')

    retry_max_attempts = conf.get('retryMaxAttempts', 10)
    if retry_max_attempts < 0:
        raise ValueError('Invalid value in config.json: retryMaxAttempts must be >= 0.\n'
                         f'config.json path: {config_file_path}')

    # Note: some config values can be overridden via the config file for development purpose
    return _Config(
        config_dir=str(config_dir),
        auth_pool_id=conf.get('authPoolId', 'ap-northeast-1_oUVGkT61e'),
        auth_sdk_client_id=conf.get('authSdkClientId', '66l8iadggtteljctngjepi8du0'),
        api_base=conf.get('apiBase', 'https://api.quantum.global.fujitsu.com'),
        result_polling_interval=result_polling_interval,
        retry_max_attempts=retry_max_attempts,
    )


Config = load_config()
