import sqlite3
import os

# base_dir = os.path.dirname(os.path.abspath(__file__))
# g_db_path = os.path.abspath(os.path.join(base_dir, 'emotions.db'))
g_db_path = 'emotions.db'

def __get_table(table_name: str, positive=True, negative=True):
    global g_db_path

    # positive와 negative 동시 False 처리
    if not (positive or negative):
        raise ValueError("At least one of `positive` or `negative` must be True.")

    # WHERE 절 생성
    if positive and negative:
        where_clause = ""
    elif positive:
        where_clause = "WHERE sentiment != -1"
    else:
        where_clause = "WHERE sentiment = -1"


    with sqlite3.connect(g_db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f'''
                SELECT word, mean 
                FROM {table_name}
                {where_clause}
                ORDER BY RANDOM()
                LIMIT 1
            ''')
            result = cursor.fetchone()
        finally:
            cursor.close()

    return result


def get_rand_mind(positive=True, negative=True) -> tuple[str, str]:
    return __get_table('minds', positive=positive, negative=negative)



def get_rand_feeling(positive=True, negative=True) -> tuple[str, str]:
    return __get_table('feeling', positive=positive, negative=negative)