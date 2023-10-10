import pytest
import boto3
from moto import mock_ec2
from .lec07_ec2_function import describe_ec2


@mock_ec2
def test_describe_ec2():
    # EC2クライアントを作成
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # EC2インスタンスを作成(mock)
    instance = ec2.run_instances(ImageId='ami-12345678', MinCount=1, MaxCount=1)['Instances'][0]
    instance_id = instance['InstanceId']

    # AMIを作成(mock)
    ec2.create_image(InstanceId=instance_id, Name='Test Image')

    # mockで作成したEC2から最新のAMIのIDを取得
    images_response = ec2.describe_images()
    latest_image_id = images_response['Images'][0]['ImageId']

    # テストしたい関数であるdescribe_ec2関数を呼び出す
    returned_image_id = describe_ec2()

    # 返されたイメージIDを検証
    assert returned_image_id == latest_image_id