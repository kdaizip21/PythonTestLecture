import pytest
import boto3
from moto import mock_ec2
from .lec07_ec2_function import describe_ec2


@mock_ec2
def test_start_instance():
    ec2 = boto3.client('ec2')
    # EC2を作成
    ec2.run_instances(
        ImageId='testImage',
        MinCount=1,
        MaxCount=1,
        KeyName="ec2-1",
        TagSpecifications=[{'ResourceType': 'instance',
                            'Tags': [{'Key': 'Name', 'Value': 'ec2-1'}]}])
    # appファイルを実行

    describe_ec2()
