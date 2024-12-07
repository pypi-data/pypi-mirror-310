# Copyright (C) 2024 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import typing

import boto3
import botocore

if typing.TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client

from buildgrid.server.cleanup.janitor.config import S3Config


def get_s3_client(config: S3Config) -> "S3Client":
    try:
        return boto3.client(
            "s3",
            endpoint_url=config.endpoint,
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
        )
    except Exception as e:
        raise ValueError("Failed to create an S3 client, check the S3 configuration options.") from e


def check_bucket_versioning(s3_client: "S3Client", bucket: str) -> bool:
    try:
        response = s3_client.get_bucket_versioning(Bucket=bucket)
        return bool(response.get("Status"))
    except botocore.exceptions.ClientError:
        return False


def get_size_range(size: float) -> str:
    # Range in bytes
    size_range_upper_limit = [
        (2000, "0_TO_2000"),
        (4000, "2000_TO_4000"),
        (10000, "4000_TO_10000"),
        (100000, "10000_TO_100000"),
        (1000000, "100000_TO_1000000"),
        (10000000, "1000000_TO_10000000"),
        (100000000, "10000000_TO_100000000"),
        (1000000000, "100000000_TO_1000000000"),
        (2000000000, "1000000000_TO_2000000000"),
    ]
    for limit, size_range in size_range_upper_limit:
        if size < limit:
            return size_range
    return "2000000000_AND_ABOVE"


def get_age_range(age: float) -> str:
    # Range mapping ms to a range of minutes
    age_range_upper_limit = [
        (3600000, "0_TO_60"),
        (21600000, "60_TO_360"),
        (86400000, "360_TO_1440"),
        (172800000, "1440_TO_2880"),
        (604800000, "2880_TO_10080"),
        (1209600000, "10080_TO_20160"),
        (2592000000, "20160_TO_43200"),
    ]
    for limit, age_range in age_range_upper_limit:
        if age < limit:
            return age_range
    return "43200_AND_ABOVE"
