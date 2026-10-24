class ApplicationError(Exception):
    """Базовий виняток додатка."""


class ConfigurationError(ApplicationError):
    """Помилка конфігурації."""


class DataError(ApplicationError):
    """Базовий виняток для помилок даних."""


class DataImportError(DataError):
    """Неможливо імпортувати вхідні дані."""


class RecordValidationError(DataError):
    """Помилка валідації конкретного запису."""

    def __init__(
        self,
        message: str,
        *,
        line_number: int | None = None,
        field: str | None = None,
    ) -> None:
        super().__init__(message)
        self.line_number = line_number
        self.field = field


class DataExportError(DataError):
    """Помилка експорту даних."""