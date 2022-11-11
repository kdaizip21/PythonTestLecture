import pytest
import boto3
from botocore.exceptions import ClientError
from moto import mock_s3

# テスト対象となる関数
from .lec07_s3_function import upload_to_bucket, download_from_bucket

# mock化するS3バケット名
test_bucket = "moto-example"


@mock_s3
def test_upload_succeed():
    """
    1. ファイルアップロードが正常（True）かどうかを判定
    2. アップロードしたオブジェクトの中身が正常かどうか判定
    """
    # バケットの生成。Boto3通り
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket=test_bucket,
                     CreateBucketConfiguration={
                         'LocationConstraint': 'ap-northeast-1'})

    # ファイルアップロードが正常（True）かどうかを判定
    assert upload_to_bucket("data/example.txt", test_bucket, "example.txt")

    # アップロードされたファイルをGet
    body = s3.Object(test_bucket, "data/example.txt").get()["Body"].read().decode("utf-8")

    # アップロードしたオブジェクトの中身が正常かどうか判定
    assert body == "Hello, world!"


@mock_s3
def test_download_failed():
    """
    download_from_bucketの例外テスト
    ダウンロードファイルがS3に存在しないことを確認
    """
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket=test_bucket,
                     CreateBucketConfiguration={
                         'LocationConstraint': 'ap-northeast-1'})

    # botocoreの例外クラスがスローされる
    with pytest.raises(ClientError):
        download_from_bucket("nonexist.txt", test_bucket, "output/example.txt")
