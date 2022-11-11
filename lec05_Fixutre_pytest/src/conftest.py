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
