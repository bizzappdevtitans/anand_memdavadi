from odoo import models, fields
from datetime import date


class SchoolPrincipal(models.Model):
    _name = "school.principal"
    _description = "school.principal"
    _rec_name = "principal"
    _order = "principal desc"

    principal = fields.Char(string="Principal Name", required=True)
    age = fields.Integer(string="Age", compute="_compute_age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender")
    experience = fields.Integer(string="Years of Experience")
    school = fields.Many2one("school.management", string="School", ondelete="cascade")
    dob = fields.Date(string="Date of Birth")
    active = fields.Boolean("Active", default=True)

    """Function used to calculate age of principal"""
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    """Function used for cron job message in terminal"""
    def check_bday(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        principals = self.env["school.principal"].search([("active", "=", True)])
        for principal in principals:
            bday_month = principal.dob.strftime("%m")
            bday_date = principal.dob.strftime("%d")
            if bday_date == today_date and bday_month == today_month:
                print("Happy Birthday Dear", principal.principal)
