from PIL import Image
import os

# Открываем анимированный WebP
input_path = 'image/butterwebp.webp'
output_path = 'image/butterwebp_720p.webp'

img = Image.open(input_path)

# Получаем все кадры
frames = []
durations = []

try:
    while True:
        # Изменяем размер текущего кадра
        frame = img.copy()
        frame.thumbnail((1280, 720), Image.Resampling.LANCZOS)
        frames.append(frame)

        # Получаем длительность кадра
        durations.append(img.info.get('duration', 100))

        img.seek(img.tell() + 1)
except EOFError:
    pass

print(f"Обработано кадров: {len(frames)}")

# Сохраняем как анимированный WebP
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    format='WebP',
    lossless=False,
    quality=50
)

print(f"Файл сохранён: {output_path}")

# Показываем размеры
original_size = os.path.getsize(input_path) / (1024 * 1024)
new_size = os.path.getsize(output_path) / (1024 * 1024)
print(f"Оригинальный размер: {original_size:.2f} MB")
print(f"Новый размер: {new_size:.2f} MB")
