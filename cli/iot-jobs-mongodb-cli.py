# -*- coding: utf-8 -*-

from openapi_client import ApiClient, Configuration
from openapi_client.api import MongodbApi
from openapi_client.models import PostCollectionsRequest


configuration = Configuration(
    host="http://127.0.0.1:8000"
)

api_client = ApiClient(
    configuration=configuration
)

mongodb_api = MongodbApi(
    api_client=api_client
)
