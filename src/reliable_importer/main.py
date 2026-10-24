import logging
from pathlib import Path
from reliable_importer.config import load_config
from reliable_importer.exceptions import ApplicationError
from reliable_importer.exporters import export_books_json
from reliable_importer.logging_config import configure_logging
from reliable_importer.services import ImportStatistics, import_books
from reliable_importer.utils import logged_operation

logger = logging.getLogger(__name__)


def main() -> None:
    try:
        config = load_config(Path("config.yaml"))
        configure_logging(config.logging.level, config.logging.path)
        statistics = ImportStatistics()

        with logged_operation("Імпорт та експорт книг"):
            books = import_books(
                config.input_path,
                min_year=config.processing.min_year,
                max_year=config.processing.max_year,
                skip_invalid=config.processing.skip_invalid,
                statistics=statistics,
            )
            exported = export_books_json(books, config.output_path)

        logger.info(
            "Всього=%s, валідних=%s, невалідних=%s, експортовано=%s",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            exported,
        )
    except ApplicationError as error:
        logger.error("Помилка застосунку: %s", error)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()