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
