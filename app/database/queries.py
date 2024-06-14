CREATE_TABLE = """
                CREATE TABLE IF NOT EXISTS watchlist (
                    section_id VARCHAR(50) PRIMARY KEY,
                    department VARCHAR(4) NOT NULL,
                    emails JSONB NOT NULL
                );
                """

ADD_TO_WATCHLIST = """
                INSERT INTO watchlist (section_id, department, emails)
                VALUES (%s, %s, %s::jsonb)
                ON CONFLICT (section_id)
                DO UPDATE SET emails = (
                    SELECT jsonb_agg(email) FROM (
                        SELECT DISTINCT jsonb_array_elements_text(watchlist.emails || EXCLUDED.emails) AS email
                    ) AS subquery
                );
                """

DELETE_FROM_WATCHLIST = "DELETE FROM watchlist WHERE section_id = %s;"

GET_WATCHLIST = "SELECT * FROM watchlist;"

SEARCH_WATCHLIST = "SELECT * FROM watchlist WHERE section_id = %s;"

DELETE_EMAIL_FROM_WATCHLIST = """
    DO $$
    BEGIN
        IF (
            SELECT jsonb_array_length(emails)
            FROM watchlist
            WHERE section_id = %s
        ) = 1 AND (
            SELECT emails->>0
            FROM watchlist
            WHERE section_id = %s
        ) = %s THEN
            DELETE FROM watchlist
            WHERE section_id = %s;
        ELSE
            UPDATE watchlist
            SET emails = (
                SELECT jsonb_agg(email) FROM (
                    SELECT email
                    FROM jsonb_array_elements_text(emails) AS email
                    WHERE email != %s
                ) AS subquery
            )
            WHERE section_id = %s;
        END IF;
    END $$;
                            """
