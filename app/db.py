import sqlite3
from pathlib import Path

from .config import load_config


def get_connection() -> sqlite3.Connection:
    """
    Geeft een SQLite connectie terug op basis van de config.
    Zorgt ervoor dat de map bestaat.
    """
    cfg = load_config()
    db_path = Path(cfg["database_path"])

    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    return conn


def init_db() -> None:
    """
    Maakt de tabellen aan indien ze nog niet bestaan.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Tabel voor Pokémon-sets
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sets (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            code    TEXT NOT NULL UNIQUE,   -- set id, bv 'BRS'
            name    TEXT NOT NULL           -- set name, bv 'Brilliant Stars'
        );
        """
    )

    # Tabel voor kaarten
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cards (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,      -- naam van de kaart
            set_id      INTEGER NOT NULL,   -- verwijzing naar sets.id
            count       INTEGER NOT NULL,   -- aantal kaarten
            price       REAL NOT NULL,      -- prijs per kaart
            FOREIGN KEY(set_id) REFERENCES sets(id)
        );
        """
    )

    conn.commit()
    conn.close()
