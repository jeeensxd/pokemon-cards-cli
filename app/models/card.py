from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from ..db import get_connection


@dataclass
class Card:
    id: Optional[int]
    name: str
    set_id: int
    count: int
    price: float  # prijs per kaart

    @staticmethod
    def create(name: str, set_id: int, count: int, price: float) -> "Card":
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cards (name, set_id, count, price) VALUES (?, ?, ?, ?)",
            (name, set_id, count, price),
        )
        conn.commit()
        card_id = cur.lastrowid
        conn.close()
        return Card(id=card_id, name=name, set_id=set_id, count=count, price=price)

    @staticmethod
    def update_count(card_id: int, new_count: int) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE cards SET count = ? WHERE id = ?",
            (new_count, card_id),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_with_set() -> List[Dict[str, Any]]:
        """
        Haalt alle kaarten op inclusief set code en set name.
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT c.id,
                   c.name,
                   c.count,
                   c.price,
                   s.code,
                   s.name
            FROM cards c
            JOIN sets s ON c.set_id = s.id
            ORDER BY s.code, c.name;
            """
        )
        rows = cur.fetchall()
        conn.close()

        result: List[Dict[str, Any]] = []
        for row in rows:
            result.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "count": row[2],
                    "price": row[3],
                    "set_code": row[4],
                    "set_name": row[5],
                }
            )
        return result
