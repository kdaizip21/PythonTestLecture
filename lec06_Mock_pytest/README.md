# pytest-mock
## （おさらい）mockとは？
- mockとは、テストに必要な部品の値を擬似的に設定するもの
- 外部連携（APIを叩くとか）するプログラムでは、自分自身だけでテストが完結しない場合にmockで外部を擬似化する
    - ある外部のAPIをコールする処理があるが、まだAPI側が未完成なため、擬似的にAPIで値をとってきたものとする。
    - 別チームが開発するクラスを呼び出す処理があるが、まだ未完成なため、擬似的に応答結果を返す
    ![image](../lec01_PythonTestFramework/pic/mock.png)



## pytest用mockライブラリ
```shell script
$ pip install pytest-mock
```

## pytest-mockの実行
### テスト対象

- 入力したURLをGETしてステータスコードを返す関数

```python
import requests

def request_status_code(url):
    """
    指定されたURLにGETリクエストを送信し、ステータスコードを返します。
    """
    try:
        response = requests.get(url)
        return response.status_code
    except Exception:
        return 0
```

## Pytest Mockの基本的な使用方法
- 以下は、外部のAPIを呼び出すrequest_status_code関数を模擬化する簡単な例
- `mocker.patch(パッケージ名.クラス名.メソッド名)`で対象をmock化していく


### 1. **特定の値を返すようにMock化**
```python
def test_request_status_code_mock_return_value(mocker):
    status_code = 200
    url = "https://example.com"
    
    # Mock化して、status_code=200 を返すようにする
    mocker.patch('src.lec06_function.request_status_code', return_value=status_code)
    
    assert request_status_code(url) == status_code
```

### 2. **Mock化した関数が1回だけ呼ばれたことを確認**
```python
def test_request_status_code_call_once(mocker):
    status_code = 200
    url = "https://example.com"
    
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)
    request_status_code(url)
    mock_obj.assert_called_once()
```

### 3. **Mock化した関数が指定された回数だけ呼ばれたことを確認**
```python
def test_request_status_code_call_10(mocker):
    status_code = 200
    url = "https://example.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    for _ in range(10):
        request_status_code(url)
    
    assert mock_obj.call_count == 10
```

### 4. **Mock化した関数が全く呼ばれていないことを確認**
```python
def test_request_status_code_no_call(mocker):
    status_code = 200
    url = "https://example.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    mock_obj.assert_not_called()
```

### 5. **Mock化した関数を別の関数に置き換え**
```python
def return_200(url):
    return 200

def test_request_status_code_side_effect(mocker):
    url = "https://example.com"
    mock_obj = mocker.patch('path.to.request_status_code')

    mock_obj.side_effect = return_200

    assert request_status_code(url) == 200
```

### 6. **Mock化した関数から例外をスロー**
```python
def test_request_status_code_exception(mocker):
    url = "https://example.com"
    mock_obj = mocker.patch('path.to.request_status_code')
    mock_obj.side_effect = Exception

    assert request_status_code(url) == 0
```

