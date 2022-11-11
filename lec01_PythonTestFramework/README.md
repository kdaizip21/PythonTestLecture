# Python でのテスト
- 福元はPythonしかかけないので、Python以外は誰か別の人が書いて

## Python Test Framework
- Pythonは単体テストを書くためのフレームワークがいくつか存在する
- 標準の`Unittest`か、`Pytest`が一般的
- 詳細は[Tatami Wiki](https://dev-growi.aw-connected.com/TecInfo/00.Python_Programing/08.%E3%83%86%E3%82%B9%E3%83%88)参照




| フレームワーク | 説明・用途                                                                                                                                    |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| [doctest](/TecInfo/00.Python_Programing/08.テスト/01.doctest)        | [docstring](/TecInfo/00.Python_Programing/02.制御フロー/11.Docstrings～関数の説明書～)を利用した簡易テスト。<br>テストというより関数/クラスの説明で使われる                                                                    |
| [Unittest](/TecInfo/00.Python_Programing/08.テスト/02.Unittest)       | Pythonの標準ライブラリ。 <br>書き方が少し難しいが、他の言語のテストフレームワークの書き方と類似しているため、複数言語を扱うエンジニアには良い |
| [pytest](/TecInfo/00.Python_Programing/08.テスト/03.pytest)         | サードパーティライブラリ。<br>Pythonでのテストフレームワークとしては主流。unittestより書きやすい                                                  |
| nose               | 過去主流だったが、今はあまり出てこない                                                                                                                                              |



- 本ドキュメントでは、`pytest`を例にすすめる


# テスト用語
- Pythonとは限らないテスト用語の整理

## Mock
### mockとは？
- mockとは、テストに必要な部品の値を擬似的に設定するもの
- 外部連携（APIを叩くとか）するプログラムでは、自分自身だけでテストが完結しない場合にmockで外部を擬似化する
    - ある外部のAPIをコールする処理があるが、まだAPI側が未完成なため、擬似的にAPIで値をとってきたものとする。
    - 別チームが開発するクラスを呼び出す処理があるが、まだ未完成なため、擬似的に応答結果を返す
    ![image](./pic/mock.png)


### stubとは？
- テストに必要なデータをダミーで生成してくれるもの
    - 定義上mockとは異なるが、ダミーをしてくれるという点では同じ

    ![image](./pic/stub.png)



### Pythonのmock
- unittestに含まれる`MagicMock`
- Pytest拡張の`pytest-mock`


### AWSのMock（Python）
- AWSのリソース操作はすべてAPIベースになる
- そのため、AWS操作するプログラムでのテストはAWS リソースをmock化する必要がある。
- AWSリソースのmock化は下記がある

| ライブラリ                      | 概要                                                                  | メリット                                                | デメリット                                                         |
| ------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------ |
| MagicMock(unittest) pytest-mock | 通常のmockライブラリで AWSリソースをmock化する                        | 自分で実装するため どんな方法でもmock化できる           | AWSリソースの種類は膨大なため、 mock化は非常に面倒で大変           |
| motoライブラリ                  | Python用 AWSリソース専用 mockライブラリhttps://github.com/spulec/moto | 非常に簡単にmock化できる                                | mock化できるAWSリソースはすべてではない                            |


## FAKE
- mockのようなダミーではなく、実環境とほぼ同じ環境を別に用意してテストする。
- ローカルマシンにRDBを構築し、そのRDBを使ってテストする

### AWSのFAKE
- localstack    
  https://github.com/localstack/localstack
  
    - 自分のローカルにAWSリソースを再現する
    - S3、Dynamoなど、一部のリソースを 本物と同じように扱える
    - マシンスペック必要、LocalマシンのOS依存、 CICD化の際、自動化が面倒