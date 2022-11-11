# botocore.stub 

  
    
## （おさらい）stubとは？
- テストに必要なデータをダミーで生成してくれるもの
    - 定義上mockとは異なるが、ダミーをしてくれるという点では同じ

    ![image](./pic/stub.png)
    
    

## botocore.stubとは
- PythonのAWS SDKであるboto3ライブラリ内で提供されているAWS操作用スタブ
- 公式サイト    
    https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html
- 2021年07月現在、日本語で読めるドキュメントは存在しない
    - [AWS SDK for Ruby　の公式ドキュメント](https://docs.aws.amazon.com/ja_jp/sdk-for-ruby/v3/developer-guide/stubbing.html) が唯一近いものとなる
    
## botocore.stubの使い所
- `moto`や`localstack`では再現できないテストの場合、botocore.stubを使う
    - `moto`、`localstack`が未サポートなAWSサービス
    - 強制的にAWS SDK（Boto3）から例外を出させる場合など
    
- `botocore.stub`の使い方を理解すれば、`moto`、`localstack`は不要となるが、何を使っても良い
    

## botocore.stubの使い方のイメージ
```python
# EC2 の情報をdescribeする処理o
import boto3

ec2 = boto3.client('ec2')
responce = ec2.describe_instances()
```

- この `describe_instances()`関数の返り値を好きなダミーに書き換えて、テストすることとなる

# botocore.stub使い方解説    
## テスト対象のコード
- AWSパラメータストアからパラメータを取得する関数
- テストは以下を実施する
    1. パラメータストアに対象のキーが存在している場合、正常にデータ（Value）が取得できることを確認
        - motoでも可能だが、ここではstubでテストする
    2. パラメータストアに対象のキーが存在しない場合、例外（IndexError）を発生させることができることを確認
        - motoでも可能だが、ここではstubでテストする
    3. それ以外AWS側の異常などの例外が発生した場合、例外（Exception）を発生させることができることを確認
        - motoでは再現ができないため、stubでテストする

```python
import logging
import boto3

logger = logging.getLogger(__name__)
REGION = 'ap-northeast-1'


def get_parameters(param_key: str) -> str:
    """
    パラメータストアからパラメータを取得する
    Args:
        param_key: パラメータキー

    Returns:
        正常時：パラメータ
        エラー時；システム終了
    """
    ssm = boto3.client('ssm', region_name=REGION)

    # 1. 正常に値が取得できるところの処理
    try:
        response = ssm.get_parameters(
            Names=[
                param_key,
            ],
            WithDecryption=True
        )

    # 3. それ以外の異常 get_parameters 自体の異常が発生した場合
    except Exception as e:
        logger.error("Unexpected error occurred while getting Parameter, Error=%s", e)
        raise Exception from e

    # 2. パラメータストアのキーがないときの処理
    if not response['Parameters']:
        logger.error("Parameter Key is not exist")
        raise IndexError

    # 1. のレスポンス
    parameter = response['Parameters'][0]['Value']
    return parameter
```


## 1. パラメータストアに対象のキーが存在している場合、正常にデータ（Value）が取得できることを確認
- 正常系のレスポンスを返すように設定する
- レスポンス内容は公式ドキュメントを参照する。（今回は、ssm.get_parameter() )    
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameters
    
```python
from datetime import datetime

import boto3
from botocore.stub import Stubber
import pytest

from .lec09_function import get_parameters


def test_get_parameters(mocker):
    """
    get_parameters() の正常系テストをbotocore.stubで実施
    """

    # boto3のssm clientのスタブを建てる
    client = boto3.client("ssm")
    stubber = Stubber(client)


    # client.get_parameters の正常系のレスポンスを自分で定義する（
    get_parameters_response = {
        'Parameters': [
            {
                'Name': '========= Input_KEY =========',
                'Type': 'String',
                'Value': '========== Test Result ===========',
                'Version': 123,
                'Selector': 'string',
                'SourceResult': 'string',
                'LastModifiedDate': datetime(2015, 1, 1),
                'ARN': 'string',
                'DataType': 'string'
            },
        ],
        'InvalidParameters': [
            'string',
        ]
    }

    # stubberのレスポンスを定義。　　add_response(ダミー化する関数、ダミーのレスポンス）
    stubber.add_response('get_parameters', get_parameters_response)
    stubber.activate()

    mocker.patch('boto3.client', return_value=client)
    response = get_parameters('========= Input_KEY =========')

    assert response == '========== Test Result ==========='
```

## 2. パラメータストアに対象のキーが存在しない場合、例外（IndexError）を発生させることができることを確認
- 対象にキーがない場合、ssmは `ParametersのValueは長さセロの配列を返す`
    ```json
    {'Parameters': [], xxxxx}
    ```
- この場合に正常に`IndexError`を返すかをテストする

```python
def test_get_parameters_with_nokey(mocker):
    """
    get_parameters() の異常系テストをbotocore.stubで実施
    Keyが存在しない場合の異常系テスト
    """

    # boto3のssm clientのスタブを建てる
    client = boto3.client("ssm")
    stubber = Stubber(client)

    # client.get_parameters の異常系のレスポンスを自分で定義する。
    # この場合の異常は、「Keyが存在しないという」レスポンスがAWSから帰ってくること

    # [Parameters]の中身が空っぽが帰ってくると定義する
    get_parameters_response = {
        'Parameters': [],
        'InvalidParameters': [
            'string',
        ]
    }

    # stubberのレスポンスを定義。　　add_response(ダミー化する関数、ダミーのレスポンス）
    stubber.add_response('get_parameters', get_parameters_response)
    stubber.activate()

    mocker.patch('boto3.client', return_value=client)
    with pytest.raises(IndexError):
        get_parameters('========= Input_KEY =========')
```



### 3. それ以外AWS側の異常などの例外が発生した場合、例外（Exception）を発生させることができることを確認
- Stubberのエラー専用メソッドを利用する `add_client_error`

```python
def test_utilities_get_parameter_with_exception(mocker):
    """
    get_parameters() の異常系テストをbotocore.stubで実施
    その他例外（Exception発生）テスト
    """
    client = boto3.client('ssm')
    stubber = Stubber(client)

    # stubberのレスポンスを定義。　　add_client_error(ダミー化する関数、異常内容）
    stubber.add_client_error('get_parameters', Exception)
    stubber.activate()

    mocker.patch('boto3.client', return_value=client)
    with pytest.raises(Exception):
        get_parameters('xxxxx')

```