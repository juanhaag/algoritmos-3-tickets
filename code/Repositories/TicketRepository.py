import sqlite3
from pathlib import Path
from ..Models.Ticket import Ticket
from datetime import datetime


DB_PATH = Path(__file__).resolve().parent.parent / "tickets.db"


class TicketRepository:
    def __init__(self, db_path: str | Path = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self._ensure_db()

    def _get_conn(self):
        return sqlite3.connect(str(self.db_path))

    def _ensure_db(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT,
                incident TEXT,
                telephone_operator TEXT,
                service_record TEXT,
                message TEXT,
                state TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def create(self, client: str = None, incident: str = None, message: str = "") -> int:
        now = datetime.now().isoformat()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tickets (client, incident, message, state, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (client, incident, message, "open", now, now),
        )
        conn.commit()
        ticket_id = cur.lastrowid
        conn.close()
        return ticket_id

    def get_all(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, client, incident, telephone_operator, service_record, message, state, created_at, updated_at FROM tickets ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        tickets = []
        for r in rows:
            tickets.append({
                "id": r[0],
                "client": r[1],
                "incident": r[2],
                "telephone_operator": r[3],
                "service_record": r[4],
                "message": r[5],
                "state": r[6],
                "created_at": r[7],
                "updated_at": r[8],
            })
        return tickets

    def get_by_id(self, ticket_id: int):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, client, incident, telephone_operator, service_record, message, state, created_at, updated_at FROM tickets WHERE id = ?", (ticket_id,))
        r = cur.fetchone()
        conn.close()
        if not r:
            return None
        return {
            "id": r[0],
            "client": r[1],
            "incident": r[2],
            "telephone_operator": r[3],
            "service_record": r[4],
            "message": r[5],
            "state": r[6],
            "created_at": r[7],
            "updated_at": r[8],
        }

    def update(self, ticket_id: int, **fields) -> bool:
        allowed = ["client", "incident", "telephone_operator", "service_record", "message", "state"]
        set_parts = []
        values = []
        for k, v in fields.items():
            if k in allowed:
                set_parts.append(f"{k} = ?")
                values.append(v)
        if not set_parts:
            return False
        values.append(datetime.now().isoformat())
        values.append(ticket_id)
        sql = f"UPDATE tickets SET {', '.join(set_parts)}, updated_at = ? WHERE id = ?"
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(sql, tuple(values))
        conn.commit()
        updated = cur.rowcount > 0
        conn.close()
        return updated

    def delete(self, ticket_id: int) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted
