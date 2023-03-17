from odoo import models, fields


class SchoolCourse(models.Model):
    _name = "school.course"
    _description = "Courses available in school"
    _rec_name = "stream"

    stream = fields.Selection(
        [("Science", "Science"), ("Arts", "Arts"), ("Commerce", "Commerce")],
        string="Course stream",
    )
    image = fields.Binary()
    student_details = fields.One2many("school.student", "course")
    subject = fields.One2many("school.subject", "course")
    sub = fields.Many2many("school.subject", string="Subject to study:")
