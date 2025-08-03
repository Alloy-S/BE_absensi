from marshmallow import Schema, fields

class PaginationReq(Schema):
    page = fields.Integer(required=False, load_default=1)
    size = fields.Integer(required=False, load_default=10)
    search = fields.String(required=False, load_default="")

class PaginationApprovalReq(Schema):
    page = fields.Integer(required=False, load_default=1)
    size = fields.Integer(required=False, load_default=10)
    filter_status = fields.String(required=False, load_default="All", data_key="filter-status")
    filter_month = fields.String(required=False, data_key="filter-month")

class PaginationAllApproval(Schema):
    page = fields.Integer(required=False, load_default=1)
    size = fields.Integer(required=False, load_default=10)
    filter_tipe_approval = fields.String(required=False, load_default="All", data_key="filter-tipe-approval")
    filter_month = fields.String(required=False, data_key="filter-month")


class PaginationHistoryReq(Schema):
    page = fields.Integer(required=False, load_default=1)
    size = fields.Integer(required=False, load_default=10)
    filter_status = fields.String(required=False, load_default="All", data_key="filter-status")
    filter_month = fields.String(required=False, data_key="filter-month")
    search = fields.String(required=False, allow_none=True)
