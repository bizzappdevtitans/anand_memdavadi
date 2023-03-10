from odoo import api, models, fields
from datetime import date


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "school.teacher"

    name = fields.Char(string="Teacher Name")
    age = fields.Integer(string="Age", compute="_compute_age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    experience = fields.Integer(string="Years of Experience")
    school = fields.Many2one("school.management", string="School", ondelete="cascade")
    code = fields.Char(string="School Code")

    dob = fields.Date(string="Date of Birth")

    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    @api.onchange("school")
    def onchange_code(self):
        print("onchange triggerred")
        print(self.school)
        if self.school:
            if self.school.code:
                self.code = self.school.code
        else:
            self.code = ""
