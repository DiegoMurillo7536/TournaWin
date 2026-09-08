"""Typed boto3 client factories.

Every client is built through here so the Floci endpoint override lives in exactly one
place. When ``aws_endpoint_url`` is ``None`` boto3 falls back to real AWS endpoints.
"""

from typing import TYPE_CHECKING

import boto3

from tournament.config import get_settings

if TYPE_CHECKING:
    from mypy_boto3_lambda.client import LambdaClient
    from mypy_boto3_s3.client import S3Client
    from mypy_boto3_sqs.client import SQSClient


def s3_client() -> "S3Client":
    settings = get_settings()
    return boto3.client(
        "s3",
        region_name=settings.aws_default_region,
        endpoint_url=settings.aws_endpoint_url,
    )


def sqs_client() -> "SQSClient":
    settings = get_settings()
    return boto3.client(
        "sqs",
        region_name=settings.aws_default_region,
        endpoint_url=settings.aws_endpoint_url,
    )


def lambda_client() -> "LambdaClient":
    settings = get_settings()
    return boto3.client(
        "lambda",
        region_name=settings.aws_default_region,
        endpoint_url=settings.aws_endpoint_url,
    )
