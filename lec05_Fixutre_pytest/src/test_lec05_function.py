import pytest

from .lec05_function import check_file_exist


def test_check_file_exist(create_file_and_return_path):
    assert check_file_exist(create_file_and_return_path)
