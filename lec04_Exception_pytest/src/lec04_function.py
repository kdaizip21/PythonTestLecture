def add_num_and_double(num1: int, num2: int) -> int:
    """
    足して2倍して返す
    :param num1: 変数１
    :param num2: 変数２
    :return: 返り値
    """

    # 入力がint型でない場合、ValueErrorを返す
    if type(num1) is not int or type(num2) is not int:
        raise ValueError

    result: int = num1 + num2
    result *= 2
    return result
