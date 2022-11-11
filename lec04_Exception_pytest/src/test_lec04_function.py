# pytestをインポート
import pytest

from .lec04_function import add_num_and_double


def test_add_num_and_double():
    result = add_num_and_double(2, 3)

    assert result == 10


def test_add_num_and_double_raise():
    # withステートメントのpytest.raisesでエクセプション評価する
    with pytest.raises(ValueError):
        add_num_and_double("String", "String")
