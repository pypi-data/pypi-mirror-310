from chinus_emotions.src.main.db.db_connect import db_connect


class PrintableStr(str):
    """
    바로 출력할 수 있는 str 타입 \n
    .print()로 바로 출력
    """

    def print(self):
        print(self)


class Emotion:

    def __init__(self, id: int, table_name: str):
        self._id = id
        self._table_name = table_name

    def get_id(self) -> int:
        """
        :return: id(pk)
        """
        return int(self._id)

    def get_word(self) -> PrintableStr:
        """
        id에 해당하는 단어 리턴 \n
        .print()쓰면 결과 바로 출력

        :return: str

        :raise KeyError: 유효하지 않은 id 일 때
        """

        query = f'''
            SELECT word
            FROM {self._table_name}
            WHERE id = {self._id}
            '''

        word = db_connect(query)

        return PrintableStr(word[0][0])

    def get_mean(self) -> PrintableStr:
        """
        id에 해당하는 단어의 뜻 리턴 \n
        .print()쓰면 결과 바로 출력

        :return: str

        :raise KeyError: 유효하지 않은 id 일 때
        """

        query = f'''
            SELECT mean
            FROM {self._table_name}
            WHERE id = {self._id}
            '''

        word = db_connect(query)

        return PrintableStr(word[0][0])
