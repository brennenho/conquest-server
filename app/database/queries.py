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
                    rating VARCHAR(3) NOT NULL,
                    UNIQUE (legacy_id)
                    );
                    """

CREATE_TABLE_COURSES = """
                CREATE TABLE IF NOT EXISTS courselist (
                    id SERIAL PRIMARY KEY,
                    section_id VARCHAR(10) NOT NULL,
                    course VARCHAR(8) NOT NULL,
                    first_name VARCHAR(60) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    start_time VARCHAR(30) NOT NULL,
                    end_time VARCHAR(30) NOT NULL,
                    days VARCHAR(15) NOT NULL,
                    class_type VARCHAR(8) NOT NULL,
                    UNIQUE (section_id)
                    );
                    """
ADD_TO_COURSELIST = """
                INSERT INTO courselist (section_id, course, first_name, last_name, start_time, end_time, days, class_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (section_id) DO NOTHING;
                """
SEARCH_COURSE = "SELECT * FROM courselist WHERE LOWER(course) = LOWER(%s);"
SEARCH_COURSE_BY_ID = "SELECT * FROM courselist WHERE section_id = %s;"
ADD_TO_PROFESSORLIST = """
                    INSERT INTO professorlist (legacy_id, first_name, last_name, department, rating)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (legacy_id) DO NOTHING;
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
