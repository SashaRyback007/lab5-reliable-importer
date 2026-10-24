from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import Book


def parse_book(
    row: dict[str, str],
    *,
    line_number: int,
    min_year: int,
    max_year: int,
) -> Book:
    isbn = row.get("isbn", "").strip()
    if not isbn:
        raise RecordValidationError(
            "ISBN книги порожній",
            line_number=line_number,
            field="isbn",
        )

    title = row.get("title", "").strip()
    if not title:
        raise RecordValidationError(
            "Назва книги порожня",
            line_number=line_number,
            field="title",
        )

    author = row.get("author", "").strip()
    if not author:
        raise RecordValidationError(
            "Автор книги порожній",
            line_number=line_number,
            field="author",
        )

    try:
        year = int(row["year"])
    except (KeyError, TypeError, ValueError) as error:
        raise RecordValidationError(
            "Некоректний формат року видання",
            line_number=line_number,
            field="year",
        ) from error

    if not (min_year <= year <= max_year):
        raise RecordValidationError(
            f"Рік видання має бути в межах від {min_year} до {max_year}",
            line_number=line_number,
            field="year",
        )

    try:
        pages = int(row["pages"])
    except (KeyError, TypeError, ValueError) as error:
        raise RecordValidationError(
            "Некоректний формат кількості сторінок",
            line_number=line_number,
            field="pages",
        ) from error

    if pages <= 0:
        raise RecordValidationError(
            "Кількість сторінок має бути суворо більшою за 0",
            line_number=line_number,
            field="pages",
        )

    return Book(
        isbn=isbn,
        title=title,
        author=author,
        year=year,
        pages=pages,
    )