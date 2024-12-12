import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

def on_clicked(icon, item):
    if str(item) == 'Exit':
        icon.stop()
    elif str(item) == 'Show Message':
      print("Hello from tray icon!") # Здесь можно добавить любое действие

# Создаем иконку
image = Image.new('RGB', (64, 64), 'white')
draw = ImageDraw.Draw(image)
draw.ellipse((0, 0, 64, 64), fill='black') # Простая черная круглая иконка
image = image.resize((16, 16), Image.LANCZOS) # Оптимизация размера

# Создаем пункты меню
menu = (item('Show Message', on_clicked), item('Exit', on_clicked))

# Создаем иконку в трее
icon = pystray.Icon("My Program", image, "My Program", menu)
icon.run()