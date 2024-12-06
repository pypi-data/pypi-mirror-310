import json

# 自定义函数用于加载配置数据
def load_config(config_file_path):
    # 假设我们从一个JSON文件中加载配置
    with open(config_file_path, 'r') as config_file:
        try:
            config_data = json.load(config_file)
            return config_data
        except json.JSONDecodeError as e:
            print(f"{config_file_path} Error decoding JSON: {e}")