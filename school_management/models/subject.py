from odoo import models, fields, api


class SchoolTransportService(models.Model):
    _name = "school.subject"
    _description = "Subjects in School"

    name = fields.Char(string="Subject Name", required=True)
    code = fields.Char(string="Subject Code")

    _sql_constraints = [("unique_tag_name", "unique (name)", "Subject already exists")]
