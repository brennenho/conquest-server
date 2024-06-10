import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="conquest_core",
            host="localhost",
            user="conquest_user",
            password="conquest_password",
            port="5432",
        )
        self.cursor = self.conn.cursor()

    def query(self, query, args=None):
        self.cur.execute(query, args)
        return self.cur.fetchall()

    def __del__(self):
        self.cur.close()
        self.conn.close()
