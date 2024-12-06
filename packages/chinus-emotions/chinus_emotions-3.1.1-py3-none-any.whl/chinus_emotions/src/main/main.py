from chinus_emotions.src.main.classes.emotion import Emotion


class Minds(Emotion):
    """
    emotions.db의 minds 테이블의 랜덤 row

    생성자 매개변수:
        - num: 갯수
        - only_positive: 긍정적인 것만
        - only_negative: 부정적인 것만

    :ivar word: 단어 리스트
    :ivar mean: 단어의 뜻 리스트
    """


class Feelings(Emotion):
    """
    emotions.db의 feelings 테이블의 랜덤 row

    생성자 매개변수:
        - num: 갯수
        - only_positive: 긍정적인 것만
        - only_negative: 부정적인 것만

    :ivar word: 단어 리스트
    :ivar mean: 단어의 뜻 리스트
    """


class Senses(Emotion):
    """
    emotions.db의 senses 테이블의 랜덤 row

    생성자 매개변수:
        - num: 갯수
        - only_positive: 긍정적인 것만
        - only_negative: 부정적인 것만

    :ivar word: 단어 리스트
    :ivar mean: 단어의 뜻 리스트
    """



if __name__ == '__main__':
    a = Minds(num=3)
    a.mean.idx(0)
    print(a.mean.idx(2))
    print('111')
    a.mean.print()