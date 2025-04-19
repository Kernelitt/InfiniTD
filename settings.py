import json
import os
from cryptography.fernet import Fernet

class Settings:

    key = b'aVV1rKC-_l1OxB2ym3AwR-FsHDW79OJnPr-Ppcr9W9w='  # Замените на ваш сгенерированный ключ
    cipher = Fernet(key)    


    def __init__(self):
        self.screen_width = 1800
        self.screen_height = 1000
        self.bg_color = (25, 25, 25)

    def load_data(self):
        if os.path.exists("save_data.data"):
            with open("save_data.data", 'rb') as f:
                encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data)  
        return {"Money": 0, "StartMoney": int(0), "StartMoneyUpgradePrice": int(150),"Levels": {}}

    def save_data(self, data):
        json_data = json.dumps(data).encode()
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

