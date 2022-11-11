def greeting_without_type_hint(name):
    """
    型ヒントなし記述。
    mypyでは無視される
    """
    return 'Hello ' + name


def greeting_with_type_hint(name: str) -> str:
    """
    型ヒントあり記述。
    mypyでチェックされる
    """
    return 'Hello ' + name
#
#
# # 1. name: str に文字列を入れる場合
# greeting_with_type_hint("test")
#
# # 2. name: str にintを入れる場合
# greeting_with_type_hint(10)
#
# # 3. name: str にバイト型を入れる場合
# greeting_with_type_hint(b'greeting_with_type_hint')


# def greeting_with_no_return(name: str) -> None:
#     """
#     何も返さない関数
#     """
#     print('hello' + name)
#
#
# # 返り値(return)が無い関数の値を入れようとしてもエラーが出る
# no_return = greeting_with_no_return("Bill")


# def different_type(num: int):
#     """
#     型計算間違い
#     """
#     return num + 'x'


#
# mypy --ignore-missing-imports
# import boto3
# import numpy
