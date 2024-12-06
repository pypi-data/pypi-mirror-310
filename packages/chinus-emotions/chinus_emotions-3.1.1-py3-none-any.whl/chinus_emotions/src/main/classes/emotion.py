from chinus_emotions.src.main.db.db_connect import db_connect


class PrintableList(list):
    """
    바로 출력할 수 있는 str
    """

    def print(self):
        str_list = ', '.join(map(str, self))
        print(str_list)

    def idx(self, index: int):
        if index >= len(self):
            raise IndexError

        return self[index]


class Emotion:
    def __init__(
            self,
            num: int = 1,
            only_positive: bool = False,
            only_negative: bool = False
    ):
        self.word: PrintableList
        self.mean: PrintableList
        self._set_init_vars(num, only_positive, only_negative)

    def _set_init_vars(self, num, only_positive, only_negative):
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
            SELECT word, mean
            FROM {type(self).__name__.lower()}
            {where_clause}
            ORDER BY RANDOM()
            LIMIT {num}
        '''

        self.word, self.mean = map(lambda x: PrintableList(list(x)), zip(*db_connect(query)))

