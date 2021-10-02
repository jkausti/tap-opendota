"""Stream type classes for tap-opendota."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
import requests

from singer_sdk import typing as th
from singer_sdk.helpers.jsonpath import extract_jsonpath  # JSON Schema typing helpers

from tap_opendota.client import opendotaStream

# Delete this is if not using json files for schema definition
# SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class HeroesStream(opendotaStream):
    """
    Defining a stream for fetching data about Dota 2 hereos.
    """
    name = 'heroes'
    path = '/constants/heroes'
    primary_keys = ['id']
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.NumberType),
        th.Property("name", th.StringType),
        th.Property("localized_name", th.StringType),
        th.Property("primary_attr", th.StringType),
        th.Property("attack_type", th.StringType),
        th.Property("roles", th.ArrayType(
            wrapped_type=th.StringType
        )),
        th.Property("base_health", th.NumberType),
        th.Property("base_health_regen", th.NumberType),
        th.Property("base_mana", th.NumberType),
        th.Property("base_mana_regen", th.NumberType),
        th.Property("base_armor", th.NumberType),
        th.Property("base_mr", th.NumberType),
        th.Property("base_attack_min", th.NumberType),
        th.Property("base_attack_max", th.NumberType),
        th.Property("base_str", th.NumberType),
        th.Property("base_agi", th.NumberType),
        th.Property("base_int", th.NumberType),
        th.Property("str_gain", th.NumberType),
        th.Property("agi_gain", th.NumberType),
        th.Property("int_gain", th.NumberType),
        th.Property("attack_range", th.NumberType),
        th.Property("projectile_speed", th.NumberType),
        th.Property("attack_rate", th.NumberType),
        th.Property("move_speed", th.NumberType),
        th.Property("turn_rate", th.NumberType),
        th.Property("cm_enabled", th.BooleanType),
        th.Property("legs", th.NumberType),
    ).to_dict()

class PlayerMatchesStream(opendotaStream):
    """
    Fetches recent match data for a player ID.
    """

    @property
    def url_base(self) -> str:
        return f'{super().url_base}players/{super().account_id}'

    @property
    def match_limit(self) -> int:
        """
        Returns the match limit from config.
        """
        return self.config['match_limit']
    
    name = 'playermatches'
    path = '/matches'
    primary_keys = ['match_id']
    replication_key = None
    schema = th.PropertiesList(
        th.Property("match_id", th.NumberType),
        th.Property("player_slot", th.NumberType),
        th.Property("radiant_win", th.BooleanType),
        th.Property("duration", th.NumberType),
        th.Property("game_mode", th.NumberType),
        th.Property("lobby_type", th.NumberType),
        th.Property("hero_id", th.NumberType),
        th.Property("start_time", th.NumberType),
        th.Property("version", th.NumberType),
        th.Property("kills", th.NumberType),
        th.Property("deaths", th.NumberType),
        th.Property("assists", th.NumberType),
        th.Property("skill", th.NumberType),
        th.Property("leaver_status", th.NumberType),
        th.Property("party_size", th.NumberType),
    ).to_dict()



    def get_url_params(
        self, 
        context: Optional[dict], 
        next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        result = super().get_url_params(context, next_page_token)
        result['limit'] = self.match_limit
        return result

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        playermatches_jsonpath = '$[*]'
        yield from extract_jsonpath(playermatches_jsonpath, input=response.json())