#
# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import argparse
from builtins import int
from collections.abc import Iterable
import datetime
from itertools import chain
import logging
import os
from typing import List, Optional, Union

from ngcbpc.api.authentication import Authentication
from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.api.pagination import pagination_helper_use_page_reference
from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV, TRANSFER_STATES
from ngcbpc.errors import (
    NgcException,
    ResourceAlreadyExistsException,
    ResourceFilesNotFoundException,
    ResourceNotFoundException,
)
from ngcbpc.printer.transfer import TransferPrinter
from ngcbpc.transfer import async_download, http_uploader
from ngcbpc.transfer.utils import get_download_files
from ngcbpc.util.file_utils import (
    get_file_contents,
    get_transfer_path,
    tree_size_and_count,
)
from ngcbpc.util.utils import (
    confirm_remove,
    extra_args,
    find_case_insensitive,
    format_org_team,
)
from ngccli.data.model.ApplicationType import ApplicationTypeEnum
from ngccli.data.model.FrameworkType import FrameworkTypeEnum
from ngccli.data.model.PrecisionType import PrecisionTypeEnum
from ngccli.data.model.RecipeCreateRequest import RecipeCreateRequest
from ngccli.data.model.RecipeListResponse import RecipeListResponse
from ngccli.data.model.RecipeResponse import RecipeResponse
from ngccli.data.model.RecipeUpdateRequest import RecipeUpdateRequest
from ngccli.data.model.RecipeVersion import RecipeVersion
from ngccli.data.model.RecipeVersionCreateRequest import RecipeVersionCreateRequest
from ngccli.data.model.RecipeVersionFileListResponse import (
    RecipeVersionFileListResponse,
)
from ngccli.data.model.RecipeVersionListResponse import RecipeVersionListResponse
from ngccli.data.model.RecipeVersionResponse import RecipeVersionResponse
from ngccli.data.model.RecipeVersionUpdateRequest import RecipeVersionUpdateRequest
from registry.api.utils import (
    filter_version_list,
    get_environ_tag,
    get_label_set_labels,
    handle_public_dataset_no_args,
    ModelRegistryTarget,
)
from registry.constants import MODEL_SERVICE_URL_MAPPING
from registry.transformer.model_script import ModelScriptSearchTransformer

logger = logging.getLogger(__name__)

PAGE_SIZE = 1000


NOTES_ARG = "--release-notes-filename"
PERFORMANCE_ARG = "--performance-filename"
ADVANCED_ARG = "--advanced-filename"
QUICK_START_ARG = "--quick-start-guide-filename"
SETUP_ARG = "--setup-filename"
OVERVIEW_ARG = "--overview-filename"

environ_tag = get_environ_tag()
env = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}.get(environ_tag)
ENDPOINT_VERSION = "v1" if Configuration().base_url == MODEL_SERVICE_URL_MAPPING[env] else "v2"


class ResourceAPI:
    def __init__(self, connection: Connection, api_client=None):
        self.config = Configuration()
        self.connection = connection
        self.api_client = api_client
        self.transfer_printer = TransferPrinter()
        self.resource_type = "RECIPE"

    # PUBLIC FUNCTIONS
    @extra_args
    def download_version(
        self,
        target: str,
        destination: Optional[str] = ".",
        file_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ):
        """Download the specified model version"""
        self.config.validate_configuration(guest_mode_allowed=True)
        # non-list, use org/team from target
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True, version_required=False)

        if not mrt.version:
            mrt.version = self._get_latest_version(mrt)
            self.transfer_printer.print_ok(f"No version specified, downloading latest version: '{mrt.version}'.")

        download_dir = os.path.abspath(destination)
        if not os.path.isdir(download_dir):
            raise NgcException(f"The path: '{destination}' does not exist.")
        try:
            resp = self.get_version(mrt.org, mrt.team, mrt.name, mrt.version)
            status = resp.recipeVersion.status
            if status != "UPLOAD_COMPLETE":
                raise NgcException(f"'{target}' is not in state UPLOAD_COMPLETE.")
        except ResourceNotFoundException:
            raise ResourceNotFoundException(f"'{target}' could not be found.") from None

        self._download(mrt, download_dir, file_patterns=file_patterns, exclude_patterns=exclude_patterns)

    @extra_args
    def upload_version(
        self,
        target: str,
        source: Optional[str] = ".",
        gpu_model: Optional[str] = None,
        memory_footprint: Optional[str] = None,
        num_epochs: Optional[int] = None,
        release_notes_filename: Optional[str] = None,
        quick_start_guide_filename: Optional[str] = None,
        performance_filename: Optional[str] = None,
        setup_filename: Optional[str] = None,
        batch_size: Optional[int] = None,
        accuracy_reached: Optional[float] = None,
        description: Optional[str] = None,
        dry_run: Optional[bool] = False,
    ):
        """Upload a model version."""
        self.config.validate_configuration()
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True, version_required=True)

        transfer_path = get_transfer_path(source)
        if dry_run:
            self.transfer_printer.print_ok("Files to be uploaded:")
        transfer_size, file_count = tree_size_and_count(
            transfer_path,
            omit_links=False,
            print_paths=dry_run,
            dryrun_option=dry_run,
            check_max_size=True,
        )
        if dry_run:
            self.transfer_printer.print_upload_dry_run(transfer_size, file_count)
            return

        vcr = RecipeVersionCreateRequest(
            {
                "versionId": mrt.version,
                "accuracyReached": accuracy_reached,
                "batchSize": batch_size,
                "gpuModel": gpu_model,
                "memoryFootprint": memory_footprint,
                "numberOfEpochs": num_epochs,
                "releaseNotes": get_file_contents(release_notes_filename, NOTES_ARG),
                # commmon recipe/version
                "description": description,
                "performance": get_file_contents(performance_filename, PERFORMANCE_ARG),
                "quickStartGuide": get_file_contents(quick_start_guide_filename, QUICK_START_ARG),
                "setup": get_file_contents(setup_filename, SETUP_ARG),
            }
        )
        vcr.isValid()
        try:
            self._create_version(
                org_name=mrt.org, team_name=mrt.team, resource_name=mrt.name, version_create_request=vcr
            )
        except ResourceAlreadyExistsException:
            version_resp = self.get_version(
                org_name=mrt.org, team_name=mrt.team, resource_name=mrt.name, version=mrt.version
            )
            version_status = version_resp.recipeVersion.status
            if version_status != "UPLOAD_PENDING":
                raise ResourceAlreadyExistsException("Target '{}' already exists.".format(mrt)) from None
        except ResourceNotFoundException:
            target_base = "/".join([x for x in [mrt.org, mrt.team, mrt.name] if x is not None])
            raise ResourceNotFoundException("Target '{}' not found.".format(target_base)) from None

        completed_upload = self._perform_upload(mrt, transfer_path)
        if completed_upload:
            self._update_upload_complete(mrt.org, mrt.team, mrt.name, mrt.version)
        else:
            raise NgcException("WARNING: Upload failed, or was unable to complete.") from None

    @extra_args
    def update(
        self,
        target: str,
        application: Optional[str] = None,
        framework: Optional[str] = None,
        model_format: Optional[str] = None,
        precision: Optional[str] = None,
        short_description: Optional[str] = None,
        overview_filename: Optional[str] = None,
        advanced_filename: Optional[str] = None,
        performance_filename: Optional[str] = None,
        quick_start_guide_filename: Optional[str] = None,
        release_notes_filename: Optional[str] = None,
        setup_filename: Optional[str] = None,
        display_name: Optional[str] = None,
        label: List[Optional[str]] = None,
        label_set: List[Optional[str]] = None,
        logo: Optional[str] = None,
        public_dataset_name: Optional[str] = None,
        desc: Optional[str] = None,
        public_dataset_license: Optional[str] = None,
        public_dataset_link: Optional[str] = None,
        built_by: Optional[str] = None,
        publisher: Optional[str] = None,
        batch_size: Optional[int] = None,
        num_epochs: Optional[int] = None,
        accuracy_reached: Optional[float] = None,
        gpu_model: Optional[str] = None,
        memory_footprint: Optional[str] = None,
    ):
        """Update a resource or resource version"""
        self.config.validate_configuration()
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True)

        # Translate the values for application and precision back to their canonical capitalization
        if application:
            application = find_case_insensitive(application, ApplicationTypeEnum, "application")
        if framework:
            framework = find_case_insensitive(framework, FrameworkTypeEnum, "framework")
        if precision:
            precision = find_case_insensitive(precision, PrecisionTypeEnum, "precision")

        if mrt.version is None:
            # validate args
            self._validate_update_resource(locals())
            update_request = RecipeUpdateRequest(
                {
                    "application": application,
                    "trainingFramework": framework,
                    "builtBy": built_by,
                    # Note: script level overview attribute is stored in description in the schema.
                    # UI diverged and we need to quickly match them now.
                    "description": get_file_contents(overview_filename, OVERVIEW_ARG),
                    "displayName": display_name,
                    "labelsV2": get_label_set_labels(
                        self.api_client.registry.label_set, self.resource_type, label_set, label
                    ),
                    "logo": logo,
                    "modelFormat": model_format,
                    "advanced": get_file_contents(advanced_filename, ADVANCED_ARG),
                    "performance": get_file_contents(performance_filename, PERFORMANCE_ARG),
                    "precision": precision,
                    "publicDatasetUsed": handle_public_dataset_no_args(
                        public_dataset_name=public_dataset_name,
                        public_dataset_link=public_dataset_link,
                        public_dataset_license=public_dataset_license,
                    ),
                    "publisher": publisher,
                    "quickStartGuide": get_file_contents(quick_start_guide_filename, QUICK_START_ARG),
                    "setup": get_file_contents(setup_filename, SETUP_ARG),
                    "shortDescription": short_description,
                }
            )
            update_request.isValid()
            try:
                return self._update_resource(
                    org_name=mrt.org, team_name=mrt.team, resource_name=mrt.name, resource_update_request=update_request
                )
            except ResourceNotFoundException:
                raise ResourceNotFoundException(f"Resource '{target}' was not found.") from None
        else:
            self._validate_update_version(locals())
            version_update_request = RecipeVersionUpdateRequest(
                {
                    "accuracyReached": accuracy_reached,
                    "batchSize": batch_size,
                    "gpuModel": gpu_model,
                    "memoryFootprint": memory_footprint,
                    "numberOfEpochs": num_epochs,
                    "releaseNotes": get_file_contents(release_notes_filename, NOTES_ARG),
                    "description": desc,
                    # commmon recipe/version
                    # TODO following are not currently getting updated on webservice.
                    "performance": get_file_contents(performance_filename, PERFORMANCE_ARG),
                    "quickStartGuide": get_file_contents(quick_start_guide_filename, QUICK_START_ARG),
                    "setup": get_file_contents(setup_filename, SETUP_ARG),
                }
            )
            try:
                return self._update_version(
                    org_name=mrt.org,
                    team_name=mrt.team,
                    resource_name=mrt.name,
                    version=mrt.version,
                    version_update_request=version_update_request,
                )
            except ResourceNotFoundException:
                raise ResourceNotFoundException("Resource version '{}' was not found.".format(target)) from None

    @extra_args
    def create(
        self,
        target: str,
        application: str,
        framework: str,
        model_format: str,
        precision: str,
        short_description: str,
        overview_filename: Optional[str] = None,
        advanced_filename: Optional[str] = None,
        performance_filename: Optional[str] = None,
        quick_start_guide_filename: Optional[str] = None,
        setup_filename: Optional[str] = None,
        display_name: Optional[str] = None,
        label: List[Optional[str]] = None,
        label_set: List[Optional[str]] = None,
        logo: Optional[str] = None,
        public_dataset_name: Optional[str] = None,
        public_dataset_license: Optional[str] = None,
        public_dataset_link: Optional[str] = None,
        built_by: Optional[str] = None,
        publisher: Optional[str] = None,
    ) -> RecipeResponse:
        """Create a resource"""
        self.config.validate_configuration()
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True, version_allowed=False)

        script_create_request = RecipeCreateRequest(
            {
                # required
                "name": mrt.name,
                "application": find_case_insensitive(application, ApplicationTypeEnum, "application"),
                "trainingFramework": find_case_insensitive(framework, FrameworkTypeEnum, "framework"),
                "modelFormat": model_format,
                "precision": find_case_insensitive(precision, PrecisionTypeEnum, "precision"),
                "shortDescription": short_description,
                # optional
                # Note: script level overview attribute is stored in description in the schema.
                # UI diverged and we need to quickly match them now.
                "description": get_file_contents(overview_filename, OVERVIEW_ARG),
                "displayName": display_name,
                "labelsV2": get_label_set_labels(
                    self.api_client.registry.label_set, self.resource_type, label_set, label
                ),
                "logo": logo,
                "publicDatasetUsed": handle_public_dataset_no_args(
                    public_dataset_name=public_dataset_name,
                    public_dataset_link=public_dataset_link,
                    public_dataset_license=public_dataset_license,
                ),
                "builtBy": built_by,
                "publisher": publisher,
                # docs
                "advanced": get_file_contents(advanced_filename, ADVANCED_ARG),
                "performance": get_file_contents(performance_filename, PERFORMANCE_ARG),
                "quickStartGuide": get_file_contents(quick_start_guide_filename, QUICK_START_ARG),
                "setup": get_file_contents(setup_filename, SETUP_ARG),
            }
        )
        script_create_request.isValid()
        try:
            created_resource = self._create(mrt.org, mrt.team, script_create_request)
        except ResourceAlreadyExistsException:
            raise ResourceAlreadyExistsException(f"Resource '{target}' already exists.") from None
        return created_resource

    @extra_args
    def info(
        self,
        target: str,
        list_files: Optional[bool] = None,
    ) -> Union[RecipeResponse, RecipeVersionResponse]:
        """Get info about a given resource or resource version"""
        self.config.validate_configuration(guest_mode_allowed=True)
        # non-list, use org/team from target
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
        if mrt.version is None:
            if list_files:
                raise argparse.ArgumentTypeError(
                    "--files argument is not valid for a resource target, please specify a version."
                )
            resp: RecipeResponse = self.get(mrt.org, mrt.team, mrt.name)
            return resp
        try:
            resp: RecipeVersionResponse = self.get_version(mrt.org, mrt.team, mrt.name, str(mrt.version))
        except ResourceNotFoundException:
            raise ResourceNotFoundException(f"Target '{target}' could not be found.") from None

        return resp

    @extra_args
    def list(
        self,
        target: Optional[str] = None,
        access_type: Optional[str] = None,
        product_names: Optional[str] = None,
        org: Optional[str] = None,
        team: Optional[str] = None,
    ) -> Union[Iterable[ModelScriptSearchTransformer], Iterable[RecipeVersion]]:
        """List Resources given a pattern glob or list a resource's versions"""
        self.config.validate_configuration(guest_mode_allowed=True, csv_allowed=True)
        mrt = ModelRegistryTarget(target, glob_allowed=True)
        org = org or mrt.org or self.config.org_name
        team = team or mrt.team or self.config.team_name

        if mrt.version is None:
            if access_type or product_names:
                return self.api_client.registry.search.search_resource(
                    org, team, target, access_type=access_type, product_names=product_names
                )
            return self.api_client.registry.search.search_resource(org, team, target)
        try:
            version_list = self.list_versions(org, team, mrt.name)
        except ResourceNotFoundException:
            version_list = []
        version_list = filter_version_list(version_list, mrt.version)
        return version_list

    @extra_args
    def remove(self, target: str, default_yes: Optional[bool] = False) -> None:
        """Remove a given resource or resource version"""
        self.config.validate_configuration()
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
        confirm_remove(target=target, default=default_yes)

        if mrt.version:
            try:
                self._remove_version(org_name=mrt.org, team_name=mrt.team, resource_name=mrt.name, version=mrt.version)
            except ResourceNotFoundException:
                raise ResourceNotFoundException(f"Resource version '{target}' could not be found.") from None
        else:
            try:
                self._remove(org_name=mrt.org, team_name=mrt.team, resource_name=mrt.name)
            except ResourceNotFoundException:
                raise ResourceNotFoundException(f"Resource '{target}' could not be found.") from None

    # END PUBLIC Functions
    def _update_upload_complete(self, org_name, team_name, resource_name, version):
        version_req = RecipeVersionUpdateRequest({"status": "UPLOAD_COMPLETE"})
        version_req.isValid()
        self._update_version(org_name, team_name, resource_name, version, version_req)

    @staticmethod
    def _get_resources_endpoint(org=None, team=None, name=None):
        """Create a resources endpoint through CAS proxy.

        /v2[/org/<org>[/team/<team>[/<name>]]]/resources
        """
        parts = [ENDPOINT_VERSION, format_org_team(org, team), "resources", name]
        return "/".join([part for part in parts if part])

    def get_versions_endpoint(
        self,
        org: Optional[str] = None,
        team: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """Create a resource version endpoint."""

        ep = self._get_resources_endpoint(org=org, team=team, name=name)
        ep = "/".join([ep, "versions"])

        # version can be zero
        if version is not None:
            ep = "/".join([ep, str(version)])

        return ep

    def get_files_endpoint(
        self,
        org: Optional[str] = None,
        team: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """Create a files endpoint."""
        ep = self.get_versions_endpoint(org=org, team=team, name=name, version=version)
        return "/".join([ep, "files"])

    @staticmethod
    def get_multipart_files_endpoint(org: Optional[str] = None, team: Optional[str] = None):
        org_team = format_org_team(org, team)
        return f"{ENDPOINT_VERSION}/{org_team}/files/multipart"

    def get_direct_download_URL(
        self,
        name: str,
        version: str,
        org: Optional[str] = None,
        team: Optional[str] = None,
        filepath: Optional[str] = None,
    ):
        ep = f"{ENDPOINT_VERSION}/{format_org_team(org, team)}/resources/{name}/{version}/files"
        if filepath:
            ep = f"{ep}?path={filepath}"
        return self.connection.create_full_URL(ep)

    def get_download_files_URL(self, name: str, version: str, org: Optional[str] = None, team: Optional[str] = None):
        """Since the file download goes through the AsyncDownload class and not the API Connection class, we need to
        return the full URL, not just the endpoint part.
        """
        org_team = format_org_team(org, team)
        ep = "/".join(
            [elem for elem in (ENDPOINT_VERSION, org_team, "resources", name, "versions", version, "files") if elem]
        )
        return self.connection.create_full_URL(ep)

    def _list(self, org_name: str, team_name: str, page_size: Optional[int] = PAGE_SIZE):
        """Get a list of resources."""

        base_url = self._get_resources_endpoint(org=org_name, team=team_name)
        query = "{url}?page-size={page_size}".format(url=base_url, page_size=page_size)
        return chain(
            *[
                RecipeListResponse(res).recipes
                for res in pagination_helper_use_page_reference(
                    self.connection, query, org_name=org_name, team_name=team_name, operation_name="list resources"
                )
                if RecipeListResponse(res).recipes
            ]
        )

    def get(self, org_name: str, team_name: str, resource_name: str):
        """Get a resource."""
        params = {"resolve-labels": "true"}
        resp = self.connection.make_api_request(
            "GET",
            self._get_resources_endpoint(org=org_name, team=team_name, name=resource_name),
            auth_org=org_name,
            auth_team=team_name,
            params=params,
            operation_name="get resource",
        )
        return RecipeResponse(resp)

    def _create(self, org_name: str, team_name: str, resource_create_request: RecipeCreateRequest):
        """Create a resource."""

        resp = self.connection.make_api_request(
            "POST",
            self._get_resources_endpoint(org=org_name, team=team_name),
            payload=resource_create_request.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="create resource",
        )

        return RecipeResponse(resp).recipe

    def _update_resource(
        self, org_name: str, team_name: str, resource_name: str, resource_update_request: RecipeUpdateRequest
    ):
        """Update a resource."""
        resp = self.connection.make_api_request(
            "PATCH",
            self._get_resources_endpoint(org=org_name, team=team_name, name=resource_name),
            payload=resource_update_request.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="update resource",
        )

        return RecipeResponse(resp).recipe

    def _remove(self, org_name: str, team_name: str, resource_name: str):
        """Remove a resource."""

        self.connection.make_api_request(
            "DELETE",
            self._get_resources_endpoint(org=org_name, team=team_name, name=resource_name),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="remove resource",
        )

    def list_versions(self, org_name: str, team_name: str, resource_name: str, page_size: Optional[int] = PAGE_SIZE):
        """Get a list of versions for a resource."""

        base_url = self.get_versions_endpoint(org=org_name, team=team_name, name=resource_name)
        query = "{url}?page-size={page_size}".format(url=base_url, page_size=page_size)
        return chain(
            *[
                RecipeVersionListResponse(res).recipeVersions
                for res in pagination_helper_use_page_reference(
                    self.connection,
                    query,
                    org_name=org_name,
                    team_name=team_name,
                    operation_name="list resource versions",
                )
                if RecipeVersionListResponse(res).recipeVersions
            ]
        )

    def get_version(self, org_name: str, team_name: str, resource_name: str, version: str):
        """Get a resource version."""
        ep = self.get_versions_endpoint(org=org_name, team=team_name, name=resource_name, version=version)
        resp = self.connection.make_api_request(
            "GET",
            ep,
            auth_org=org_name,
            auth_team=team_name,
            operation_name="get resource version",
        )
        return RecipeVersionResponse(resp)

    def _create_version(
        self, org_name: str, team_name: str, resource_name: str, version_create_request: RecipeVersionCreateRequest
    ):
        """Create a resource version."""

        resp = self.connection.make_api_request(
            "POST",
            self.get_versions_endpoint(org=org_name, team=team_name, name=resource_name),
            payload=version_create_request.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="create resource version",
        )
        return RecipeVersionResponse(resp)

    def _update_version(
        self,
        org_name: str,
        team_name: str,
        resource_name: str,
        version: str,
        version_update_request: RecipeVersionUpdateRequest,
    ):
        """Update a resource version."""

        resp = self.connection.make_api_request(
            "PATCH",
            self.get_versions_endpoint(org=org_name, team=team_name, name=resource_name, version=version),
            payload=version_update_request.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="update resource version",
        )
        return RecipeVersionResponse(resp)

    def _remove_version(self, org_name: str, team_name: str, resource_name: str, version: str):
        """Remove a resource version."""

        self.connection.make_api_request(
            "DELETE",
            self.get_versions_endpoint(org=org_name, team=team_name, name=resource_name, version=version),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="remove resource version",
        )

    def list_files(
        self, org_name: str, team_name: str, resource_name: str, version: str, page_size: Optional[int] = PAGE_SIZE
    ):
        """Get a list of files for a resource."""

        base_url = self.get_files_endpoint(org=org_name, team=team_name, name=resource_name, version=version)
        query = "{url}?page-size={page_size}".format(url=base_url, page_size=page_size)

        return chain(
            *[
                RecipeVersionFileListResponse(res).recipeFiles
                for res in pagination_helper_use_page_reference(
                    self.connection, query, org_name=org_name, team_name=team_name, operation_name="list resource files"
                )
                if RecipeVersionFileListResponse(res).recipeFiles
            ]
        )

    def _validate_update_resource(self, args_dict):
        invalid_args = [arg[1] for arg in self.version_only_args if args_dict.get(arg[0]) is not None]
        if invalid_args:
            raise argparse.ArgumentTypeError(
                "Invalid argument(s) for resource, {} is only valid for a resource version.".format(invalid_args)
            )
        if all(args_dict.get(arg[0]) is None for arg in self.resource_only_args + self.resource_and_version_args):
            raise argparse.ArgumentTypeError("No arguments provided for resource update, there is nothing to do.")

    def _validate_update_version(self, args_dict):
        invalid_args = [arg[1] for arg in self.resource_only_args if args_dict.get(arg[0]) is not None]
        if invalid_args:
            raise argparse.ArgumentTypeError(
                "Invalid argument(s) for resource version, {} is only valid for a resource.".format(invalid_args)
            )
        if all(args_dict.get(arg[0]) is None for arg in self.version_only_args + self.resource_and_version_args):
            raise argparse.ArgumentTypeError(
                "No arguments provided for resource version update request, there is nothing to do."
            )

    resource_and_version_args = [
        ("performance_filename", "--performance-filename"),
        ("quick_start_guide_filename", "--quick-start-guide-filename"),
        ("setup_filename", "--setup-filename"),
    ]

    resource_only_args = [
        ("application", "--application"),
        ("framework", "--framework"),
        ("model_format", "--format"),
        ("precision", "--precision"),
        ("short_description", "--short-desc"),
        # optional
        ("display_name", "--display-name"),
        ("advanced_filename", "--advanced-filename"),
        ("label", "--label"),
        ("logo", "--logo"),
        ("overview_filename", "--overview-filename"),
        ("public_dataset_name", "--public-dataset-name"),
        ("public_dataset_link", "--public-dataset-link"),
        ("public_dataset_license", "--public-dataset-license"),
        ("built_by", "--built-by"),
        ("publisher", "--publisher"),
        ("label_set", "--label-set"),
    ]

    version_only_args = [
        ("gpu_model", "--gpu-model"),
        ("memory_footprint", "--memory-footprint"),
        ("num_epochs", "--num-epochs"),
        ("batch_size", "--batch-size"),
        ("accuracy_reached", "--accuracy-reached"),
        ("description", "--description"),
        ("set_latest", "--set-latest"),
        ("release_notes_filename", "--release-notes-filename"),
        ("setup", "--setup"),
        ("desc", "--desc"),
        ("performance_filename", "--performance-filename"),
        ("quick_start_guide_filename", "--quick-start-guide-filename"),
    ]

    def _perform_upload(self, mrt: ModelRegistryTarget, transfer_path: str):
        """Perform the recipe upload."""
        headers = Authentication.auth_header(auth_org=mrt.org, auth_team=mrt.team)
        ep = self.get_multipart_files_endpoint(org=mrt.org, team=mrt.team)
        full_url = self.connection.create_full_URL(ep)
        started_at = datetime.datetime.now()
        (
            elapsed,
            upload_count,
            upload_size,
            failed_count,
            upload_total_size,
            total_file_count,
            _,
        ) = http_uploader.upload_directory(
            transfer_path,
            full_url,
            mrt.name,
            mrt.version,
            mrt.org,
            mrt.team,
            "resource",
            headers=headers,
            count=None,
            operation_name="resource upload_version",
        )
        ended_at = datetime.datetime.now()
        xfer_id = f"{mrt.name}[version={mrt.version}]"
        if failed_count or upload_count == 0:
            status = TRANSFER_STATES["FAILED"]
        elif upload_size != upload_total_size or upload_count != total_file_count:
            status = TRANSFER_STATES["TERMINATED"]
        else:
            status = TRANSFER_STATES["COMPLETED"]
        self.transfer_printer.print_async_upload_transfer_summary(
            "resource", xfer_id, status, transfer_path, elapsed, upload_count, upload_size, started_at, ended_at
        )
        return status == TRANSFER_STATES["COMPLETED"]

    def _download(self, mrt, download_dir, file_patterns=None, exclude_patterns=None):
        self.transfer_printer.print_download_message("Getting files to download...\n")
        all_files = list(self.get_version_files(mrt.org, mrt.team, mrt.name, mrt.version))
        all_files_path_size = {f.path: f.sizeInBytes for f in all_files}
        dl_files, total_size = get_download_files(
            {f.path: f.sizeInBytes for f in all_files}, [], file_patterns, None, exclude_patterns
        )
        dl_files_with_size = {f: all_files_path_size.get(f, 0) for f in dl_files}
        paginated = not (file_patterns or exclude_patterns)
        if paginated:
            logger.debug("Downloading all files for resource '%s' version '%s'", mrt.name, mrt.version)
        else:
            logger.debug("Downloading %s files for resource '%s' version '%s'", len(dl_files), mrt.name, mrt.version)
        url = self.get_direct_download_URL(mrt.name, mrt.version, org=mrt.org, team=mrt.team)
        # Need to match the old output where the files are within a subfolder
        download_dir = f"{download_dir}/{mrt.name}_v{mrt.version}"
        started_at = datetime.datetime.now()
        (elapsed, download_count, download_size, failed_count, _, _,) = async_download.direct_download_files(
            "resource",
            mrt.name,
            mrt.org,
            mrt.team,
            mrt.version,
            url,
            paginated,
            dl_files_with_size,
            total_size,
            download_dir,
        )
        ended_at = datetime.datetime.now()
        status = "FAILED" if failed_count else "COMPLETED"
        return self.transfer_printer.print_async_download_transfer_summary(
            "resource", status, download_dir, elapsed, download_count, download_size, started_at, ended_at
        )

    def _get_latest_version(self, target):
        try:
            resp = self.get(target.org, target.team, target.name)
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
        if not resp.recipe.latestVersionIdStr:
            raise NgcException("Target '{}' has no version available for download.".format(target))
        return resp.recipe.latestVersionIdStr

    def get_version_files(self, org_name, team_name, name, version):
        try:
            file_list = self.list_files(org_name, team_name, name, version)
        except ResourceNotFoundException:
            raise ResourceFilesNotFoundException(f"Files could not be found for target '{name}:{version}'.") from None
        return file_list


class GuestResourceAPI(ResourceAPI):

    # FIXME: change to /resources/ endpoints once available
    def _get_resources_endpoint(self, org=None, team=None, name=None):
        """Create a guest resources endpoint.

        /v2/resources[/<org>[/<team>[/<name>]]]
        """

        ep = f"{ENDPOINT_VERSION}/resources"
        if org:
            ep = "/".join([ep, org])
        if team:
            ep = "/".join([ep, team])
        if name:
            ep = "/".join([ep, name])
        return ep

    def get_download_files_URL(self, name, version, org=None, team=None):
        """The download URL for guest access adds the org and team to the name, and omits them from the scope."""
        full_name = "/".join([elem for elem in (org, team, name) if elem])
        return super().get_download_files_URL(full_name, version, org=None, team=None)

    def get_direct_download_URL(self, name, version, org=None, team=None, filepath=None):
        org_team = format_org_team(org, team)
        ep = "/".join([item for item in (ENDPOINT_VERSION, "resources", org_team, name, version, "files") if item])
        if filepath:
            ep = f"{ep}?path={filepath}"
        return self.connection.create_full_URL(ep)
