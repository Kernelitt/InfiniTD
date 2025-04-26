import tkinter as tk
from tkinter import messagebox, ttk
import json

class WaveMake:
    def __init__(self, master, row):
        self.row_var = row
        self.total_group = 0
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=self.row_var, column=0)
        self.wave_group = []
        self.load_button = tk.Button(self.frame, text="+", command=self.add_wave_group)
        self.load_button.grid(row=0, column=0)        
        self.load_button2 = tk.Button(self.frame, text="-", command=self.remove_wave_group)
        self.load_button2.grid(row=0, column=1)

    def add_wave_group(self):
        self.wave_group.append(WaveMakeGroup(self.frame, self.total_group))
        self.total_group += 3
        self.update_button_positions()

    def remove_wave_group(self):
        if self.wave_group:
            wave_group_to_remove = self.wave_group.pop()
            wave_group_to_remove.enemy_type.destroy()
            wave_group_to_remove.enemy_count.destroy()
            wave_group_to_remove.spawn_interval.destroy()
            self.total_group -= 3
            self.update_button_positions()

    def update_button_positions(self):
        for i, button in enumerate([self.load_button, self.load_button2]):
            button.grid_forget()
            button.grid(row=0, column=i)

    def get_waves_data(self):
        waves_data = []
        wave_group_data = []
        for wave_group in self.wave_group:
            wave_data = (wave_group.enemy_type.get(), wave_group.enemy_count.get(), wave_group.spawn_interval.get())
            wave_group_data.append(wave_data)
        waves_data.append(wave_group_data)
        return waves_data
    
class WaveMakeGroup:
    def __init__(self, master, col):
        self.enemy_type = ttk.Combobox(master,width=1, values=[1,2,3,4])
        self.enemy_type.grid(row=0, column=3+col)
        self.enemy_type.current(0)

        self.enemy_count = tk.Entry(master,width=5)
        self.enemy_count.grid(row=0, column=4+col)

        self.spawn_interval = tk.Entry(master,width=5)
        self.spawn_interval.grid(row=0, column=5+col)

class LevelMaker:
    def __init__(self, master):
        self.master = master
        self.master.title("Level Maker")
        self.custom_waves = []
        self.total_waves = 0
        self.canvas_size = 720  # 24 * 30
        self.cell_size = 30
        self.grid = []
        self.platforms = []  # Массив для хранения платформ
        self.paths = []      # Массив для хранения путей
        self.paths_save = [] 

        self.wave_frame = tk.Frame(master,bg="gray")
        self.wave_frame.grid(row=0, column=1)

        # Создаем канвас для рисования сетки
        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.grid(row=0, column=0)

        # Панель инструментов
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=1, column=0)

        # Выпадающий список для выбора типа объекта
        self.object_type = tk.StringVar()
        self.object_type.set("Платформа")  # Значение по умолчанию

        self.object_selector = ttk.Combobox(self.button_frame, textvariable=self.object_type)
        self.object_selector['values'] = ("Платформа", "Путь", "Удалить")
        self.object_selector.grid(row=0, column=0)

        self.hp_label = tk.Label(self.button_frame, text="ХП базы:")
        self.hp_label.grid(row=0, column=1)
        self.hp_entry = tk.Entry(self.button_frame, width=5)
        self.hp_entry.grid(row=0, column=2)

        self.difficulty_label = tk.Label(self.button_frame, text="Множитель сложности:")
        self.difficulty_label.grid(row=0, column=3)
        self.difficulty_entry = tk.Entry(self.button_frame, width=5)
        self.difficulty_entry.grid(row=0, column=4)

        tk.Label(self.button_frame, text="Название").grid(row=0, column=5)
        self.name_entry = tk.Entry(self.button_frame, width=5)
        self.name_entry.grid(row=0, column=6)

        self.save_button = tk.Button(self.button_frame, text="Сохранить уровень", command=self.save_level)
        self.save_button.grid(row=0, column=7)

        self.load_button = tk.Button(self.button_frame, text="Загрузить уровень", command=self.load_level)
        self.load_button.grid(row=0, column=8)

        self.load_button = tk.Button(self.button_frame, text="+Wave", command=lambda:self.create_wave())
        self.load_button.grid(row=0, column=9)
        # Инициализация сетки
        self.init_grid()

        # Обработка кликов на канвасе
        self.canvas.bind("<Button-1>", self.on_click)

    def create_wave(self):
        self.custom_waves.append(WaveMake(self.wave_frame,self.total_waves))
        self.total_waves +=1
        print(self.custom_waves,self.total_waves)

    def init_grid(self):
        for y in range(24):  # 24 строки
            row = []
            for x in range(24):  # 24 столбца
                rect = self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                                     (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                                     fill="white", outline="black")
                row.append(rect)
            self.grid.append(row)

    def on_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        selected_type = self.object_type.get()

        if selected_type == "Платформа":
            # Если клетка не занята, добавляем платформу
            if (x, y) not in self.platforms:  
                self.canvas.itemconfig(self.grid[y][x], fill="green")  # Устанавливаем цвет платформы
                self.platforms.append((x, y))  # Добавляем координаты платформы в массив
            # Если клетка уже является путём, убираем её из путей
            if (x, y) in self.paths:  
                self.paths.remove((x, y))
                self.canvas.itemconfig(self.grid[y][x], fill="green")  # Устанавливаем цвет платформы

        elif selected_type == "Путь":
            if (x, y) not in self.paths: 
                order = len(self.paths) + 1 
                self.canvas.itemconfig(self.grid[y][x], fill="red")  # Устанавливаем цвет пути
                self.paths.append((x, y,order))  # Добавляем координаты пути
                print(self.paths)
                # Сортируем пути по порядку
                self.paths.sort(key=lambda pos: pos[2]) 
            else:
                messagebox.showerror("Ошибка", "Порядок должен быть числом!")

        elif selected_type == "Удалить":
        # Удаляем клетку из платформ и путей
            if (x, y) in self.platforms:  
                self.platforms.remove((x, y))
            if (x, y) in self.paths:  
                self.paths.remove((x, y,order))
            self.canvas.itemconfig(self.grid[y][x], fill="white")  # Удаляем объект, устанавливаем белый цвет


    def save_level(self):
        platforms = []
        paths = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                fill_color = self.canvas.itemcget(self.grid[y][x], 'fill')
                if fill_color == 'green':
                    platforms.append((x, y))


        self.paths_save= [(x, y) for (x, y, _) in sorted(self.paths, key=lambda pos: pos[2])]
        # Получаем значения хп базы и множителя сложности
        base_health = self.hp_entry.get()
        difficulty_multiplier = self.difficulty_entry.get()

        waves_data = []
        for wave in self.custom_waves:
            waves_data.extend(wave.get_waves_data())

        level_data = {
            "platforms": platforms,
            "paths":self.paths_save,
            "base_health": int(base_health) if base_health.isdigit() else 100,  # Значение по умолчанию
            "difficulty_multiplier": float(difficulty_multiplier) if difficulty_multiplier.replace('.', '', 1).isdigit() else 1.0,  # Значение по умолчанию
            "waves": waves_data,
        }
        lvl_name = self.name_entry.get()
        with open(lvl_name+".json", "w") as file:
            json.dump(level_data, file)
        messagebox.showinfo("Сохранение", "Уровень сохранен!")

    def load_level(self):
        try:
            with open("level.json", "r") as file:
                level_data = json.load(file)

            # Сбросить сетку
            for y in range(len(self.grid)):
                for x in range(len(self.grid[y])):
                    self.canvas.itemconfig(self.grid[y][x], fill="white")

            # Загрузить платформы
            for (x, y) in level_data.get('platforms', []):
                self.canvas.itemconfig(self.grid[y][x], fill="green")

            # Загрузить пути
            for (x, y) in level_data.get('paths', []):
                self.canvas.itemconfig(self.grid[y][x], fill="blue")

            messagebox.showinfo("Загрузка", "Уровень загружен!")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл уровня не найден!")

if __name__ == "__main__":
    root = tk.Tk()
    level_maker = LevelMaker(root)
    root.mainloop()



