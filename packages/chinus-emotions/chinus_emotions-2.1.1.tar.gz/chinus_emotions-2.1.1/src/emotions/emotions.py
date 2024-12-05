import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
g_db_path = os.path.abspath(os.path.join(base_dir, 'emotions.db'))


def __get_table(table_name: str, only_positive: bool, only_negative: bool):
    global g_db_path

    # positive와 negative 동시 True 처리
    if only_positive and only_negative:
        raise ValueError("At least one of `only_positive` or `only_negative` must be False.")

    # WHERE 절 생성
    if only_positive:
        where_clause = "WHERE sentiment != -1"
    elif only_negative:
        where_clause = "WHERE sentiment = -1"
    else:
        where_clause = ""



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


def get_rand_mind(only_positive=False, only_negative=False) -> tuple[str, str]:
    return __get_table('minds', only_positive=only_positive, only_negative=only_negative)



def get_rand_feeling(only_positive=False, only_negative=False) -> tuple[str, str]:
    return __get_table('feelings', only_positive=only_positive, only_negative=only_negative)


def get_rand_sense(only_positive=False, only_negative=False) -> tuple[str, str]:
    return __get_table('senses', only_positive=only_positive, only_negative=only_negative)