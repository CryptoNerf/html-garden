from PIL import Image
import os

# Список файлов для конвертации в WebP
images_to_convert = [
    'image/welcome to html-garden.png',
    'image/welcome to html-garden fone ver.png',
    'image/plant desc.png',
    'image/about.png',
    'image/manual.png',
    'image/icon.png',
    'image/DesktopVersion.png',
    'image/inst1.png',
    'image/inst2.png',
    'image/Антибиологическая взаимность.png',
    'image/Десятилетняя вымышленная радость.png',
    'image/диффузия.png',
    'image/Инопланетный огурец.png',
    'image/Кровавый моховик.png',
    'image/Моя милая страшная осень.png',
    'image/Острая необходимость.png',
    'image/Пустынный лиственник.png',
    'image/пылесборник.png',
    'image/резинка.png',
    'image/exampletree.png'
]

total_saved = 0

for img_path in images_to_convert:
    if not os.path.exists(img_path):
        print(f"Пропущен (не найден): {img_path}")
        continue

    try:
        # Открываем PNG
        img = Image.open(img_path)

        # Генерируем имя для WebP
        webp_path = img_path.rsplit('.', 1)[0] + '.webp'

        # Сохраняем как WebP с хорошим качеством
        img.save(webp_path, 'WebP', quality=85, method=6)

        # Статистика
        original_size = os.path.getsize(img_path) / (1024 * 1024)
        new_size = os.path.getsize(webp_path) / (1024 * 1024)
        saved = original_size - new_size
        total_saved += saved

        print(f"[OK] {os.path.basename(img_path)}: {original_size:.2f}MB -> {new_size:.2f}MB (saved {saved:.2f}MB)")

    except Exception as e:
        print(f"[ERROR] {img_path}: {e}")

print(f"\n=== Итого сохранено: {total_saved:.2f}MB ===")
