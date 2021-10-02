"""REST client handling, including opendotaStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.typing import NumberType


# SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class opendotaStream(RESTStream):
    """opendota stream class."""

    @property
    def account_id(self) -> str:
        return self.config['account_id']

    @property
    def url_base(self) -> str:
        """
        Returns the API url root from config.
        """
        return self.config['api_url']

    records_jsonpath = "$.*"


    def get_url_params(
        self, 
        context: Optional[dict], 
        next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        return row