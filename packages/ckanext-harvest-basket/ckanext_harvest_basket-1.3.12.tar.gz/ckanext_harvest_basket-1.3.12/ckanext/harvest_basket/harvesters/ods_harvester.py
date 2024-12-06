from __future__ import annotations

import json
import logging
import mimetypes
from typing import Any
from urllib.parse import urlencode, urljoin

from ckanext.harvest.harvesters.ckanharvester import SearchError
from ckanext.harvest.model import HarvestObject
from ckanext.harvest_basket.harvesters.base_harvester import \
    BasketBasicHarvester

import ckan.plugins.toolkit as tk
from ckan.lib.navl.validators import unicode_safe

log = logging.getLogger(__name__)


class ODSHarvester(BasketBasicHarvester):
    SRC_ID = "ODS"

    def info(self):
        return {
            "name": "ods",
            "title": "OpenDataSoft",
            "description": "Harvests datasets from remote Opendatasoft portals",
        }

    def gather_stage(self, harvest_job):
        source_url = harvest_job.source.url.strip("/")
        self._set_config(harvest_job.source.config)
        log.info(f"{self.SRC_ID}: gather stage started: {source_url}")

        try:
            pkg_dicts = self._search_datasets(source_url)
        except SearchError as e:
            log.error(f"{self.SRC_ID}: search for datasets failed: {e}")
            self._save_gather_error(
                f"{self.SRC_ID}: unable to search the remote portal for datasets: {source_url}",
                harvest_job,
            )
            return []

        if not pkg_dicts:
            log.error(f"{self.SRC_ID}: search returns empty result.")
            self._save_gather_error(
                f"{self.SRC_ID}: no datasets found at ODS remote portal: {source_url}",
                harvest_job,
            )
            return []

        try:
            package_ids = set()
            object_ids = []

            for pkg_dict in pkg_dicts:
                pkg_id = unicode_safe(pkg_dict["dataset"]["dataset_id"])
                if pkg_id in package_ids:
                    log.debug(
                        f"{self.SRC_ID}: Discarding duplicate dataset {pkg_id}. ",
                        "Probably, due to datasets being changed in process of harvesting",
                    )
                    continue

                package_ids.add(pkg_id)
                pkg_name: str = pkg_dict["dataset"]["metas"]["default"]["title"]
                log.info(
                    f"{self.SRC_ID}: Creating HARVEST object for {pkg_name} | id: {pkg_id}"
                )

                obj = HarvestObject(
                    guid=pkg_id, job=harvest_job, content=json.dumps(pkg_dict)
                )
                obj.save()
                object_ids.append(obj.id)

            return object_ids
        except Exception as e:
            log.debug("The error occured during the gather stage: {}".format(e))
            self._save_gather_error(str(e), harvest_job)
            return []

    def _search_datasets(self, source_url):
        """
        gathering ODS datasets
        returns a list with dicts of datasets metadata
        """

        pkg_dicts = []

        max_datasets = tk.asint(self.config.get("max_datasets", 0))

        params = {"rows": 50, "include_app_metas": True}

        where = self.config.get("where")

        if where:
            params["where"] = where

        if 1 <= max_datasets <= 100:
            params["rows"] = max_datasets

        search_url = urljoin(source_url, "/api/v2/catalog/datasets")
        url = search_url + "?" + urlencode(params)

        while True:
            log.info(f"{self.SRC_ID}: gathering ODS remote dataset: {url}")

            resp = self._make_request(url)
            if not resp:
                continue

            try:
                pkgs_data = json.loads(resp.text)
            except ValueError as e:
                log.debug(
                    f"{self.SRC_ID}: can't fetch the metadata. \
					Access denied or JSON object is corrupted"
                )
                return []

            for pkg in pkgs_data["datasets"]:
                pkg_dicts.append(pkg)

            url = self._get_next_page_datasets_url(pkgs_data)
            if not url:
                break

            if max_datasets and len(pkg_dicts) > max_datasets:
                break

        return pkg_dicts[:max_datasets] if max_datasets else pkg_dicts

    def _get_next_page_datasets_url(self, pkg_dict):
        for link in pkg_dict["links"]:
            if link["rel"] == "next":
                return link["href"]

    def _fetch_resources(self, source_url, resource_urls, pkg_data):
        resources = []

        for res in resource_urls:
            resource = {}

            resource["package_id"] = pkg_data["id"]
            resource["url"] = res["href"]
            resource["format"] = res["rel"].upper()
            resource[
                "name"
            ] = f"{pkg_data.get('title', tk._('Unnamed resource'))} ({res['rel']})"

            # Try to create unique ID that won't be changed over time
            resource['id'] = self._generate_unique_id(pkg_data['id'] + resource["format"], resource["url"])

            resources.append(resource)

        # attachments are an additional resources that we can fetch
        attachments = pkg_data.get("attachments")
        if attachments:
            offset = "/api/datasets/1.0/{}/attachments/{}/"
            for att in attachments:
                resource = {}
                url = urljoin(
                    source_url, offset.format(pkg_data["origin_id"], att["id"])
                )

                resource["package_id"] = pkg_data["id"]
                resource["url"] = url
                resource["format"] = self._guess_attachment_format(att)
                resource["name"] = att.get("title", "")

                # Try to create unique ID that won't be changed over time
                resource['id'] = self._generate_unique_id(pkg_data['id'] + resource["format"], resource["url"])

                resources.append(resource)
        return resources

    def _guess_attachment_format(self, attachment: dict[str, str]) -> str:
        """The attachment doesn't have a format field, only mimetype. So we
        could try to guess a format by mimetype. If it's not here, use a url
        and try to parse format from it (it could end with something like
        `attachment_name.pdf`"""
        mimetype: str | None = attachment.get("mimetype")
        if mimetype:
            formats = tk.h.resource_formats()
            if mimetype in formats:
                return formats[mimetype][1].lower()

            dot_format: str | None = mimetypes.guess_extension(mimetype)
            if dot_format:
                return dot_format.strip(".")

        return (attachment["url"].split(".")[-1]).upper()

    def fetch_stage(self, harvest_object):
        self._set_config(harvest_object.source.config)
        source_url = self._get_src_url(harvest_object)
        package_dict = json.loads(harvest_object.content)
        self._pre_map_stage(package_dict, source_url)
        harvest_object.content = json.dumps(package_dict)
        return True

    def _pre_map_stage(self, package_dict: dict, source_url: str):
        self._flatten_ods_dataset_dict(package_dict)
        package_dict["origin_id"] = origin_id = package_dict["dataset_id"]
        package_dict["id"] = self._generate_unique_id(origin_id, source_url)
        package_dict["url"] = self._get_dataset_links_data(package_dict)
        package_dict["notes"] = self._description_refine(
            package_dict.get("description")
        )

        res_export_url: str = self._get_export_resource_url(source_url, origin_id)
        res_links = self._get_all_resource_urls(res_export_url)
        package_dict["resources"] = self._fetch_resources(
            source_url, res_links, package_dict
        )

        package_dict["tags"] = self._fetch_tags(package_dict.get("keyword", []))
        package_dict["type"] = "dataset"

        extra = (
            ("language", "Language"),
            ("license", "License"),
            ("license_url", "License url"),
            ("timezone", "Timezone"),
            ("parent_domain", "Parent Domain"),
            ("references", "References"),
        )

        package_dict["extras"] = []

        for field in extra:
            if package_dict.get(field[0]):
                package_dict["extras"].append(
                    {"key": field[1], "value": package_dict[field[0]]}
                )

    def _flatten_ods_dataset_dict(self, pkg_dict):
        pkg_dict.update(pkg_dict.pop("dataset", {}))

        if meta_dict := pkg_dict.get("metas"):
            meta_keys: list[str] = list(meta_dict.keys())

            for category in meta_keys:
                for field in meta_dict[category]:
                    new_key: str = field if category == "default" else f"{category}_{field}"
                    pkg_dict[new_key] = meta_dict[category][field]

            pkg_dict.pop("metas")

        pkg_dict.pop("fields", {})

    def _get_dataset_links_data(self, pkg_links):
        for link in pkg_links["links"]:
            if link["rel"] == "self":
                return link["href"]

    def _get_export_resource_url(self, source_url, pkg_id):
        offset = "/api/v2/catalog/datasets/{}/exports".format(pkg_id)
        return source_url + offset

    def _get_all_resource_urls(self, res_link: str) -> list[str]:
        """Fetches a resource URLs

        Args:
                res_link (str): resource API endpoint

        Returns:
                list[str]: list of url strings
        """
        if not res_link:
            return []

        resp = self._make_request(res_link)
        if not resp:
            return []

        try:
            content = json.loads(resp.text)
        except ValueError as e:
            log.debug(
                f"{self.SRC_ID}: Can't fetch the metadata. \
				Access denied or JSON object is corrupted"
            )
            return []

        res_links = []
        formats = ("csv", "json", "xls", "geojson", "shp", "kml")
        for link in content["links"]:
            if link["rel"].lower() not in formats or not link["href"]:
                continue
            res_links.append(link)

        return res_links
