from odoo import models, fields, api


class SchoolTransportService(models.Model):
    _name = "school.transport"
    _description = "Transportation Service"
    _order = "name desc"

    date = fields.Datetime(string="Date of Joining")
    name = fields.Many2one("school.student", string="Select Student")
    school = fields.Many2one("school.management", string="School", ondelete="cascade", related="name.school")
    orphan = fields.Boolean(string="Orphan")
    parent = fields.Char(string="Parent Name")
    contact_number = fields.Integer(string="Phone Number")
    address = fields.Char(string="Enter Address")
    distance = fields.Integer(string="Travel Distance")
    transport_fees = fields.Integer(
        string="Transportation Charge", compute="_compute_charge"
    )
    status = fields.Selection(
        [("new", "New Student"), ("old", "Existed-Student")], string="Student Status"
    )
    medical_issues = fields.Boolean(string="Medical Issues", default="1")
    issues = fields.Selection(
        [("diabetes", "Diabetes"), ("epilepsy", "Epilepsy"), ("other", "Other")],
        string="Please select issues",
    )
    state = fields.Selection(
        [
            ("new", "Start New Service"),
            ("in", "In Service"),
            ("cancel", "Service Cancel"),
        ],
        default="new",
        string="Status",
    )
    _sql_constraints = [("unique_tag_name", "unique (name)", "User already exists")]

    def action_in(self):
        self.state = "in"

    def action_cancel(self):
        self.state = "cancel"

    def action_new(self):
        self.state = "new"

    @api.depends("distance")
    def _compute_charge(self):
        for rec in self:
            transport_fees = 0
            if rec.distance:
                rec.transport_fees = rec.distance * 500
            transport_fees = rec.transport_fees

    _sql_constraints = [("unique_tag_name", "unique (name)", "Student already exists")]
