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