import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import Book
from reliable_importer.readers import read_csv_rows
from reliable_importer.validators import parse_book

logger = logging.getLogger(__name__)


@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0


def import_books(
    path: Path,
    *,
    min_year: int,
    max_year: int,
    skip_invalid: bool,
    statistics: ImportStatistics,
) -> Iterator[Book]:
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            book = parse_book(
                row,
                line_number=line_number,
                min_year=min_year,
                max_year=max_year,
            )
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning(
                "Некоректний запис у рядку %s (поле: %s): %s",
                error.line_number,
                error.field,
                error,
            )
            if skip_invalid:
                continue
            raise
        statistics.valid += 1
        yield book