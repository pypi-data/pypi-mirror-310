#!python

import argparse
import os
import subprocess

from main_pkg.io_utils import check_and_touch_log_file

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='Config Center HttpPort number')
    parser.add_argument('--config-path', type=str, default = 'no-config-path', help='Config Center config file path')
    parser.add_argument('--daemonize', type=str, default = None, help='Daemonize uWSGI process or not. If not set log path will be printed to console, uWSGI will run in foreground.')
    return parser.parse_args()

def start_uwsgi(http_port, module, config_path, daemonize):

    processes_count = int(os.getenv('ZX_PROCESSES_COUNT', 2))
    threads_count = int(os.getenv('ZX_THREADS_COUNT', 4))

    print(f'Starting uWSGI with {processes_count} processes and {threads_count} threads')

    uwsgi_cmd = [
        'uwsgi',
        '--http', f'0.0.0.0:{http_port}',
        '--module', module,
        '--master',
        '--processes', f'{processes_count}',
        '--threads', f'{threads_count}',
        '--reload-mercy', '60'
    ]
    if daemonize or os.getenv('ZX_DAEMONIZE'):
        log_file_path = "/dev/null"
        if os.getenv('ZX_DAEMONIZE'):
            daemonize = os.getenv('ZX_DAEMONIZE')
        log_file = check_and_touch_log_file(daemonize, 'zx-config')
        if log_file:
            log_file_path = log_file
        uwsgi_cmd.extend(['--daemonize', log_file_path])

    print(f'uWSGI command: {uwsgi_cmd}')
    if os.path.exists(config_path):
        os.environ['ZX_CONFIG_PATH'] = config_path

    print(f'config file path: {os.getenv("ZX_CONFIG_PATH")}')

    if not os.getenv('ZX_CONFIG_PATH') and os.path.exists(os.path.join(os.path.expanduser("~"), '.zx_config', 'config.json')):
        os.environ['ZX_CONFIG_PATH'] = os.path.join(os.path.expanduser("~"), '.zx_config', 'config.json')
    if not os.getenv('ZX_CONFIG_PATH'):
        os.environ['ZX_CONFIG_PATH'] = '/app/config.json' # 兼容docker部署

    print(f'config file path: {os.getenv("ZX_CONFIG_PATH")}')

    try:
        subprocess.run(uwsgi_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed to start uWSGI: {e}')

def main():
    args = parse_args()
    config_file_path = args.config_path
    port = args.port
    if os.getenv('ZX_CONFIG_FILE_PATH') or args.config_path == 'no-config-path':
        config_file_path = os.getenv('ZX_CONFIG_FILE_PATH')
    if os.getenv('ZX_CONFIG_PORT'):
        port = int(os.getenv('ZX_CONFIG_PORT'))

    start_uwsgi(port, 'main_pkg.wsgi:app', str(config_file_path), args.daemonize)

if __name__ == '__main__':
    main()