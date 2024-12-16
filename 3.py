import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def convert_to_bw(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = image_hsv[..., 1]
    mask = saturation < 200 # Маска для низкой насыщенности
    
    # Преобразуем точки с низкой насыщенностью в чёрно-белые
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale_bgr = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)
    image[mask] = grayscale_bgr[mask]
    return image

def linear_darken(image1, image2):
    # Применение эффекта Cres = C1 + C2 - 1 (нормализуем значение каналов)
    result = cv2.add(image1.astype(np.float32) / 255.0, image2.astype(np.float32) / 255.0) - 1.0
    result = np.clip(result, 0, 1)  # Ограничение значений в диапазоне [0, 1]
    return (result * 255).astype(np.uint8)

def process_images(image1_path, image2_path, output_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    
    # Приводим первое изображение к размеру второго
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
    
    # Преобразуем первое изображение в ч/б точки (с низкой насыщенностью)
    image1 = convert_to_bw(image1)
    
    # Применяем эффект линейного затемнения
    result = linear_darken(image1, image2)

    cv2.imwrite(output_path, result)

def load_image1():
    global image1_path
    image1_path = filedialog.askopenfilename(title="Выберите первое изображение", filetypes=[("Изображения", ".jpg .jpeg .png .webp")])
    if not image1_path:
        messagebox.showerror("Ошибка", "Не удалось загрузить первое изображение.")

def load_image2():
    global image2_path
    image2_path = filedialog.askopenfilename(title="Выберите второе изображение", filetypes=[("Изображения", ".jpg .jpeg .png .webp")])
    if not image2_path:
        messagebox.showerror("Ошибка", "Не удалось загрузить второе изображение.")

def save_output():
    output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    return output_path

def process():
    if not image1_path or not image2_path:
        messagebox.showerror("Ошибка", "Пожалуйста, загрузите оба изображения.")
        return

    output_path = save_output()
    if output_path:
        process_images(image1_path, image2_path, output_path)
        messagebox.showinfo("Успех", f"Изображение успешно сохранено по пути:\n{output_path}")

root = tk.Tk()
root.title("Обработка изображений")

button_image1 = tk.Button(root, text="Загрузить первое изображение", command=load_image1)
button_image1.pack(padx=10, pady=5)

button_image2 = tk.Button(root, text="Загрузить второе изображение", command=load_image2)
button_image2.pack(padx=10, pady=5)

button_process = tk.Button(root, text="Обработать и сохранить", command=process)
button_process.pack(padx=10, pady=20)

root.mainloop()
