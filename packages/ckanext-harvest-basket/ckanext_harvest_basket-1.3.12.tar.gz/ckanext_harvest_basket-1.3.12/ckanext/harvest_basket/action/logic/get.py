from __future__ import annotations

import json
from typing import Any, Optional

from ckanext.harvest_basket.harvesters import (ArcGISHarvester,
                                               CustomCKANHarvester,
                                               DKANHarvester, JunarHarvester,
                                               ODSHarvester, SocrataHarvester)
from ckanext.transmute.utils import get_json_schema
from jsonschema import ValidationError as SchemaValidationError
from jsonschema import validate

import ckan.plugins.toolkit as tk


@tk.side_effect_free
def check_source(ctx: dict[str, Any], data_dict: dict) -> dict[str, Any]:
    tk.check_access("harvest_basket_check_source", ctx, data_dict)

    source_name: str = tk.get_or_bust(data_dict, "source_name")
    source_url: Optional[str] = data_dict.get("source_url")
    config: dict = json.loads(data_dict.get("config", "").strip() or "{}")

    if not source_url:
        raise tk.ValidationError(f"The source URL must be provided to make a checkup")

    sources = {
        "dkan": DKANHarvester,
        "junar": JunarHarvester,
        "socrata": SocrataHarvester,
        "arcgis": ArcGISHarvester,
        "ckan": CustomCKANHarvester,
        "ods": ODSHarvester,
    }

    harvester_class = sources.get(source_name)

    if not harvester_class:
        raise tk.ValidationError(
            f"The source checkup for type `{source_name}` not implemented"
        )

    return harvester_class().make_checkup(source_url, source_name, config)


@tk.side_effect_free
def update_config(ctx: dict[str, Any], data_dict: dict) -> dict[str, Any]:
    tk.check_access("harvest_basket_update_config", ctx, data_dict)

    config_content: str = tk.get_or_bust(data_dict, "config")

    try:
        config: dict = json.loads(config_content)
    except ValueError as e:
        return str(e)

    schema = get_json_schema()

    try:
        validate(config, schema)
    except SchemaValidationError as e:
        return f"{e.message}"
