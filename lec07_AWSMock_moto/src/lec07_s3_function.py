import boto3


def upload_to_bucket(up_file_path: str, bucket_name: str, file_name: str) -> bool:
    """
    S3にローカルファイルをアップロードする関数
    Args:
        up_file_path: アップロードするローカルファイルのパス
        bucket_name: 　S3バケット名
        file_name:     S3プレフィックス名

    Returns: Bool

    """
    s3_client = boto3.client("s3")

    _ = s3_client.upload_file(up_file_path, bucket_name, "data/" + file_name)

    return True


def download_from_bucket(file_name: str, bucket_name, down_file_path: str) -> bool:
    """
    S3からローカルにダウンロードする関数
    Args:
        file_name: S3プレフィックス
        bucket_name: S3バケット名
        down_file_path: ダウンロードパス

    Returns: Bool

    """
    s3_client = boto3.client("s3")

    _ = s3_client.download_file(bucket_name, "data/" + file_name, down_file_path)

    return True
