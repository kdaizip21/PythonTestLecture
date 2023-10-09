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

def get_weather_data(city: str) -> dict:
    """
    指定された都市の天気データを取得します。

    Args:
        city (str): 天気データを取得する都市の名前。

    Returns:
        dict: 天気データ。
    """
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY"  # APIのURLを作成します。
    
    # APIにリクエストを送信し、レスポンスを取得する
    response = requests.get(url) 
    
    # レスポンスのステータスコードが200ではない場合、エラーを発生させる
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve data: {response.text}")
    # レスポンスのJSONコンテンツを返す
    return response.json()

```

## Pytest Mockの基本的な使用方法
- 以下は、外部のAPIを呼び出すrequest_status_code関数を模擬化する簡単な例
- `mocker.patch(パッケージ名.クラス名.メソッド名)`で対象をmock化していく


###  **requests.get関数自体をmock化する**
```python
from .lec06_function import get_weather_data

# test_weather.py

import pytest
# from weather import get_weather_data

def test_get_weather_data(mocker):  # mockerフィクスチャを引数として受け取ります。
    """
    get_weather_data関数のテストを実行します。
    """
    
    # weather.requests.get関数をモック化
    mock_get = mocker.patch('src.lec06_function.requests.get')
    
    # モックオブジェクトのstatus_code属性を200に設定
    mock_get.return_value.status_code = 200
    
    # モックオブジェクトのjsonメソッドの戻り値を設定。
    mock_get.return_value.json.return_value = {
        "weather": [{"description": "clear sky"}]
    }

    city = "Tokyo"
    
    # 呼び出されたget_weather_data関数内の requests.get はモック化されており、返り値は上記で設定したものが入る
    data = get_weather_data(city)  
    
    assert data == {"weather": [{"description": "clear sky"}]} 
    
    
    # call_countを使うことで、呼び出せれた回数を確認できる。
    assert mock_get.call_count == 1  
```