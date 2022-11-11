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
