# Test Coverage テスト網羅率　

- テストがどの程度行われたかを図る指標

## カバレッジ基準
- 下記サイトが良くまとまっているので参照すると良い    
    [ホワイトボックステストにおけるカバレッジとテストケース(C0, C1, C2, CDC, MC/DC, MCC)](https://dlrecord.hatenablog.com/entry/2020/04/29/201223#%E6%9D%A1%E4%BB%B6%E7%B6%B2%E7%BE%85--condition-coverageC2)


| Code | 名称         | Name               | テスト設計方針                                              |
| ---- | ------------ | ------------------ | ----------------------------------------------------------- |
| C0   | 命令網羅     | Statement Coverage | それぞれの命令文が、少なくとも1回は実行される                |
| C1   | 分岐網羅 | Decision Coverage  | それぞれの判定条件における真偽が、少なくとも1回は実行される |
| C2   | 条件網羅     | Condition Coverage | それぞれの条件文における真偽が、少なくとも1回は実行される   |



- C0 / C1 / C2 はどこが `命令`でどこが`分岐`でどこが`条件`かがわかると理解しやすい
- 下記のサンプルコードの場合
    ```python
    def sample(num):
        if num > 0 or num < 100:
            num = -num
            
        else:
            num = num * 10
            
        return num
    ```

- 命令、条件、判定は下記のようになる
    ```python
    def sample(num):
        if 条件:  ← 分岐
            命令
            
        else:    ← 分岐
            命令
            
        return num
    ```
    - 下記の理解で大体OK
        - 命令：処理
        - 分岐：if else処理
        - 条件：==, != , < , > など
        
        
 
 # pytest-covによるカバレッジ算出
 - `pytest-cov`を使うことでpytestにおいてカバレッジ算出ができる
 - ただし、できるのはC0、C1までで、C2の算出はできない
 
 ## pytst-covのインストール
```shell script
$ pip install pytest-cov pytest-xdist
```

## 実行方法
### C0カバレッジ算出
- 一番基本的な算出
    - 使用するのはlec02で使用した関数とテストコード
```shell script
# 使い方
$ pytest テストコード.py --cov=パッケージ名（.pyはなし）

# カレントディレクトリ以下のテストテストをまとめて実施（これで十分）
$ pytest --cov=.
```


- 実行結果
```shell script
# 略
----------- coverage: platform win32, python 3.8.6-final-0 -----------
Name                         Stmts   Miss  Cover
------------------------------------------------
src\__init__.py                  0      0   100%
src\lec03_function.py            6      1    83%
src\test_lec03_function.py       4      0   100%
------------------------------------------------
TOTAL                           10      1    90%
```
    - 対象は`src\lec03_function.py`だけ。（フォルダ構成が良くないため、全部でちゃってるのは勘弁）

- 内容の説明

    | 項目名 | 内容                     | 
    | ------ | ------------------------ | 
    | Stmts  | 実行対象コード全体の行数 |  
    | Miss   | 網羅できなかった行数     |   
    | Cover  | カバレッジ率             |    


- `Miss`がどこかをチェックする
    
    ```shell script
    # --cov-report=term-missingをつけることで、missの行番号が出る
    $ pytest --cov=. --cov-report=term-missing
    ```
    
    ```shell script
    Name                         Stmts   Miss  Cover   Missing
    ----------------------------------------------------------
    src\__init__.py                  0      0   100%
    src\lec03_function.py            6      1    83%   11
    src\test_lec03_function.py       4      0   100%
    ----------------------------------------------------------
    TOTAL                           10      1    90%
    
    ```
        
    | 項目名 | 内容                     | 
    | ------ | ------------------------ | 
    | Stmts  | 実行対象コード全体の行数 |  
    | Miss   | 網羅できなかった行数     |   
    | Cover  | カバレッジ率             |   
    | Missing  | Missがでた行番号             |   
    
    
    
 - 解説
    - Missingが11行目に発生している
     ```python
    1 def add_num_and_double(num1: int, num2: int) -> int:
    2     """
    3     足して2倍して返す
    4     :param num1: 変数１
    5     :param num2: 変数２
    6     :return: 返り値
    7     """
    8
    9    # 入力がint型でない場合、ValueErrorを返す
    10    if type(num1) is not int or type(num2) is not int:
    11        raise ValueError
    12
    13    result: int = num1 + num2
    14    result *= 2
    15    return result
    ```

    - 下記のテストコードでは`ValueError`がチェックできていない
    
    ```python
    from .lec03_function import add_num_and_double
    
    
    def test_add_num_and_double():
        result = add_num_and_double(2, 3)
    
        assert result == 10
    ```


### C1カバレッジ算出

- `--cov-branch`オプションでC1分岐のチェックができる
    ```shell script
    # --cov-branchをつける
    $ pytest --cov=. --cov-report=term-missing　--cov-branch
    ```

- 実行結果
    ```shell script
    ----------- coverage: platform win32, python 3.8.6-final-0 -----------
    Name                         Stmts   Miss Branch BrPart  Cover   Missing
    ------------------------------------------------------------------------
    src\__init__.py                  0      0      0      0   100%
    src\lec03_function.py            6      1      2      1    75%   11
    src\test_lec03_function.py       4      0      0      0   100%
    ------------------------------------------------------------------------
    TOTAL                           10      1      2      1    83%
    ```
    - `Branch`と`BrPart`が出てきて、分岐チェックが見れる
    - このときの`Cover`はC1カバレッジが出る（`--cov-branch`オプションなしでは83%だった）
        
    | 項目名 | 内容                     | 
    | ------ | ------------------------ | 
    | Stmts  | 実行対象コード全体の行数 |  
    | Miss   | 網羅できなかった行数     |   
    | Branch  | 分岐の数（IF文の数のイメージ）             |   
    | BrPart  | 通っていない分岐の数             |   
    | Cover  | カバレッジ率             |   
    | Missing  | Missがでた行番号             |   
    
    
 ### 実行結果をHTMLで出力し、そのままレポートに
 
 - `--cov-report=html`オプションをつけると、HTMLでレポートが出る
 
     ```shell script
    $ pytest --cov=. --cov-report=term-missing --cov-branch --cov-report=html
    ```

- `htmlcov`フォルダができ、`index.html`を見るとそのままレポートになっている


### その他のオプション
- 公式サイト参照    
    https://pytest-cov.readthedocs.io/en/latest/index.html

