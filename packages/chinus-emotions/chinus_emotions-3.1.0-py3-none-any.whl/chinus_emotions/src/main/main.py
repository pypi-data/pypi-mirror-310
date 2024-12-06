from chinus_emotions.src.main.classes.emotion import Emotion


class Minds(Emotion):
    """
    emotions.db의 minds 테이블의 랜덤 row
    :ivar id: 아이디
    :ivar word: 단어
    :ivar mean: 단어의 뜻
    """


class Feelings(Emotion):
    """
    emotions.db의 feelings 테이블의 랜덤 row
    :ivar id: 아이디
    :ivar word: 단어
    :ivar mean: 단어의 뜻
    """


class Senses(Emotion):
    """
    emotions.db의 senses 테이블의 랜덤 row
    :ivar id: 아이디
    :ivar word: 단어
    :ivar mean: 단어의 뜻
    """



if __name__ == '__main__':
    a = Minds()