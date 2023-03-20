from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class SchoolManagement(models.Model):
    _name = "school.admission"
    _description = "school.admission"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name desc"

    name = fields.Char(string="New Applicant Name")
    active = fields.Boolean("Active", default=True)
    standard = fields.Selection(
        [
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
        ]
    )
    is_appointment = fields.Boolean(
        string="Appointment ?", compute="_compute_appointment"
    )
    school = fields.Many2one("school.management", string="School", ondelete="cascade")
    is_favorite = fields.Boolean()
    state = fields.Selection(
        [
            ("new", "New Applicant"),
            ("progress", "In Progress"),
            ("confirm", "Admission Confirmed"),
            ("cancel", "Admission Cancelled"),
        ],
        default="new",
        string="Status",
        tracking=True,
    )
    app_date = fields.Date(string="Admission Appointment")
    percentage = fields.Float(string="Percentage", compute="_compute_percentage")
    maths_marks = fields.Integer(string="Maths Marks")
    english_marks = fields.Integer(string="English Marks")
    science_marks = fields.Integer(string="Science Marks")
    doc_info = fields.Text(string="Documentation")
    number = fields.Integer(string="Phone Number")

    """ Action for confirm button"""

    def action_confirm(self):
        self.state = "confirm"

    """Action for cron job for cancelled admission"""

    def action_archieved_cancel_admission(self):
        self.env["school.admission"].search([("state", "=", "cancel")]).write(
            {"active": False}
        )

    """To calculate percentage"""

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

    """Constrains for deleting record, record should be in cancel state"""

    @api.ondelete(at_uninstall=False)
    def check_state(self):
        for record in self:
            if (
                record.state == "new"
                or record.state == "progress"
                or record.state == "confirm"
            ):
                raise ValidationError(
                    _("You can delete admission record of cancel state only")
                )

    """If student has less than 60% state changes to admission cancel"""

    @api.onchange("percentage", "state")
    def check_pass(self):
        for rec in self:
            if rec.percentage <= 60:
                rec.state = "cancel"

    """If student has greater than 85% state changes to admission confirm"""

    @api.onchange("percentage", "state")
    def check_pass1(self):
        for rec in self:
            if rec.percentage >= 85:
                rec.state = "confirm"

    """Else state will be in progress """

    @api.onchange("percentage", "state")
    def check_pass2(self):
        for rec in self:
            if rec.percentage > 60 and rec.percentage < 85:
                rec.state = "progress"

    """If admission confirmed & today is appointment day it notifies"""

    @api.depends("app_date", "state")
    def _compute_appointment(self):
        for rec in self:
            rec.is_appointment = False
            if rec.state:
                if rec.app_date:
                    today = date.today()
                    if (
                        today.day == rec.app_date.day
                        and today.month == rec.app_date.month
                        and today.year == rec.app_date.year
                        and rec.state == "confirm"
                    ):
                        is_appointment = True
                        rec.is_appointment = is_appointment

    def action_share_whatsapp(self):
        if self.is_appointment == True and self.number:
            message = "Hi %s you have admission appointment today" % (self.name)
            whatsapp_api_url = "https://api.whatsapp.com/send?phone%s&text=%s" % (
                self.number,
                message,
            )
            return {
                "type": "ir.actions.act_url",
                "target": "new",
                "url": whatsapp_api_url,
            }
        else:
            raise ValidationError("Invalid Number")
