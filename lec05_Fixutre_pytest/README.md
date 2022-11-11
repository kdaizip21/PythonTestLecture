# Pytest Fixture
- テストを行う際にテスト用の事前準備、事後整理を行いたい時がある
    - テスト用のダミーファイルを作成する
    - テスト用のダミーのデータベーステーブルを作って、ダミーデータを入れる
    - テスト用のダミー環境変数を設定する

## Fixtureとは
- pytest ではこのようにテスト実行のために必要な準備や終了処理が`Fixture`というフレームワークとして組み込まれている
- `unittest`のsetUp/tearDownを高機能化したもの。

## Fixtureのメリット
- Fixtureは外部ファイル`conftest.py`に記載するため、テスト間、エンジニア間で使い回すことができる
    - DBの接続などは誰が書いても一緒
- 通常の関数（メソッド）で書くことができ、通常のテストから容易に呼び出せる

## Fixtureの種類
- 組み込みFixture
  https://docs.pytest.org/en/latest/fixture.html#fixture
  予め用意されたもの（あんまり高度なことはできない）
  
- 独自Fixture
  自由に組み込むことができる（これが普通）
  


# Fixture利用の流れ
1. `conftest.py`にやりたいメソッドを書く
2. メソッドの前にデコレータ`@pytest.fixture`をつける
3. テストコードからメソッドを呼び出す

## Fixtureの使い方例
- ファイルの存在をチェックする ↓関数のユニットテストをする
    ```python
    import os
    
    
    def check_file_exist(filename):
        """
        osライブラリで、ファイルが存在するかどうかをチェックする関数
        """
        return os.path.isfile(filename)
    
    ```
  
  
- `conftest.py`に、一時ファイルの生成とパスを返すFixtureを作成する
    ```python
    import pytest
    
    
    @pytest.fixture
    def create_file_and_return_path():
        # 一時ファイルを作成
        file_path = './test.txt'
        with open(file_path, 'w') as f:
            # 作成したファイルパスを渡す
            return file_path
    
    ```
    - `conftest.py`に書く、`@pytest.fixture`デコレータ書くとどこからでも呼び出せる
    
- テストコードを書く
    - テスト用関数の引数に、fixtureで作成した関数名を入れてあげる

    ```python
    import pytest
    
    from .lec05_function import check_file_exist
    
    
    def test_check_file_exist(create_file_and_return_path):
        assert check_file_exist(create_file_and_return_path)    
    ```    
    
- テストを実行する

```python
$ pytest --cov=. --cov-report=term-missing --cov-branch
```

```shell script
----------- coverage: platform win32, python 3.8.6-final-0 -----------
Name                         Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------
__init__.py                      0      0      0      0   100%
src\__init__.py                  0      0      0      0   100%
src\conftest.py                  6      0      0      0   100%
src\lec05_function.py            3      0      0      0   100%
src\test_lec05_function.py       4      0      0      0   100%
------------------------------------------------------------------------
TOTAL                           13      0      0      0   100%
```



### 後処理
- 上記のやり方だとファイルが残ってしまうので、ファイルを削除するfixtureも一緒に入れる

```python
import os

import pytest


@pytest.fixture
def create_file_and_return_path():
    # 一時ファイルを作成
    file_path = './test.txt'
    with open(file_path, 'w') as f:
        # 作成したファイルパスを渡す

        # return file_path

        yield file_path

    # 一時ファイルを削除
    os.remove(file_path)
```

- `yield`はジェネレータであり、`処理をそこで中断する`事ができる（Pythonの一般機能）
- fixtureで利用する場合、テスト完了後に`yeild`以降が実行される特徴を持つ
    - ファイル削除などのtearDown処理はこのように記載していく
- Pytestでは`yeild`が複数あると、Pytestから怒られる