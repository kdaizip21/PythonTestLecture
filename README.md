# テストコード基礎講座
- テストコードを書くために基本的な知識を記載
- 本ドキュメントはPythonベースで記載してますが、テストコードの考え方はどの言語でも同じです。

## ドキュメントURL
- https://dev-gitlab.aw-connected.com/I32541_FUKUMOTO/Testing
    - 上記URLはどこかのタイミングで非公開とします。 

## 注意点
- 本ドキュメントにおけるテストコードの書き方は、一例になります。
    - テストコードの書き方の自由度が高いためです。ただし書き方は統一してあります
        - `with patch`ではなく`mocker.pathc`で統一　など

- Python3.8を利用していますが、python3.6以上であれば基本的に同じです。

## 講座内容
- Lecture 00：What is Unittest
    - [テスト、特にユニットテストとはなんなのか解説](./lec00_WhatIsUnittest/README.md)

- Lecture 01：Python Test FrameWork
    - [Pythonにおけるテストフレームワークを解説](./lec01_PythonTestFramework/README.md)
    
- Lecture 02 Start Pytest
    - [Pythonのテストレームワークである`Pytest`の解説](./lec02_Start_pytest/README.md)
    
- Lecture 03 Coverage
    - [テストにおけるカバレッジの考え方と`Pytest`での算出方法](./lec03_Coverage_pytest/README.md)
    
- Lecture 04 Exception Test
    - [`Pytest`での例外のテスト方法](./lec04_Exception_pytest/README.md)

- Lecture 05 Fixture
    - [Pytestにおけるテスト準備フレームワーク`Fixture`の解説](./lec05_Fixutre_pytest/README.md)
    
- Lecture 06 Mock
    - [PytestでのMockの立て方を解説](./lec06_Mock_pytest/README.md)

- Lecture 07 AWS Mock moto
    - [PythonのAWS Mockフレームワーク `moto`の解説](./lec07_AWSMock_moto/README.md)
    
- Lecture 08 Localstack
    - [AWSの環境をローカルに再現するモッキングフレームワーク `Localstack`の解説](./lec08_Localstack/README.md)

- Lecture 09 botocore.stub
    - [AWS boto3でのスタブの構築方法の解説](./lec09_botocore_stub/README.md)

- おまけLecture mypy
    - [Pythonにおける型ヒント、型チェックツール`mypy`の解説](./lecxx_mypy/README.md)

## 参考
- Pythonのテストフレームワークの解説は下記も参照してください     
    https://dev-growi.aw-connected.com/TecInfo/00.Python_Programing/08.テスト

- Classmethodのテストに関するオンラインセミナーも参考になります
    - [AKIBA.MAD 実践から学ぶ AWS Lambdaのテスト戦略](https://logmi.jp/events/2626)
    - [AWS Lambdaのテスト戦略を実践から学ぶ #akibamad(Youtube)](https://www.youtube.com/watch?v=QCxqePkRqiQ)




## Author
masataka.fukumoto@aisin.co.jp