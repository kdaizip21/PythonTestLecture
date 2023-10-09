
import requests  # requestsモジュールをインポートします。

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
