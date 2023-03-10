from odoo import models, fields


class SchoolPrincipal(models.Model):
    _name = "school.principal"
    _description = "school.principal"
    _rec_name = "principal"

    principal = fields.Char(string="Principal Name", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender")
    experience = fields.Integer(string="Years of Experience")
    school = fields.Many2one("school.management", string="School", ondelete="cascade")
