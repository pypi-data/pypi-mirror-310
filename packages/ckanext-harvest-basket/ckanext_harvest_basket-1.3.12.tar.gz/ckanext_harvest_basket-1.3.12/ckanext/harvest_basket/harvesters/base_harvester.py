from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime as dt
from html import unescape
from typing import Any, Optional

import requests
from ckanext.harvest.harvesters.base import HarvesterBase
from ckanext.transmute.utils import get_schema
from dateutil import parser
from html2markdown import convert

import ckan.plugins.toolkit as tk
from ckan import model
from ckan.lib.munge import munge_tag
from ckan.plugins import plugin_loaded

try:
    from ckanext.xloader.plugin import XLoaderFormats
except ImportError:
    from ckanext.xloader.utils import XLoaderFormats


log = logging.getLogger(__name__)


class BasketBasicHarvester(HarvesterBase):
    def _datetime_refine(self, string):
        now = dt.now().isoformat()

        # if date stored as timestamp
        try:
            if string and int(string):
                formated_data = dt.fromtimestamp(string).isoformat()
                return formated_data
        except ValueError:
            return now

        # if date stored as string
        if string:
            # some portals returns modified_data with this substring
            if string.startswith("Date changed"):
                string = string[13:]

            try:
                formated_data = parser.parse(string, ignoretz=True).isoformat()
            except ValueError:
                formated_data = now

            return formated_data
        return now

    def _description_refine(self, string):
        if not string:
            return ""
        string = unescape(string)
        return convert(string)

    def _make_request(
        self, url: str, stream: bool = False
    ) -> Optional[requests.Response]:
        resp = None
        err_msg = ""

        try:
            resp = requests.get(url, stream=stream)
        except requests.exceptions.HTTPError as e:
            err_msg = f"{self.SRC_ID}: The HTTP error happend during request {e}"
            log.error(err_msg)
        except requests.exceptions.ConnectTimeout as e:
            err_msg = f"{self.SRC_ID}: Connection timeout: {e}"
            log.error(err_msg)
        except requests.exceptions.ConnectionError as e:
            err_msg = f"{self.SRC_ID}: The Connection error happend during request {e}"
            log.error(err_msg)
        except requests.exceptions.RequestException as e:
            err_msg = f"{self.SRC_ID}: The Request error happend during request {e}"
            log.error(err_msg)

        if resp is None:
            log.error(f"{self.SRC_ID}: {err_msg}")
            return

        if resp.status_code == 200:
            return resp

        err_msg = (
            f"{self.SRC_ID}: Bad response from remote portal: "
            f"{resp.status_code}, {resp.reason}"
        )
        log.error(err_msg)
        raise tk.ValidationError({self.SRC_ID: err_msg})

    def make_checkup(self, source_url: str, source_name: str, config: dict):
        """Makes a test fetch of 1 dataset from the remote source


        Args:
            source_url (str): remote portal URL
            config (dict): config dictionary with some options to adjust
                            harvester (e.g schema, max_datasets, delay)

        Raises:
            tk.ValidationError: raises validation error if the fetch failed
                                returns all the information about endpoint
                                and occured error

        Returns:
                dict: must return a remote dataset meta dict
        """
        self.config = config
        self.config.update(
            {
                "max_datasets": 1,
            }
        )

        self.source_url = source_url
        self.source_type = source_name.title()

        try:
            pkg_dicts = self._search_datasets(source_url)
        except Exception as e:
            raise tk.ValidationError(
                "Checkup failed. Check your source URL \n"
                f"Endpoint we used: {getattr(self, 'url', '')} \n"
                f"Error: {e}"
            )

        if not pkg_dicts:
            return f"No datasets found on remote portal: {source_url}"

        self._pre_map_stage(pkg_dicts[0], source_url)
        return pkg_dicts[0]

    def _set_config(self, config_str):
        if config_str:
            self.config = json.loads(config_str)
        else:
            self.config = {}

        return self.config

    def _fetch_tags(self, tag_list: list[str]) -> list[dict[str, str]]:
        """Converts socrata tags to CKAN

        Args:
                tag_list (list[str]): a list of tag names

        Returns:
                list[dict[str, str]]: a list of tag dicts
        """
        tags = []

        if not tag_list:
            return tags

        for t in tag_list:
            tag = {}
            tag["name"] = munge_tag(t)
            tags.append(tag)

        return tags

    def _transmute_content(self, package_dict: dict[str, Any]):
        schema = self.config.get("tsm_schema")
        if not schema and (schema_name := self.config.get("tsm_named_schema")):
            schema = get_schema(schema_name)
        self.transmute_data(package_dict, schema)

    def import_stage(self, harvest_object):
        self.base_context = {
            "model": model,
            "session": model.Session,
            "user": self._get_user_name(),
        }

        config = self._set_config(harvest_object.source.config)

        if not harvest_object:
            log.error("No harvest object received")
            return False

        if harvest_object.content is None:
            log.error(f"Empty content for object {harvest_object.id}: {harvest_object}")
            return False

        package_dict = json.loads(harvest_object.content)

        self._transmute_content(package_dict)

        if package_dict.get("type") == "harvest":
            log.info("Remote dataset is a harvest source, ignoring...")
            return True

        default_extras = config.get("default_extras", {})

        def get_extra(key, package_dict):
            for extra in package_dict.get("extras", []):
                if extra["key"] == key:
                    return extra

        if default_extras:
            # you can disable extras override by defining override_extras to True in config
            override_extras = config.get("override_extras", False)
            if "extras" not in package_dict:
                package_dict["extras"] = []

            for k, v in default_extras.items():
                existing_extra = get_extra(k, package_dict)
                if existing_extra and not override_extras:
                    continue
                if existing_extra:
                    package_dict["extras"].remove(existing_extra)

                if isinstance(v, str):
                    v = v.format(
                        harvest_source_id=harvest_object.job.source.id,
                        harvest_source_url=harvest_object.job.source.url.strip("/"),
                        harvest_source_title=harvest_object.job.source.title,
                        harvest_job_id=harvest_object.job.id,
                        harvest_object_id=harvest_object.id,
                        dataset_id=package_dict["id"],
                    )

                package_dict["extras"].append({"key": k, "value": v})

        # Local harvest source organization
        source_dataset = tk.get_action("package_show")(
            self.base_context, {"id": harvest_object.source.id}
        )
        local_org = source_dataset.get("owner_org")

        package_dict["owner_org"] = local_org

        try:
            result = self._create_or_update_package(
                package_dict, harvest_object, package_dict_form="package_show"
            )

            if result != "unchanged" and plugin_loaded("xloader"):
                package_id = package_dict.get("id")
                self.create_or_update_resources(package_id)

            return result
        except tk.ValidationError as e:
            log.error(
                "Invalid package with GUID {}: {}".format(
                    (harvest_object.guid, e.error_dict), harvest_object
                )
            )
        except Exception as e:
            self._save_object_error(str(e), harvest_object, "Import")

    def transmute_data(self, data, schema):
        if schema:
            tk.get_action("tsm_transmute")(
                self.base_context, {"data": data, "schema": schema}
            )

    def _get_src_url(self, harvest_obj) -> str:
        return harvest_obj.source.url.strip("/")

    def _generate_unique_id(self, origin_id: str, source_id: str) -> str:
        """Generates a stable unique ID based on origin remote pkg ID
        and source name

        Args:
            origin_id (str): origin remote package ID

        Returns:
            str: unique ID
        """
        namespace = uuid.uuid5(uuid.NAMESPACE_DNS, source_id)
        return str(uuid.uuid5(namespace, origin_id))

    def create_or_update_resources(self, package_id):
        """
            Submit Resources to Xloader
        """
        try:
            package_dict = tk.get_action("package_show")(
                self.base_context,
                {"id": package_id}
            )
        except tk.ObjectNotFound:
            return

        resources = package_dict.get("resources", [])

        for resource in resources:
            resource_id = resource.get("id")

            if resource_id and XLoaderFormats.is_it_an_xloader_format(resource.get("format")):
                tk.get_action('xloader_submit')(
                    {"ignore_auth": True},
                    {'resource_id': resource_id}
                )
