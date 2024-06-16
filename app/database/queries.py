CREATE_TABLE = """
                CREATE TABLE IF NOT EXISTS watchlist (
                    id SERIAL PRIMARY KEY,
                    section_id VARCHAR(50) NOT NULL,
                    department VARCHAR(4) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    UNIQUE (section_id, email)
                );
                """

ADD_TO_WATCHLIST = """
                INSERT INTO watchlist (section_id, department, email)
                VALUES (%s, %s, %s)
                ON CONFLICT (section_id, email) DO NOTHING;
                """

DELETE_FROM_WATCHLIST = "DELETE FROM watchlist WHERE section_id = %s;"

GET_WATCHLIST = "SELECT * FROM watchlist;"

SEARCH_BY_SECTION = "SELECT * FROM watchlist WHERE section_id = %s;"

SEARCH_WATCHLIST = "SELECT * FROM watchlist WHERE section_id = %s AND email = %s;"

DELETE_EMAIL_FROM_WATCHLIST = """
                DELETE FROM watchlist
                WHERE section_id = %s AND email = %s;
                            """
