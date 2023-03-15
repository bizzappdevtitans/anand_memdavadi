from odoo import api, models, fields
from datetime import date


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "school.teacher"
    _order = "name desc"

    name = fields.Char(string="Teacher Name")
    age = fields.Integer(string="Age", compute="_compute_age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    experience = fields.Integer(string="Years of Experience")
    school = fields.Many2one("school.management", string="School", ondelete="cascade")
    code = fields.Char(string="School Code")
    dob = fields.Date(string="Date of Birth")

    """Function used for cron job message in terminal"""
    def check_bday(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        teachers = self.env["school.teacher"].search([])
        for teacher in teachers:
            bday_month = teacher.dob.strftime("%m")
            bday_date = teacher.dob.strftime("%d")
            if bday_date == today_date and bday_month == today_month:
                print("Happy Birthday Dear", teacher.name)

    """Function used to calculate teachers age"""
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    """Function used to change school code when school is changed"""
    @api.onchange("school")
    def onchange_code(self):
        print("onchange triggerred")
        print(self.school)
        if self.school:
            if self.school.code:
                self.code = self.school.code
        else:
            self.code = ""
