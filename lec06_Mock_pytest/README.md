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

def call_url(url):
    """
    便的に用意。request_status_codeを呼び出すだけ
    """
    return request_status_code(url)



def request_status_code(url):
    """
    入力されたURLをgetして、レスポンスコードを返す関数
    """
    try:
        response = requests.get(url)
        return response.status_code

    except Exception:
        return 0
```

### テストコードの準備
1. `call_url`をテストする際、`request_status_code`関数をmock化する
2. `mocker.patch(パッケージ名.クラス名.メソッド名)`で対象をmock化できる
    - クラスなしで、関数名でもOK。mock化したいものを指定するだけ
    
#### 0. mock化して何もしないようにする
- 下記の設定で、`request_status_code`は何もしなくなる
```python
mocker.patch('src.lec06_function.request_status_code')
```    
- 今回の例では`何もしなくなる`とテストができないので紹介だけ


#### 1. mock化して特定の値を返すようにする
- `return_value=`でmock化した関数が好きな返り値を返すようにできる
```python
def test_call_url_mock_return_value(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    
    # mock化して、status_code=200 を返すようにする
    mocker.patch('src.lec06_function.request_status_code', return_value=status_code)
    assert call_url(url) == status_code
```


#### 2. mock化した関数/メソッドが、1回だけ呼ばれたことを確認する
- `assert_called_once()`で1回だけ呼ばれたかどうかをチェックする
- APIコールのテストとかで使われる
```python
def test_call_url_call_onece(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    
    # mockオブジェクトを代入する
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    # mockした関数を1回だけ呼び出す
    call_url(url)
    
    # mock化した関数が1回だけ呼び出されたかどうかをチェック
    mock_obj.assert_called_once()
```

#### 3. mock化した関数/メソッドが、指定された回数だけ呼ばれたことを確認する
- `call_count`

```python
def test_call_url_call_10(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    # 10回コールする
    for _ in range(10):
        call_url(url)

    # call_countで10回呼ばれたかチェック
    assert mock_obj.call_count == 10
```


#### 4. mock化した関数/メソッドが、全く呼ばれていないことを確認する
- `assert_not_called`
```python
def test_call_url_no_call(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    # 一度も呼ばれていないかを確認する
    mock_obj.assert_not_called()
```


#### 5. mock化した関数を、全く別の関数にすげ替える
- side_effectで挿げ替え
- 下記の例はmock化した`request_status_code`を`return_200`関数にすげ替えている

```python
def return_200(url):
    return 200

def test_call_url_side_effect(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code')

    # side_effectで、mock化した関数を別の関数にすげ替える
    mock_obj.side_effect = return_200

    assert call_url(url) == status_code 
```

#### 6. mock化した関数から、例外を出す

```python
# side_effectで例外を指定
mocker.patch('src.lec06_function.request_status_code', side_effect=Exception)

# もしくは
mock_obj = mocker.patch('src.lec06_function.request_status_code')
mymock.side_effect = Exception
```
