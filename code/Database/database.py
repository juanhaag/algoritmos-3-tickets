import sqlite3

class DataBase:
        
    def __init__(self):
        self.init_db()

    def get_db():
            conn = sqlite3.connect('Ticketing.db')
            conn.row_factory = sqlite3.Row
            return conn

    def init_db():
            with DataBase.get_db() as conn:
                    conn.execute("""
                                CREATE TABLE IF NOT EXISTS ticket(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    client  TEXT NOT NULL,
                                    incident  INT,
                                    telephone_operator TEXT,
                                    technician TEXT,
                                    message TEXT,
                                    unitequipment TEXT,
                                    state TEXT,
                                    service_record TEXT
                                )
                                """
                    )
                    conn.commit()
                    conn.close()