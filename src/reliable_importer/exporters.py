import json
from collections.abc import Iterable
from pathlib import Path
from reliable_importer.exceptions import DataExportError
from reliable_importer.models import Book


def export_books_json(books: Iterable[Book], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    count = 0

    try:
        with temporary.open("w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            for book in books:
                if not first:
                    file.write(",\n")
                json.dump(
                    book.to_dict(),
                    file,
                    ensure_ascii=False,
                    indent=2,
                )
                first = False
                count += 1
            file.write("\n]\n")
        temporary.replace(path)
    except (OSError, TypeError) as error:
        temporary.unlink(missing_ok=True)
        raise DataExportError(f"Неможливо експортувати дані у {path}") from error

    return count