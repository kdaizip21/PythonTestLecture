from .lec03_function import add_num_and_double


def test_add_num_and_double():
    result = add_num_and_double(2, 3)

    assert result == 10

