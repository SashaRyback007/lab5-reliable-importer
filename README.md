# Лабораторна робота №5: Обробка помилок, файли та серіалізація

Надійний модуль імпорту, валідації та атомарного експорту даних для **системи обліку книг (Варіант 2)**, створений у межах курсу «Професійний Python».

## 📌 Функціональні можливості

- **Streaming I/O (Потокове читання):** Обробка CSV-файлів за допомогою генераторів (`Iterator`) без завантаження всього датасету в оперативну пам'ять.
- **Fail-fast валідація конфігурації:** Перевірка параметрів YAML-конфігу та існування файлів до початку обробки даних.
- **Кастомна ієрархія винятків:** Власні класи помилок (`ApplicationError`, `RecordValidationError`, `ConfigurationError` тощо) з підтримкою Exception Chaining (`raise ... from ...`).
- **Гнучкі режими валідації:**
  - `Tolerant mode` (`skip_invalid: true`): Некоректні записи логуються як `WARNING`, пропускаються, а програма продовжує роботу.
  - `Strict mode` (`skip_invalid: false`): Перший же некоректний запис перериває виконання імпорту.
- **Атомарний експорт (Atomic Write):** Запис результатів у тимчасовий файл `.tmp` із подальшою заміною цільового `.json`, що унеможливлює пошкодження файлу при аварійному завершенні.
- **Логування та контекстні менеджери:** Використання модуля `logging` для фіксації подій у файл та консоль, а також кастомний `@contextmanager` для вимірювання часу виконання операцій.

---

## 🛠 Валідація даних (Варіант 2)

Модуль обробляє наступні поля сутності **Book**:
- `isbn`: Поле не може бути порожнім.
- `title`: Назва книги обов'язкова.
- `author`: Автор книги обов'язковий.
- `year`: Ціле число у допустимому діапазоні (задається в `config.yaml`, наприклад: `1000 <= year <= 2026`).
- `pages`: Ціле число, суворо більше за 0 (`pages > 0`).

---

## 📁 Структура проєкту

```text
reliable_importer/
├── data/
│   └── books.csv               # Вхідний CSV-файл
├── logs/
│   └── application.log         # Файл логів (автоматично створюється)
├── output/
│   └── books.json              # Результуючий JSON (автоматично створюється)
├── src/
│   └── reliable_importer/
│       ├── __init__.py
│       ├── config.py           # Завантаження та перевірка YAML
│       ├── exceptions.py       # Кастомні винятки
│       ├── exporters.py        # Атомарний експорт у JSON
│       ├── logging_config.py   # Налаштування логування
│       ├── main.py             # Точка входу
│       ├── models.py           # Dataclasses (Book, AppConfig)
│       ├── readers.py          # Потокове читання CSV
│       ├── services.py         # Бізнес-логіка та статистика
│       ├── utils.py            # Кастомний контекстний менеджер
│       └── validators.py       # Валідація полів книги
├── config.yaml                 # Конфігураційний файл
├── pyproject.toml              # Конфігурація пакета
└── README.md

🚀 Інструкція із запуску
1. Клонування репозиторію
Bash
git clone [https://github.com/ВАШ_НИКНЕЙМ/python-lab5-reliable-importer.git](https://github.com/ВАШ_НИКНЕЙМ/python-lab5-reliable-importer.git)
cd python-lab5-reliable-importer/reliable_importer
2. Встановлення залежностей
Рекомендується використовувати віртуальне оточення:

Bash
python -m venv .venv

# Для Linux / macOS:
source .venv/bin/activate

# Для Windows (PowerShell / CMD):
.venv\Scripts\activate

Установка проекту в режимі розробки:

Bash
pip install -e .
3. Запуск програми
Bash
python -m reliable_importer.main
Або з явним зазначенням PYTHONPATH:

Windows (CMD):

DOS
set PYTHONPATH=src && python -m reliable_importer.main
Linux / macOS:

Bash
PYTHONPATH=src python -m reliable_importer.main
📊 Приклад роботи та виводу
При виконанні програми у Tolerant mode (skip_invalid: true):

Plaintext
2026-10-24 15:40:22,722 | INFO | reliable_importer.utils | Імпорт та експорт книг розпочато
2026-10-24 15:40:22,724 | WARNING | reliable_importer.services | Некоректний запис у рядку 5 (поле: title): Назва книги порожня
2026-10-24 15:40:22,724 | WARNING | reliable_importer.services | Некоректний запис у рядку 6 (поле: year): Рік видання має бути в межах від 1000 до 2026
2026-10-24 15:40:22,724 | WARNING | reliable_importer.services | Некоректний запис у рядку 7 (поле: pages): Кількість сторінок має бути суворо більшою за 0
2026-10-24 15:40:22,726 | INFO | reliable_importer.utils | Імпорт та експорт книг завершено за 0.003356 с
2026-10-24 15:40:22,726 | INFO | __main__ | Всього=7, валідних=4, невалідних=3, експортовано=4

Після створення файла додайте його до комміту та запушьте на GitHub:

```cmd
git add README.md
git commit -m "docs: add comprehensive README.md"
git push