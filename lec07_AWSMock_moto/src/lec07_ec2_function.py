import boto3


def describe_ec2() -> None:
    """
    EC2をDescribeし、インスダンスIDを出力する
    """
    ec2 = boto3.client('ec2')
    # インスタンスIDを取得
    image_response = ec2.describe_images()
    image_id = image_response['Images'][0]['ImageId']
    print(image_id)