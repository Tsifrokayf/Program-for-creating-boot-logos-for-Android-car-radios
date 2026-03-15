# 🚀 Boot Animation Creator Pro

A modern desktop tool for creating Android head unit boot animations from GIF files.  
Made by **[Tsifrokayf](https://github.com/Tsifrokayf)**.

---

## ✨ Features

- 🎞 Convert any GIF into a ready-to-flash `bootanimation.zip`
- 📐 Custom resolution with quick presets (1024×600, 1280×720, 800×480)
- 🔄 Loop modes: **infinite** or **play once**
- 🖼 Scale modes: **contain** (letterbox), **cover** (crop), **stretch**
- 🎨 Color depth: **RGB 24-bit** or **RGBA 32-bit** (important for older head units!)
- ⚡ Real-time animated **GIF preview** — see the final result before converting
- ⏱ Displays animation **duration** based on frame count and FPS
- 💾 Custom output filename support
- 📦 Output ZIP is **uncompressed** (ZIP_STORED) — required by Android bootanimation format

---

## 📦 Installation

### Option 1 — Ready EXE (Windows, no Python needed)
Download `BootAnimCreator.exe` from [Releases](../../releases) and run it directly.

### Option 2 — Run from source

**Requirements:** Python 3.8+

```bash
pip install Pillow customtkinter
python src/boot_creator.py
```

Or just double-click `src/run.bat` on Windows — it installs dependencies automatically.

---

## 🛠 How to use

1. Click **"Обзор..."** and select your GIF file
2. Set the target resolution (or pick a preset)
3. Adjust FPS, scale mode, color depth and loop type
4. Watch the real-time preview to verify the result
5. Enter the output filename (default: `bootanimation`)
6. Click **"СОЗДАТЬ BOOTANIMATION.ZIP"** and save the file
7. Copy `bootanimation.zip` to your Android head unit (usually `/system/media/` or via the bootanimation update method)

---

## 📁 Project structure

```
├── src/
│   ├── boot_creator.py   # Main application source
│   └── run.bat           # Windows launcher (auto-installs deps)
├── BootAnimCreator.exe   # Portable Windows executable
├── app_icon.ico          # Application icon
└── README.md
```

---

## 📋 Requirements (for source run)

| Package | Version |
|---|---|
| Python | 3.8+ |
| Pillow | any recent |
| customtkinter | any recent |

---

## 📄 License

MIT — free to use, modify and distribute.

---

*Created by [Tsifrokayf](https://github.com/Tsifrokayf)*

---
---

# 🚀 Boot Animation Creator Pro (RU)

Современный инструмент для создания загрузочных анимаций Android-магнитол из GIF-файлов.  
Автор: **[Tsifrokayf](https://github.com/Tsifrokayf)**

---

## ✨ Возможности

- 🎞 Конвертация любого GIF в готовый `bootanimation.zip`
- 📐 Произвольное разрешение с быстрыми пресетами (1024×600, 1280×720, 800×480)
- 🔄 Режимы цикла: **бесконечно** или **1 раз**
- 🖼 Режимы масштабирования: **contain** (вписать), **cover** (заполнить с обрезкой), **stretch** (растянуть)
- 🎨 Глубина цвета: **RGB 24-bit** или **RGBA 32-bit** (важно для старых магнитол!)
- ⚡ Анимированный **предпросмотр** в реальном времени — видишь результат ещё до конвертации
- ⏱ Отображение **длительности** анимации с учётом FPS и кол-ва кадров
- 💾 Настраиваемое имя выходного файла
- 📦 ZIP сохраняется **без сжатия** (ZIP_STORED) — это обязательное требование формата bootanimation

---

## 📦 Установка

### Вариант 1 — Готовый EXE (Windows, Python не нужен)
Скачайте `BootAnimCreator.exe` из раздела [Releases](../../releases) и запустите.

### Вариант 2 — Запуск из исходников

**Требования:** Python 3.8+

```bash
pip install Pillow customtkinter
python src/boot_creator.py
```

Или просто дважды кликните `src/run.bat` на Windows — скрипт автоматически установит все зависимости.

---

## 🛠 Как использовать

1. Нажмите **"Обзор..."** и выберите GIF-файл
2. Укажите нужное разрешение (или выберите пресет)
3. Настройте FPS, режим масштабирования, глубину цвета и тип цикла
4. Смотрите предпросмотр в реальном времени — убедитесь в результате
5. Введите имя выходного файла (по умолчанию: `bootanimation`)
6. Нажмите **«СОЗДАТЬ BOOTANIMATION.ZIP»** и сохраните файл
7. Скопируйте `bootanimation.zip` на магнитолу (обычно в `/system/media/` или через штатный метод обновления анимации)

---

## 📁 Структура проекта

```
├── src/
│   ├── boot_creator.py   # Основной исходный код
│   └── run.bat           # Запускатор для Windows (автоустановка зависимостей)
├── BootAnimCreator.exe   # Портативный EXE-файл для Windows
├── app_icon.ico          # Иконка приложения
└── README.md
```

---

## 📋 Зависимости (для запуска из исходников)

| Пакет | Версия |
|---|---|
| Python | 3.8+ |
| Pillow | любая актуальная |
| customtkinter | любая актуальная |

---

## 📄 Лицензия

MIT — свободно использовать, изменять и распространять.

---

*Создано [Tsifrokayf](https://github.com/Tsifrokayf)*
