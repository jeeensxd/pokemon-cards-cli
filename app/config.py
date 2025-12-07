import configparser
from pathlib import Path


def load_config(config_filename: str = "config.ini") -> dict:
    """
    Laadt het instellingenbestand en geeft een dict terug met de database-locatie.
    """
    config_path = Path(config_filename)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configbestand '{config_filename}' niet gevonden. "
            f"Maak een kopie van 'config_example.ini' naar 'config.ini' en pas het pad aan."
        )

    parser = configparser.ConfigParser()
    parser.read(config_path)

    db_path = parser.get("database", "path", fallback="data/pokecards.db")

    return {
        "database_path": db_path
    }
