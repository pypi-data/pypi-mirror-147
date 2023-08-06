# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2021 - 2022 TU Wien.
#
# Invenio-Requests is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Request Event Schemas."""

from datetime import timezone

from flask import g
from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import RAISE, Schema, fields, missing, validate
from marshmallow_oneofschema import OneOfSchema
from marshmallow_utils import fields as utils_fields

from invenio_requests.proxies import current_requests

from ..records.api import RequestEventFormat, RequestEventType


class RequestSchema(BaseRecordSchema):
    """Schema for requests.

    Note that the payload schema and the entity reference schemas (i.e. creator,
    receiver, and topic) are dynamically constructed and injected into this schema.
    """

    # load and dump
    type = fields.String()
    title = utils_fields.SanitizedUnicode(default="")
    description = utils_fields.SanitizedUnicode()

    # Dump-only
    number = fields.String(dump_only=True)
    status = fields.String(dump_only=True)
    is_closed = fields.Boolean(dump_only=True)
    is_open = fields.Boolean(dump_only=True)
    expires_at = utils_fields.TZDateTime(
        timezone=timezone.utc, format="iso", dump_only=True
    )
    is_expired = fields.Boolean(dump_only=True)

    class Meta:
        """Schema meta."""

        unknown = RAISE


class CommentExtra(Schema):
    """Comment extras schema."""

    content = utils_fields.SanitizedHTML(
        required=True, validate=validate.Length(min=1)
    )
    format = fields.Str(
        validate=validate.OneOf(choices=[e.value for e in RequestEventFormat]),
        load_default=RequestEventFormat.HTML.value,
    )


class GenericRequestSchema(RequestSchema):
    """Generic request schema.

    CAUTION: This schema should not be used for the final validation of input
    data. Use the request type's own defined schema instead.

    This schema can be used in situations where you need to do basic validation
    or dumping of a request without the payload.

    This is used e.g. in Invenio-RDM-Records for dumping a request without
    having to know the specific request type.
    """

    created_by = fields.Dict()
    receiver = fields.Dict()
    topic = fields.Dict()


class ModelFieldStr(fields.Str):
    """Marshmallow field for serializing by attribute before item."""

    def get_value(self, obj, attr, **kwargs):
        """Return obj.attr or obj[attr] in this precedence order."""
        return getattr(obj, attr, obj.get(attr, missing))


class BaseEventSchema(BaseRecordSchema):
    """Base Event schema that other schemas should inherit from."""

    type = ModelFieldStr(required=True)
    created_by = fields.Dict(dump_only=True)


class CommentSchema(BaseEventSchema):
    """Comment schema."""

    permissions = fields.Dict(dump_only=True)

    payload = fields.Nested(CommentExtra, required=True)


class NoExtrasSchema(BaseEventSchema):
    """No extras schema."""

    permissions = fields.Dict(dump_only=True)


class RequestEventSchema(BaseRecordSchema, OneOfSchema):
    """Schema."""

    # TODO: Make this schema hookable? how?

    type_schemas = {
        RequestEventType.COMMENT.value: CommentSchema,
        RequestEventType.ACCEPTED.value: NoExtrasSchema,
        RequestEventType.DECLINED.value: NoExtrasSchema,
        RequestEventType.CANCELLED.value: NoExtrasSchema,
        RequestEventType.REMOVED.value: NoExtrasSchema,
        RequestEventType.EXPIRED.value: NoExtrasSchema,
    }
    type_field_remove = False

    def get_obj_type(self, obj):
        """Return key of type_schemas to use given object to dump."""
        return obj.type


class CommentPermissionShema(Schema):
    """Add permissions to the dump data."""

    permissions = fields.Method("get_permissions")

    def get_permissions(self, obj):
        """Get certain permissions of the user with the current hit."""
        service = current_requests.request_events_service
        return {
            "can_update_comment": service.check_permission(
                self.context['identity'], "update_comment", event=obj
            ),
            "can_delete_comment": service.check_permission(
                self.context['identity'], "delete_comment", event=obj
            ),
        }


class CommentDumpSchema(BaseEventSchema, CommentPermissionShema):
    """Comment dump schema."""

    payload = fields.Nested(CommentExtra, required=True)


class NoExtrasDumpSchema(BaseEventSchema, CommentPermissionShema):
    """Comment dump schema."""


class RequestEventDumpSchema(BaseRecordSchema, OneOfSchema):
    """Dump schema."""

    type_schemas = {
        RequestEventType.COMMENT.value: CommentDumpSchema,
        RequestEventType.ACCEPTED.value: NoExtrasDumpSchema,
        RequestEventType.DECLINED.value: NoExtrasDumpSchema,
        RequestEventType.CANCELLED.value: NoExtrasDumpSchema,
        RequestEventType.REMOVED.value: NoExtrasDumpSchema,
        RequestEventType.EXPIRED.value: NoExtrasDumpSchema,
    }
    type_field_remove = False

    def get_obj_type(self, obj):
        """Return key of type_schemas to use given object to dump."""
        return obj.type
