"""opendota tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_opendota.streams import (
    HeroesStream,
    MatchDetailStream,
    PlayerMatchesStream,
    opendotaStream
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    HeroesStream,
    PlayerMatchesStream,
    MatchDetailStream
]


class Tapopendota(Tap):
    """opendota tap class."""
    name = "tap-opendota"

    config_jsonschema = th.PropertiesList(
        th.Property("api_key", th.StringType, required=False),
        th.Property("api_url", th.StringType, default="https://api.opendota.com/api/"),
        th.Property("account_id", th.StringType, default=None, required=True),
        th.Property("match_limit", th.StringType, default='10', required=True)
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
