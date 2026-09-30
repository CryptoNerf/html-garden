from PIL import Image, ImageOps
import json
import os

# Конвертирует PNG растений и фото владельцев из plants.json в WebP и обновляет пути в plants.json.
# Запускать после добавления нового растения: python3 optimize_plants.py

PLANTS_JSON = 'plants.json'
LARGE_DIR = 'image/plants'          # для страницы растения
THUMB_DIR = 'image/plants/thumbs'   # для сетки в саду
OWNER_DIR = 'image/owners'
LARGE_SIZE = 1080
THUMB_SIZE = 400
OWNER_SIZE = 480                    # по короткой стороне: фото обрезается в круг через object-fit: cover


def save_webp(img, size, path):
    # Уменьшаем в premultiplied-альфе, чтобы по краям не было тёмного ореола
    resized = img.convert('RGBa')
    resized.thumbnail((size, size), Image.Resampling.LANCZOS)
    resized.convert('RGBA').save(path, 'WebP', quality=85, method=6)


def save_owner_webp(source, path):
    img = ImageOps.exif_transpose(Image.open(source))  # WebP не хранит EXIF-поворот
    img = img.convert('RGBA' if 'A' in img.getbands() else 'RGB')
    scale = OWNER_SIZE / min(img.size)
    if scale < 1:
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    img.save(path, 'WebP', quality=85, method=6)


os.makedirs(THUMB_DIR, exist_ok=True)
os.makedirs(OWNER_DIR, exist_ok=True)

with open(PLANTS_JSON, encoding='utf-8') as f:
    data = json.load(f)

total_before = 0
total_after = 0

for plant in data['plants']:
    source = plant['largeImage'].lstrip('/')
    if not source.lower().endswith('.png'):
        continue  # уже сконвертировано

    name = os.path.splitext(os.path.basename(source))[0] + '.webp'
    large_path = os.path.join(LARGE_DIR, name)
    thumb_path = os.path.join(THUMB_DIR, name)

    img = Image.open(source).convert('RGBA')
    save_webp(img, LARGE_SIZE, large_path)
    save_webp(img, THUMB_SIZE, thumb_path)

    plant['image'] = '/' + thumb_path
    plant['largeImage'] = '/' + large_path

    before = os.path.getsize(source) / 1024
    large = os.path.getsize(large_path) / 1024
    thumb = os.path.getsize(thumb_path) / 1024
    total_before += before
    total_after += thumb
    print(f"[OK] {name}: {before:.0f}KB -> {large:.0f}KB (large), {thumb:.0f}KB (thumb)")

converted_owners = {}
for plant in data['plants']:
    source = plant.get('ownerPhoto', '').lstrip('/')
    if not source or source.lower().endswith('.webp'):
        continue

    if source not in converted_owners:
        owner_path = os.path.join(OWNER_DIR, os.path.splitext(os.path.basename(source))[0] + '.webp')
        save_owner_webp(source, owner_path)
        converted_owners[source] = '/' + owner_path
        before = os.path.getsize(source) / 1024
        after = os.path.getsize(owner_path) / 1024
        print(f"[OK] {os.path.basename(owner_path)}: {before:.0f}KB -> {after:.0f}KB (owner)")

    plant['ownerPhoto'] = converted_owners[source]

with open(PLANTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

if total_before:
    print(f"\n=== Сад: {total_before / 1024:.1f}MB -> {total_after / 1024:.1f}MB ===")
