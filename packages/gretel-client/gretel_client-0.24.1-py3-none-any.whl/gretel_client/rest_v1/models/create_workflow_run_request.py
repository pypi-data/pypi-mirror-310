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

from typing import Any, ClassVar, Dict, List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field, field_validator, StrictStr
from typing_extensions import Annotated, Self


class CreateWorkflowRunRequest(BaseModel):
    """
    CreateWorkflowRunRequest
    """  # noqa: E501

    workflow_id: Annotated[str, Field(strict=True)] = Field(
        description="The ID of the workflow to create a run for."
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="An optional config for the workflow run If provided, this will be used in place of the workflow's config.",
    )
    config_text: Optional[StrictStr] = Field(
        default=None,
        description="An optional config for the workflow run as a YAML string. If provided, this will be used in place of the workflow's config.",
    )
    __properties: ClassVar[List[str]] = ["workflow_id", "config", "config_text"]

    @field_validator("workflow_id")
    def workflow_id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^w_.*$", value):
            raise ValueError(r"must validate the regular expression /^w_.*$/")
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
        """Create an instance of CreateWorkflowRunRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateWorkflowRunRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "workflow_id": obj.get("workflow_id"),
                "config": obj.get("config"),
                "config_text": obj.get("config_text"),
            }
        )
        return _obj
