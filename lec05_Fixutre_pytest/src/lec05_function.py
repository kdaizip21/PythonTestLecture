import os


def check_file_exist(filename):
    """
    osライブラリで、ファイルが存在するかどうかをチェックする関数
    """
    print("\n")
    print(filename)
    return os.path.isfile(filename)
