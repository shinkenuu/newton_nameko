from marshmallow import EXCLUDE, fields, Schema, validate

from .constants import (
    SUM_OPERATION_NAME,
    SUBTRACT_OPERATION_NAME,
    MULTIPLY_OPERATION_NAME,
    DIVIDE_OPERATION_NAME,
)

_VALID_OPERATIONS = (
    SUM_OPERATION_NAME,
    SUBTRACT_OPERATION_NAME,
    MULTIPLY_OPERATION_NAME,
    DIVIDE_OPERATION_NAME,
)


class ArithmeticProcedureSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    operation = fields.String(validate=validate.OneOf(_VALID_OPERATIONS), required=True)
    arguments = fields.List(fields.Float(), required=True)
    result = fields.Float(required=True, allow_none=True)
    status = fields.String(required=True)
