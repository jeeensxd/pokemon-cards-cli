from dataclasses import dataclass
from typing import Optional, List

from ..db import get_connection


@dataclass
class PokeSet:
    id: Optional[int]
    code: str
    name: str

    @staticmethod
    def create(code: str, name: str) -> "PokeSet":
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sets (code, name) VALUES (?, ?)",
            (code, name),
        )
        conn.commit()
        set_id = cur.lastrowid
        conn.close()
        return PokeSet(id=set_id, code=code, name=name)

    @staticmethod
    def get_all() -> List["PokeSet"]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, code, name FROM sets ORDER BY name")
        rows = cur.fetchall()
        conn.close()
        return [PokeSet(id=row[0], code=row[1], name=row[2]) for row in rows]

    @staticmethod
    def get_by_code(code: str) -> Optional["PokeSet"]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, code, name FROM sets WHERE code = ?",
            (code,),
        )
        row = cur.fetchone()
        conn.close()
        if row:
            return PokeSet(id=row[0], code=row[1], name=row[2])
        return None
