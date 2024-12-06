from chinus_emotions.src.main.db.db_connect import db_connect


class PrintableStr(str):
    """
    바로 출력할 수 있는 str
    """

    def print(self):
        print(self)


class Emotion:

    def __init__(
            self,
            only_positive: bool = False,
            only_negative: bool = False
    ):
        self.id: int
        self.word: PrintableStr
        self.mean: PrintableStr
        self._set_init_vars(only_positive, only_negative)

    def _set_init_vars(self, only_positive, only_negative):
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
            SELECT id, word, mean
            FROM {type(self).__name__.lower()}
            {where_clause}
            ORDER BY RANDOM()
            LIMIT 1
        '''

        self.id, word, mean = db_connect(query)[0]
        self.word = PrintableStr(word)
        self.mean = PrintableStr(mean)
