import sqlite3

DB_NAME = "app.db"

class DatabaseConnection:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
            
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()