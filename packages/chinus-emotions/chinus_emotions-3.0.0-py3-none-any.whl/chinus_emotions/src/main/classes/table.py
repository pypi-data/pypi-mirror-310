from typing import Literal
from chinus_emotions.src.main.classes.emotion import Emotion
from chinus_emotions.src.main.db.db_connect import db_connect


class Table:
    _TABLE_NAME: Literal['minds', 'feelings', 'senses'] = ''

    @classmethod
    def get_rand_id(
            cls,
            only_positive: bool = False,
            only_negative: bool = False,
            num: int = 1
    ) -> list[Emotion]:
        """
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
            FROM {cls._TABLE_NAME}
            {where_clause}
            ORDER BY RANDOM()
            LIMIT {num}
        '''

        ids = db_connect(query)

        return [Emotion(id[0], cls._TABLE_NAME) for id in ids]
