CREATE_TABLE = """
                CREATE TABLE IF NOT EXISTS watchlist (
                    section_id VARCHAR(6) PRIMARY KEY,
                    department VARCHAR(4) NOT NULL,
                    emails JSONB NOT NULL
                );
                """

ADD_TO_WATCHLIST = """
                INSERT INTO watchlist (section_id, department, emails)
                VALUES (%s, %s, %s::jsonb)
                ON CONFLICT (section_id)
                DO UPDATE SET emails = watchlist.emails || EXCLUDED.emails;
                """

DELETE_FROM_WATCHLIST = "DELETE FROM watchlist WHERE section_id = %s;"
