from .lec06_function import request_status_code

def test_request_status_code_mock_return_value(mocker):
    status_code = 200
    url = "https://example.com"
    
    # Mock化して、status_code=200 を返すようにする
    mocker.patch('src.lec06_function.request_status_code', return_value=status_code)
    
    assert request_status_code(url) == status_code