# coding: utf-8

"""
    

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import json
import pprint
import re  # noqa: F401

from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, field_validator, StrictStr
from typing_extensions import Self

from gretel_client.rest_v1.models.project import Project
from gretel_client.rest_v1.models.user_profile import UserProfile
from gretel_client.rest_v1.models.workflow_run import WorkflowRun


class Workflow(BaseModel):
    """
    Workflow
    """  # noqa: E501

    id: StrictStr = Field(description="The unique ID of the workflow.")
    name: StrictStr = Field(description="The name of the workflow.")
    project_id: StrictStr = Field(
        description="The project ID that this workflow belongs to."
    )
    project: Optional[Project] = Field(
        default=None,
        description="The project that this workflow belongs to. Provided when the `expand=project` query param is present.",
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None, description="The config of the workflow."
    )
    config_text: Optional[StrictStr] = Field(
        default=None, description="The config of the workflow as a YAML string."
    )
    runner_mode: Optional[StrictStr] = Field(
        default=None,
        description="The runner mode of the workflow. Can be `cloud` or `hybrid`.",
    )
    created_by: StrictStr = Field(description="The user ID that created this workflow.")
    created_by_profile: Optional[UserProfile] = Field(
        default=None,
        description="The user profile of the user that created this workflow. Provided when the `expand=created_by` query param is present.",
    )
    updated_by: Optional[StrictStr] = Field(
        default=None, description="The user ID that last updated this workflow."
    )
    updated_by_profile: Optional[UserProfile] = Field(
        default=None,
        description="The user profile of the user that last updated this workflow. Provided when the `expand=updated_by` query param is present.",
    )
    created_at: datetime = Field(
        description="A timestamp indicating when this workflow was created."
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="A timestamp indicating when this workflow was last updated.",
    )
    next_scheduled_run: Optional[datetime] = Field(
        default=None,
        description="A timestamp indicating when the next scheduled run is.",
    )
    latest_run: Optional[WorkflowRun] = Field(
        default=None,
        description="The latest run of this workflow. Provided when the `expand=latest_run` query param is present.",
    )
    __properties: ClassVar[List[str]] = [
        "id",
        "name",
        "project_id",
        "project",
        "config",
        "config_text",
        "runner_mode",
        "created_by",
        "created_by_profile",
        "updated_by",
        "updated_by_profile",
        "created_at",
        "updated_at",
        "next_scheduled_run",
        "latest_run",
    ]

    @field_validator("runner_mode")
    def runner_mode_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(
            [
                "RUNNER_MODE_UNSET",
                "RUNNER_MODE_CLOUD",
                "RUNNER_MODE_HYBRID",
                "RUNNER_MODE_INVALID",
            ]
        ):
            raise ValueError(
                "must be one of enum values ('RUNNER_MODE_UNSET', 'RUNNER_MODE_CLOUD', 'RUNNER_MODE_HYBRID', 'RUNNER_MODE_INVALID')"
            )
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Workflow from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of project
        if self.project:
            _dict["project"] = self.project.to_dict()
        # override the default output from pydantic by calling `to_dict()` of created_by_profile
        if self.created_by_profile:
            _dict["created_by_profile"] = self.created_by_profile.to_dict()
        # override the default output from pydantic by calling `to_dict()` of updated_by_profile
        if self.updated_by_profile:
            _dict["updated_by_profile"] = self.updated_by_profile.to_dict()
        # override the default output from pydantic by calling `to_dict()` of latest_run
        if self.latest_run:
            _dict["latest_run"] = self.latest_run.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Workflow from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "project_id": obj.get("project_id"),
                "project": (
                    Project.from_dict(obj["project"])
                    if obj.get("project") is not None
                    else None
                ),
                "config": obj.get("config"),
                "config_text": obj.get("config_text"),
                "runner_mode": obj.get("runner_mode"),
                "created_by": obj.get("created_by"),
                "created_by_profile": (
                    UserProfile.from_dict(obj["created_by_profile"])
                    if obj.get("created_by_profile") is not None
                    else None
                ),
                "updated_by": obj.get("updated_by"),
                "updated_by_profile": (
                    UserProfile.from_dict(obj["updated_by_profile"])
                    if obj.get("updated_by_profile") is not None
                    else None
                ),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "next_scheduled_run": obj.get("next_scheduled_run"),
                "latest_run": (
                    WorkflowRun.from_dict(obj["latest_run"])
                    if obj.get("latest_run") is not None
                    else None
                ),
            }
        )
        return _obj
