from pathlib import Path
import yaml
from reliable_importer.exceptions import ConfigurationError
from reliable_importer.models import AppConfig, LoggingConfig, ProcessingConfig


def load_config(path: Path) -> AppConfig:
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(
            f"Файл конфігурації не знайдено: {path}"
        ) from error
    except yaml.YAMLError as error:
        raise ConfigurationError("Некоректна структура YAML") from error

    try:
        config = AppConfig(
            input_path=Path(raw["input"]["path"]),
            output_path=Path(raw["output"]["path"]),
            processing=ProcessingConfig(
                min_year=int(raw["processing"]["min_year"]),
                max_year=int(raw["processing"]["max_year"]),
                skip_invalid=bool(raw["processing"]["skip_invalid"]),
            ),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=Path(raw["logging"]["path"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError(
            "Некоректні або відсутні ключі в конфігурації"
        ) from error

    validate_config(config)
    return config


def validate_config(config: AppConfig) -> None:
    proc = config.processing
    if proc.min_year > proc.max_year:
        raise ConfigurationError("min_year не може бути більшим за max_year")
    if not config.input_path.exists():
        raise ConfigurationError(
            f"Вхідний CSV-файл не знайдено: {config.input_path}"
        )