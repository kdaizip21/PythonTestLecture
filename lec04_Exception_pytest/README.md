# 例外のテスト
## Lecture03の結果の振り返り

- 実行結果

    ```shell script
    Name                         Stmts   Miss  Cover   Missing
    ----------------------------------------------------------
    src\__init__.py                  0      0   100%
    src\lec03_function.py            6      1    83%   11
    src\test_lec03_function.py       4      0   100%
    ----------------------------------------------------------
    TOTAL                           10      1    90%
    
    ```

- Missingが11行目に発生している
    ```python
    1 def add_num_and_double(num1: int, num2: int) -> int:
    2     """
    3     足して2倍して返す
    4     :param num1: 変数１
    5     :param num2: 変数２
    6     :return: 返り値
    7     """
    8
    9    # 入力がint型でない場合、ValueErrorを返す
    10    if type(num1) is not int or type(num2) is not int:
    11        raise ValueError
    12
    13    result: int = num1 + num2
    14    result *= 2
    15    return result
    ```
  
- 例外`raise`のテスト方法は通常とは異なるため、解説する


## 例外のテスト方法
- raise ValueErrorがかかるようにテストを記述する。
- 例外テストの仕方
    1. pytestをインポート
    2. pytestのraisesメソッドで評価する
    3. raisesメソッドはwithステートメントで利用する

- `test_lec04_function.py`    
    ```python
    # pytestをインポート
    import pytest
    
    from .lec04_function import add_num_and_double
    
    
    def test_add_num_and_double():
        result = add_num_and_double(2, 3)
    
        assert result == 10
    
    # 例外テストを追加する
    def test_add_num_and_double_raise():
        # withステートメントのpytest.raisesでエクセプション評価する
        with pytest.raises(ValueError):
            add_num_and_double("String", "String")
    ```

- 実行

    ```shell script
    $ pytest --cov=. --cov-report=term-missing --cov-branch
    ```

    - 例外も含めて、全てテストがパスできている

    ```shell script
    ----------- coverage: platform win32, python 3.8.6-final-0 -----------
    Name                         Stmts   Miss Branch BrPart  Cover   Missing
    ------------------------------------------------------------------------
    src\__init__.py                  0      0      0      0   100%
    src\lec04_function.py            6      0      2      0   100%
    src\test_lec04_function.py       8      0      0      0   100%
    ------------------------------------------------------------------------
    TOTAL                           14      0      2      0   100%
    ```
