# pytestのインストール
- pipでインストールするだけ
```sh
$ pip install pytest
```

- インストール確認
```sh
$ pytest --version
pytest 6.2.4
```

# pytestの開始
## テストする関数を準備する
- サンプルとして簡単な関数を用意
    - `lec02_funciton.py`を用意
```python
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
```
- 2つの変数を足して２倍するだけの関数
 
## テストすること
- `add_num_add_double`関数に
    - `2`と`3`を入力し、`10`が帰ってくればテスト成功

### テストコードの記述方法
1. ファイル名は `test_対象のパッケージ名.py`とする。
2. テスト対象のモジュールをimpotする
3. テスト関数・メソッド名は`test_テスト対象の関数・メソッド名`とする。
    - pytestは`test_`で定義された関数、メソッドをテスト対象であると認識する 
    - `test_`がクラスの外、クラスの中どちらであってもテストしてくれる
4. `assert`文の条件が成立しているかどうかをpytestは判断する

```python
from .lec02_function import add_num_and_double


def test_add_num_and_double():
    result = add_num_and_double(2, 3)

    assert result == 10
```


### テストの実行
- `pytest`コマンドで実行

```shell
$ pytest test_lec02_function.py
===================================================================================================== test session starts ======================================================================================================
platform win32 -- Python 3.9.4, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: D:\Develop\Study\Testing
plugins: anyio-3.2.1
collected 1 item                                                                                                                                                                                                                

02_Start_pytest\test_sample_function.py .                                                                                                                                                                                 [100%]

====================================================================================================== 1 passed in 0.05s =======================================================================================================
```

- `collected 1 item` : テストコードが1件見つかった
- `02_Start_pytest\test_sample_function.py . ` : 対象のテストコード
- `1 passed in 0.05s`  : 1件問題なくパスした


### テストの実行（テストが通らない例）
- 参考として、テストが通らないようにテストコードを書き直す
    - エラーの再現のためであり、実際はこんなことはしない
        - assert文に成立しない条件を書くことはない 
    
```python
from .lec02_function import add_num_and_double


def test_add_num_and_double():
    result = add_num_and_double(2, 3)

    assert result == 15
```


- pytest実行結果
```shell
$ pytest test_lec02_function.py
===================================================================================================== test session starts ======================================================================================================
platform win32 -- Python 3.9.4, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: D:\Develop\Study\Testing
plugins: anyio-3.2.1
collected 1 item                                                                                                                                                                                                                

02_Start_pytest\test_sample_function.py F                                                                                                                                                                                 [100%]

=========================================================================================================== FAILURES ===========================================================================================================
___________________________________________________________________________________________________ test_add_num_and_double ____________________________________________________________________________________________________

    def test_add_num_and_double():
        result = add_num_and_double(2, 3)

>       assert result == 15
E       assert 10 == 15

02_Start_pytest\test_sample_function.py:7: AssertionError
=================================================================================================== short test summary info ====================================================================================================
FAILED 02_Start_pytest/test_sample_function.py::test_add_num_and_double - assert 10 == 15
====================================================================================================== 1 failed in 0.21s =======================================================================================================

```

- どこでテスト失敗か、内容が分かるようになっている
    ```shell
    >       assert result == 15
    E       assert 10 == 15
    
    02_Start_pytest\test_sample_function.py:7: AssertionError
    =================================================================================================== short test summary info ====================================================================================================
    FAILED 02_Start_pytest/test_sample_function.py::test_add_num_and_double - assert 10 == 15
    ```


### Assert
#### `assert`での評価式はPythonで表現できる条件式すべてが対応する
- どんな対象でも条件式がかければ評価可能
    ```python
    # 辞書内に特定のkeyがあることを評価
    assert dict in 'key'
    ```
    
    ```python
    # bool判定
    assert is_ok == True
    ```
    
    ```python
    # 文字列を評価
    assert text_data == "Testing Text Data"
    ```

#### `assert`は複数重ねて評価できる
- その場合、すべてのassertが通らないとOKとはならない
    
    ```python
    assert num == 10
    assert num != 20
    ```
    
    ```python
    # requestでとったデータを評価
    assert response.status_code == 204
    assert response.json() == {"OK": "no content"}
    ```