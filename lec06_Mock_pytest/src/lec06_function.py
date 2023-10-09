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