CREATE_TABLE_WATCHLIST = """
                CREATE TABLE IF NOT EXISTS watchlist (
                    id SERIAL PRIMARY KEY,
                    section_id VARCHAR(50) NOT NULL,
                    department VARCHAR(4) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    UNIQUE (section_id, email)
                );
                """

CREATE_TABLE_PROFESSORLIST = """"
                CREATE TABLE IF NOT EXISTS professorlist (
                    legacy_id VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(4) NOT NULL,
                    rating VARCHAR(5) NOT NULL
                    );
                    """

ADD_TO_PROFESSORLIST = """
                INSERT INTO professorlist (legacy_id, name, department, rating)
                VALUES (%s, %s, %s, %s);
                """

SEARCH_PROFESSOR = "SELECT * FROM professorlist WHERE name = %s"

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
