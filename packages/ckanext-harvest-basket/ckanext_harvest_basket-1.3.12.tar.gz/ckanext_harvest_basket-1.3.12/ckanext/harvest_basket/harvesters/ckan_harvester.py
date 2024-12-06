import json
import logging

from ckanext.harvest.harvesters import CKANHarvester
from ckanext.harvest.harvesters.ckanharvester import SearchError
from ckanext.harvest_basket.harvesters.base_harvester import \
    BasketBasicHarvester
from ckanext.transmute.utils import get_schema

import ckan.plugins.toolkit as tk
from ckan import model

log = logging.getLogger(__name__)


class CustomCKANHarvester(CKANHarvester, BasketBasicHarvester):
    SRC_ID = "CKAN"

    def import_stage(self, harvest_object):
        package_dict = json.loads(harvest_object.content)
        self._set_config(harvest_object.source.config)

        self._transmute_content(package_dict)

        harvest_object.content = json.dumps(package_dict)
        super().import_stage(harvest_object)

    def _search_for_datasets(self, remote_ckan_base_url, fq_terms=None):
        if fq_terms is None:
            fq_terms = []
        if fq := self.config.get("fq" ,""):
            fq_terms.append(fq)

        pkg_dicts = super()._search_for_datasets(remote_ckan_base_url, fq_terms)
        max_datasets = int(self.config.get("max_datasets", 0))
        return pkg_dicts[:max_datasets] if max_datasets else pkg_dicts

    def _search_datasets(self, remote_url: str):
        url = remote_url.rstrip("/") + "/api/action/package_search?rows=1"
        resp = self._make_request(url)

        if not resp:
            return

        try:
            package_dict = json.loads(resp.text)["result"]["results"]
        except (ValueError, KeyError) as e:
            err_msg: str = f"{self.SRC_ID}: response JSON doesn't contain result: {e}"
            log.error(err_msg)
            raise SearchError(err_msg)

        return package_dict

    def fetch_stage(self, harvest_object):
        data_dict = json.loads(harvest_object.content)
        data_dict["type"] = "dataset"
        harvest_object.content = json.dumps(data_dict)
        return super().fetch_stage(harvest_object)

    def _pre_map_stage(self, data_dict, source_url):
        data_dict["type initial"] = data_dict["type"]
        data_dict["type"] = "dataset"
        return data_dict

    def transmute_data(self, data, schema):
        if schema:
            tk.get_action("tsm_transmute")(
                {
                    "model": model,
                    "session": model.Session,
                    "user": self._get_user_name(),
                },
                {"data": data, "schema": schema},
            )
