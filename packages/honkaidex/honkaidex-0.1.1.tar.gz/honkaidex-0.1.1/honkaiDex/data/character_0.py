from honkaiDex.base.character import BaseCharacter, Battlesuit
import logging
import json
from honkaiDex.data import HONKAIDEX_DATA, load_once
from honkaiDex import config
import os 

@load_once()
def load():

    logging.debug(f"Loading {config.data.character_0.FILENAME}")

    json_data :dict = {}

    with open(os.path.join(HONKAIDEX_DATA, config.data.character_0.FILENAME), "r") as f:
        json_data = json.load(f)

    for character_data in json_data.values():
        character_data : dict
        character = BaseCharacter(
            _name=character_data["name"],
            _nicknames=character_data.get("nicknames", []),
        )


        for bs_data in character_data.get("battlesuit", []):
            bs_data : dict
            bs = Battlesuit(
                _base_character=character,
                _name=bs_data["name"],
                _type=bs_data["type"],
                _version_released=bs_data["version"],
                _rairty=bs_data["rank"],
                _tags=bs_data.get("tags", []),
                _img_link=bs_data.get("img_link", None),
                _else=bs_data.get("else", {}),
            )
