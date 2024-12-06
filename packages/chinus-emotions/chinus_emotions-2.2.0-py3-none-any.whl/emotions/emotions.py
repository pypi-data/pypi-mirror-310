from typing import Literal
from db_connect import db_connect


def get_rand_id(
        table_name: Literal['minds', 'feelings', 'senses'],
        only_positive: bool = False,
        only_negative: bool = False,
        num: int = 1
) -> list[int]:
    """
    선택한 테이블에서 랜덤한 id(pk) 리턴

    :param table_name: id 가져올 테이블 이름
    :param only_positive: True면 긍정적인 것만 리턴
    :param only_negative: True면 부정적인 것만 리턴
    :param num: 리턴할 id 갯수
    :return: [id1, id2, id3, ...]
    """

    # positive와 negative 동시 True일 경우 처리
    if only_positive and only_negative:
        raise ValueError("At least one of `only_positive` or `only_negative` must be False.")

    # WHERE 절 생성
    if only_positive:
        where_clause = 'WHERE sentiment != -1'
    elif only_negative:
        where_clause = 'WHERE sentiment = -1'
    else:
        where_clause = ''

    # 쿼리
    query = f'''
        SELECT id
        FROM {table_name}
        {where_clause}
        ORDER BY RANDOM()
        LIMIT {num}
    '''

    ids = db_connect(query)

    # 리턴
    return [id[0] for id in ids]


def get_word(
        table_name: Literal['minds', 'feelings', 'senses'],
        id: int
) -> str:
    """
    선택한 테이블에서 id에 해당하는 단어 리턴

    :raise KeyError: 유효하지 않은 id 일 때
    """

    query = f'''
    SELECT word
    FROM {table_name}
    WHERE id = {id}
    '''

    word = db_connect(query)

    if word is None:
        raise KeyError(f'id: {id} is not valid from {table_name}.')

    return word[0][0]


def get_mean(
        table_name: Literal['minds', 'feelings', 'senses'],
        id: int
) -> str:
    """
    선택한 테이블에서 id에 해당하는 단어의 뜻 리턴

    :raise KeyError: 유효하지 않은 id 일 때
    """

    query = f'''
    SELECT mean
    FROM {table_name}
    WHERE id = {id}
    '''

    mean = db_connect(query)

    if mean is None:
        raise KeyError(f'id: {id} is not valid from {table_name}.')

    return mean[0][0]