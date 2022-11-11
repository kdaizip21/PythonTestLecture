 # moto
## motoとは
- AWSサービスのmockを生成してくれる、サードパーティ製ライブラリ
- EC2, ECS, S3 等かなり多くのサービスをmock化することができる（全てではない）    
    - Git : https://github.com/spulec/moto     
    - Doc : http://docs.getmoto.org/en/latest/
    
 
## インストール
```shell script
$ pip install moto
```

## motoの基本的な使い方
- `from moto import mock_xxxxxx` でmock化したいAWSリソースのmock化ライブラリをimport
    - import するものは公式サイト参照
- `@mock_xxxxx`のデコレータをつけ、AWSリソースを操作する
    - mock化された仮想のEC2を立ち上げる
    - mock化された仮想のDynamoDBに仮想のレコードを入れる
    - mock化された仮想のS3にファイルをputする
    
## 操作例
- ここで記載する操作例はごく一部
- 公式サイトやネットにたくさん情報があふれているた、参考にすること

### EC2のmock例
- プロダクトコード
    - EC2をDescribeして、インスタンスIDをプリントするだけの関数
    
    ```python
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
    ```


- テストコード
    - `@mock_ec2`の中でEC2を立ち上げ、decribe_ec2関数を呼び出しテスト
    ```python
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
    ```
  
  
### S3のmock例

- プロダクトコード
    - S3に対するアップロード関数、ダウンロード関数  
    ```python
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
    ```
  
- テストコード
    - `@mock_s3`の中でS3バケットを作成し、アップロード関数、ダウンロード関数をテスト
    ```python
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
        assert upload_to_bucket("src/data/example.txt", test_bucket, "example.txt")
    
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
    ```
  
  
### 注意
- EC2関連のmotoで下記のwarningが出る場合があるが、無視して良い（そのうち改善される）
> Use ec2_backend.describe_images() to find suitable image for your test

- warningは`--disable-warnings`オプションで無効化（非表示）できる
    ```shell script
    $ pytest --disable-warnings
    ```