from pymysql import connect, cursors

import settings


class DBUtil:
    def __init__(self):
        self.conn = connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
        )
        self.cursor = self.conn.cursor(cursor=cursors.DictCursor)

    def execute_sql(self, sql):
        if "SELECT" in sql:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                return self.cursor.rowcount
            except Exception:
                self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()
