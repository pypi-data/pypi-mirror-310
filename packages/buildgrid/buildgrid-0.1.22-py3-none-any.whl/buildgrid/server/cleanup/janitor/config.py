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


import os
from typing import Any, Optional, Union

import yaml
from pydantic import BaseModel, Field

from buildgrid.server.app.settings.parser import string_definitions


class S3Config(BaseModel):
    access_key: str
    bucket_regex: str
    endpoint: str
    path_prefix: str
    hash_prefix_size: int = Field(default=0)
    secret_key: str


class RedisConfig(BaseModel):
    db: Optional[int] = Field(default=None)
    dns_srv_record: Optional[str] = Field(default=None)
    index_prefix: str
    key_batch_size: int
    password: Optional[str] = Field(default=None)
    host: Optional[str] = Field(default=None)
    port: Optional[int] = Field(default=None)
    sentinel_master_name: Optional[str] = Field(default=None)


class JanitorConfig(BaseModel):
    redis: Optional[RedisConfig] = Field(default=None)
    sleep_interval: int
    s3: S3Config
    sql_connection_string: Optional[str] = Field(default=None)


def parse_janitor_config(path: Union[str, bytes, "os.PathLike[str]"]) -> JanitorConfig:
    class Loader(yaml.SafeLoader):
        def string_loader(self, node: yaml.MappingNode) -> Any:
            return string_definitions[node.tag](node.value)

    for kind in string_definitions:
        Loader.add_constructor(kind, Loader.string_loader)

    with open(path) as config_file:
        config = yaml.load(config_file, Loader=Loader)
    return JanitorConfig(**config)
