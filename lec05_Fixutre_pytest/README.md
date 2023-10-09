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
- 


## その他 Fixtureの使用例

### 1. データベース接続のセットアップと終了

```python
# conftest.py
import pytest
import psycopg2

@pytest.fixture
def db_connection():
    conn = psycopg2.connect(database="testdb", user="user", password="pass", host="127.0.0.1", port="5432")
    yield conn  # データベース接続を返します
    conn.close()  # テスト後にデータベース接続を閉じます

# test_db.py
def test_db_query(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result[0] == 1
    cursor.close()
```

### 2. 一時ファイルの作成と削除

```python
# conftest.py
import pytest
import os

@pytest.fixture
def temp_file():
    file_path = './temp.txt'
    with open(file_path, 'w') as file:
        yield file_path  # 一時ファイルのパスを返します。
    os.remove(file_path)  # テスト後に一時ファイルを削除します。

# test_file.py
def test_file_existence(temp_file):
    assert os.path.isfile(temp_file)  # 一時ファイルが存在することを確認します。
```

### 3. 環境変数の設定とクリア

```python
# conftest.py
import pytest
import os

@pytest.fixture
def set_env_var():
    os.environ['TEST_VAR'] = '123'
    yield
    del os.environ['TEST_VAR']  # テスト後に環境変数をクリアします。

# test_env.py
def test_env_var(set_env_var):
    assert os.getenv('TEST_VAR') == '123'  # 環境変数が正しく設定されていることを確認します。
```

### 4. モックオブジェクトの作成とリセット

```python
# conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_object():
    mock = MagicMock()
    yield mock  # モックオブジェクトを返します。
    mock.reset_mock()  # テスト後にモックをリセットします。

# test_mock.py
def test_mock_behavior(mock_object):
    mock_object.do_something()
    mock_object.do_something.assert_called_once()  # モックが呼び出されたことを確認します。
```

### 5. カスタム設定のロードとリセット

```python
# conftest.py
import pytest
import my_config_module

@pytest.fixture
def custom_config():
    original_config = my_config_module.get_config()
    my_config_module.load_config('test_config.json')
    yield
    my_config_module.load_config(original_config)  # テスト後に設定をリセットします。

# test_config.py
def test_custom_config(custom_config):
    config = my_config_module.get_config()
    assert config['setting'] == 'test_value'  # 設定が正しくロードされていることを確認します。
```



## AWSでのFixture
- AWSに対してFixtureすることも可能だが、lec07の `moto`を使うほうが良い

### 1. AWS S3バケットへのアクセステスト

```python
# conftest.py
import pytest
import boto3

@pytest.fixture
def s3_bucket():
    s3 = boto3.client('s3')
    bucket_name = 'test-bucket'
    yield s3, bucket_name  # S3クライアントとバケット名を返します。

# test_s3.py
def test_s3_list_objects(s3_bucket):
    s3, bucket_name = s3_bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    assert 'Contents' in response  # バケット内にオブジェクトが存在することを確認します。
```

### 2. AWS DynamoDBテーブルへのアクセステスト

```python
# conftest.py
import pytest
import boto3

@pytest.fixture
def dynamodb_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = 'test-table'
    table = dynamodb.Table(table_name)
    yield table  # DynamoDBテーブルを返します。

# test_dynamodb.py
def test_dynamodb_get_item(dynamodb_table):
    item = dynamodb_table.get_item(Key={'id': '123'})
    assert 'Item' in item  # アイテムが正しく取得できることを確認します。
```

### 3. AWS Lambda関数の呼び出しテスト

```python
# conftest.py
import pytest
import boto3

@pytest.fixture
def lambda_client():
    client = boto3.client('lambda')
    function_name = 'test-function'
    yield client, function_name  # Lambdaクライアントと関数名を返します。

# test_lambda.py
def test_lambda_invoke(lambda_client):
    client, function_name = lambda_client
    response = client.invoke(FunctionName=function_name, Payload='{"key": "value"}')
    assert response['StatusCode'] == 200  # Lambda関数が正常に呼び出されることを確認します。
```