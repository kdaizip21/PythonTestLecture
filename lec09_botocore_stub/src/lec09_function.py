import logging
import boto3

# logger = logging.getLogger(__name__)
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
        # logger.error("Unexpected error occurred while getting Parameter, Error=%s", e)
        raise Exception from e

    # 2. パラメータストアのキーがないときの処理
    if not response['Parameters']:
        # logger.error("Parameter Key is not exist")
        raise IndexError

    # 1. のレスポンス
    parameter = response['Parameters'][0]['Value']
    return parameter
