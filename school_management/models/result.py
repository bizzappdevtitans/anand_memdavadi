from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SchoolResult(models.Model):
    _name = "school.result"
    _description = "Shows result of the student"
    _inherit = "school.teacher"
    _order = "name desc"

    name = fields.Many2one("school.student", string="Select Student", required=True)
    school = fields.Many2one(
        "school.management", string="School", ondelete="cascade", related="name.school"
    )
    standard = fields.Integer(string="Standard", related="name.standard")
    course = fields.Many2one(
        "school.course",
        string="Course",
        related="name.course",
    )
    experience = fields.Integer(string="Years of Experience")

    maths_marks = fields.Integer(string="Maths Marks", related="name.maths_marks")
    english_marks = fields.Integer(string="English Marks", related="name.english_marks")
    science_marks = fields.Integer(string="Science Marks", related="name.science_marks")
    state = fields.Selection(
        [
            ("fail", "FAIL"),
            ("pass", "PASS"),
        ],
        default="fail",
        string="Status",
    )
    percentage = fields.Float(string="Percentage", compute="_compute_percentage")

    @api.depends("maths_marks", "english_marks", "science_marks", "percentage")
    def _compute_percentage(self):
        for rec in self:
            total = 0
            if rec.maths_marks:
                total += rec.maths_marks
            if rec.english_marks:
                total += rec.english_marks
            if rec.science_marks:
                total += rec.science_marks
            rec.percentage = total / 3

    @api.onchange("percentage", "state")
    def check_pass(self):
        for rec in self:
            if rec.percentage <= 40:
                rec.state = "fail"

    @api.onchange("percentage", "state")
    def check_pass1(self):
        for rec in self:
            if rec.percentage > 40:
                rec.state = "pass"

    def unlink(self):
        if self.state == "pass":
            raise ValidationError(_("You can delete only fail result records"))
        return super(SchoolResult, self).unlink()
