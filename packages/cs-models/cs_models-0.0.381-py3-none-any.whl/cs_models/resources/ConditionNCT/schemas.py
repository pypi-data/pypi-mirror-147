from marshmallow import (
    Schema,
    fields,
    validate,
)


class ConditionNCTResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    condition_id = fields.Integer(required=True)
    nct_study_id = fields.Integer(required=True)
    score = fields.Float(required=True)
    updated_at = fields.DateTime()
