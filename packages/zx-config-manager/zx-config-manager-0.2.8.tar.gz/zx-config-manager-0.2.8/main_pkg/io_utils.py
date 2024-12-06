import json
import os

# 自定义函数用于加载配置数据
def load_config(config_file_path):
    # 假设我们从一个JSON文件中加载配置
    with open(config_file_path, 'r') as config_file:
        try:
            config_data = json.load(config_file)
            return config_data
        except json.JSONDecodeError as e:
            print(f"{config_file_path} Error decoding JSON: {e}")


def check_and_touch_log_file(log_file_path, log_name):
    try:
        if not log_file_path:
            return None
        if not log_file_path.endswith('.log'):
            log_file_path = os.path.join(log_file_path, log_name + '.log')
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        return log_file_path
    except Exception as e:
        print(f'Failed to create log file: {e}')
        return None