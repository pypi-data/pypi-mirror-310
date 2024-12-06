import os
from flask import Flask,jsonify,request
from main_pkg import schedule
from main_pkg import io_utils
import time

app = Flask(__name__)

all_configs = {}
last_update_time = 0

def load_config_from_file():
    """
    This function is used to load the config values from a file.
    """
    global all_configs, last_update_time
    filename = os.getenv('ZX_CONFIG_PATH', os.path.join(os.path.expanduser("~"), '.zx_config', 'config.json'))
    file_mod_time = os.path.getmtime(filename) if os.path.exists(filename) else 0
    if file_mod_time > last_update_time and file_mod_time > 0:
        all_configs = load_utils.load_config(filename)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}, loaded config:{all_configs}")

@app.route('/config/<key>', methods=['GET'])
def get_specific_config(key):
    """
    This function is used to get a specific config value based on the key provided.
    :param key: specific config key
    :return: config value for the given key
    """
    global all_configs
    if not key in all_configs:
        return jsonify({'error': 'Config not found'}), 404
    return jsonify({'value': all_configs[key]}), 200

@app.route('/config', methods=['GET'])
def get_all_configs():
    """
    This function is used to get all the config values.
    :return: all config values
    """
    global all_configs
    return jsonify({'configs': all_configs}), 200


@app.route('/')
def hello_world():  # put application's code here
    """
    返回服务器系统信息、时间和欢迎信息
    :return:
    """
    print(f"config:{app.config}")
    return 'Welcome to ZX Config Center!'



def init_app():
    with app.app_context():
        load_config_from_file()
        print(f"ZX_CONFIG_PATH:{os.getenv('ZX_CONFIG_PATH')}, init config:{all_configs}")
        if os.getenv('ZX_SCHEDULE_ENABLE', 'False') == 'True':
            schedule.start_scheduler(load_config_from_file, int(os.getenv('ZX_SCHEDULE_INTERVAL', 60)))



def create_app():
    init_app()
    return app

if __name__ == '__main__':
    load_config_from_file()
    print(f"config:{all_configs}")
    app.run(port=5000)
