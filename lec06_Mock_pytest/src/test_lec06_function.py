from .lec06_function import call_url

def test_call_url_mock_return_value(mocker):
    status_code = 200
    url = "https://hogehoge.com"

    # mock化して、status_code=200 を返すようにする
    mocker.patch('src.lec06_function.request_status_code', return_value=status_code)
    assert call_url(url) == status_code


def test_call_url_call_onece(mocker):
    status_code = 200
    url = "https://hogehoge.com"

    # mockオブジェクトを代入する
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    # mockした関数を1回だけ呼び出す
    call_url(url)

    # mock化した関数が1回だけ呼び出されたかどうかをチェック
    mock_obj.assert_called_once()



def test_call_url_call_10(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    # 10回コールする
    for _ in range(10):
        call_url(url)

    # call_countで10回呼ばれたかチェック
    assert mock_obj.call_count == 10


def test_call_url_no_call(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code', return_value=status_code)

    # 一度も呼ばれていないかを確認する
    mock_obj.assert_not_called()



def return_200(url):
    return 200

def test_call_url_side_effect(mocker):
    status_code = 200
    url = "https://hogehoge.com"
    mock_obj = mocker.patch('src.lec06_function.request_status_code')

    # side_effectで、mock化した関数を別の関数にすげ替える
    mock_obj.side_effect = return_200

    assert call_url(url) == status_code