CREATE_TABLE_WATCHLIST = """
                CREATE TABLE IF NOT EXISTS watchlist (
                    id SERIAL PRIMARY KEY,
                    section_id VARCHAR(50) NOT NULL,
                    department VARCHAR(4) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    UNIQUE (section_id, email)
                );
                """

CREATE_TABLE_PROFESSORLIST = """
                CREATE TABLE IF NOT EXISTS professorlist (
                    legacy_id VARCHAR(10) PRIMARY KEY,
                    first_name VARCHAR(25) NOT NULL,
                    last_name VARCHAR(25) NOT NULL,
                    department VARCHAR(50) NOT NULL,
                    rating VARCHAR(3) NOT NULL
                    );
                    """

CREATE_TABLE_COURSES = """
                CREATE TABLE IF NOT EXISTS courselist (
                    section_id VARCHAR(8) PRIMARY KEY,
                    department_prefix VARCHAR(5) NOT NULL,
                    course_number VARCHAR(5) NOT NULL
                    first_name VARCHAR(25) NOT NULL,
                    last_name VARCHAR(25) NOT NULL,
                    start_time VARCHAR(8) NOT NULL,
                    end_time VARCHAR(8) NOT NULL,
                    days VARCHAR(5) NOT NULL,
                    class_type VARCHAR(8) NOT NULL
                    );
                    """

ADD_TO_PROFESSORLIST = """
            INSERT INTO professorlist (legacy_id, first_name, last_name, department, rating)
            VALUES (%s, %s, %s, %s, %s);
        """

SEARCH_PROFESSOR_DEPARTMENT = "SELECT * FROM professorlist WHERE first_name ~ %s AND last_name ~ %s AND (LOWER(department) ~ %s OR %s ~ LOWER(department));"
SEARCH_PROFESSOR_NAME = (
    "SELECT * FROM professorlist WHERE first_name ~ %s AND last_name ~ %s;"
)

ADD_TO_WATCHLIST = """
                INSERT INTO watchlist (section_id, department, email)
                VALUES (%s, %s, %s)
                ON CONFLICT (section_id, email) DO NOTHING;
                """

DELETE_FROM_WATCHLIST = "DELETE FROM watchlist WHERE section_id = %s;"

GET_WATCHLIST = "SELECT * FROM watchlist;"

SEARCH_BY_SECTION = "SELECT * FROM watchlist WHERE section_id = %s;"

SEARCH_WATCHLIST = "SELECT * FROM watchlist WHERE section_id = %s AND email = %s;"

SEARCH_BY_EMAIL = "SELECT * FROM watchlist WHERE email = %s;"

DELETE_EMAIL_FROM_WATCHLIST = """
                DELETE FROM watchlist
                WHERE section_id = %s AND email = %s;
                            """
