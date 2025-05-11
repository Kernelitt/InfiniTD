import json
import os,sys
from cryptography.fernet import Fernet 
import importlib

class Settings:

    key = b'aVV1rKC-_l1OxB2ym3AwR-FsHDW79OJnPr-Ppcr9W9w='  # Замените на ваш сгенерированный ключ
    cipher = Fernet(key)  
    total_plugins = []  
    plugins = []
    disabled_plugins = []           # Initially disabled plugins
    def __init__(self):
        self.screen_width = 1800
        self.screen_height = 1000
        self.bg_color = (25, 25, 25)
        self.save_base = {
            "Money":int(0),
            "Upgrades": {
                "StartMoney": int(0),
                "StartXPLevel": int(0),
                "StartBaseHP": int(0),
            },
            "UpgradesCost": {
                "StartMoney": int(150),
                "StartXPLevel": int(1000),
                "StartBaseHP": int(300),
            },
            "UpgradesPower": {
                "StartMoney": int(10),
                "StartXPLevel": int(1),
                "StartBaseHP": int(3),
            },
            "Levels": {}
        }

    def load_data(self):
        if os.path.exists("save_data.data"):
            with open("save_data.data", 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data)  
        return self.save_base

    def save_data(self, data):
        existing_data = self.load_data()

        for key, value in data.items():
            if isinstance(value, dict):
                existing_data[key] = existing_data.get(key, {})
                existing_data[key].update(value)
            else:
                existing_data[key] = value
        json_data = json.dumps(existing_data).encode()
        encrypted_data = self.cipher.encrypt(json_data)
        with open("save_data.data", 'wb') as f:
            f.write(encrypted_data)

    def save_game_data(self,money, level, wave):
        data = self.load_data()
    # Обновляем количество монет
        data["Money"] += money  # Прибавляем полученные монеты
        if "Levels" not in data:
            data["Levels"] = {}
        if str(level) not in data["Levels"] or data["Levels"][str(level)] < wave:
           data["Levels"][str(level)] = wave  # Обновляем рекорд волн
   
        self.save_data(data)

    def read_screen_resolution(config_file='config.ini'):
        try:
            with open(config_file, 'r') as file:
                content = file.readlines()
        except FileNotFoundError:
            print("Error: Configuration file not found.")
            return None

        width = None
        height = None

        for line in content:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                if section == 'Screen':
                    continue
            elif '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if key == 'width':
                    width = value
                elif key == 'height':
                    height = value

        if width is None or height is None:
            print("Error: Section 'Screen' or keys 'width' and 'height' not found in the configuration file.")
            return None

        try:
            width = int(width)
            height = int(height)
        except ValueError:
            print("Error: Values 'width' and 'height' must be integers.")
            return None

        return width, height

    def load_plugins(self, plugin_folder='mods'):
        self.total_plugins = []
        if not os.path.exists(plugin_folder):
            print(f"Plugin folder '{plugin_folder}' does not exist.")
            return
        # Добавляем путь к папке mods в список sys.path
        sys.path.insert(0, os.path.abspath(plugin_folder))
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                module_name = filename[:-3]  # Убираем .py
                try:
                    module = importlib.import_module(module_name)
                    self.plugins.append(module)
                    self.total_plugins.append(module)
                    print(f"Loaded mod: {module_name}")
                except ImportError as e:
                    print(f"Error loading mod: {module_name} - {e}")
        print("Loaded in total ", self.plugins)

    def toggle_plugin(self,i):
        plugin_name = self.total_plugins[i]
        if plugin_name in self.plugins:
            self.plugins.remove(plugin_name)
            self.disabled_plugins.append(plugin_name)
            print(f"Disabled plugin: {plugin_name}")
        elif plugin_name in self.disabled_plugins:
            self.disabled_plugins.remove(plugin_name)
            self.plugins.append(plugin_name)
            print(f"Enabled plugin: {plugin_name}")
        else:
            pass