from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SchoolManagement(models.Model):
    _name = "school.management"
    _description = "school.management"
    _order = "name desc"

    name = fields.Char(string="School Name", required=True)
    id = fields.Integer(string="School")
    address = fields.Text(string="Address of School")
    phone = fields.Char(string="Phone Number")
    online_class = fields.Boolean(string="Online Class", required=True)
    course = fields.Many2many("school.course", string="Select Course")
    website = fields.Char(string="Website")
    image = fields.Image()
    code = fields.Char(string="School Code")

    lib_fees = fields.Float(string="Library Fees")
    tuition_fees = fields.Float(string="Tuition Fees", compute="compute_tuition_fees")
    picnic_fees = fields.Float(string="Picnic Fees")
    fees = fields.Float(
        string="School Fees", required=True, digits=(4, 3), compute="compute_fees"
    )
    school_type = fields.Selection(
        [("public", "Public School"), ("private", "Private School")]
    )
    student_count = fields.Integer("student count", compute="_compute_student")
    _sql_constraints = [("unique_tag_name", "unique (name)", "school already exists")]

    @api.depends("student_count")
    def _compute_student(self):
        for rec in self:
            rec.student_count = self.env["school.student"].search_count(
                [("school", "=", "self.id")]
            )
            student_count = rec.student_count
            print(student_count)

    @api.model
    def name_get(self):
        school_list = []
        for rec in self:
            school_list.append((rec.id, "%s - %s" % (rec.code, rec.name)))
        return school_list

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        if name:
            rec = self.search(
                [
                    "|",
                    "|",
                    ("name", operator, name),
                    ("id", operator, name),
                    ("phone", operator, name),
                ]
            )
            return rec.name_get()
        return self.search([("name", operator, name)] + args, limit=limit).name_get()

    def action_url(self):
        return {
                "type": "ir.actions.act_url",
                "target": "new",
                'url': self.website}

    def action_open_student(self):
        return {
            "type": "ir.actions.act_window",
            "name": "students",
            "res_model": "school.student",
            "view_mode": "tree,form",
            "target": "current",
        }

    @api.depends("tuition_fees")
    def compute_tuition_fees(self):
        for rec in self:
            if rec.school_type == "public":
                rec.tuition_fees = 100
            elif rec.school_type == "private":
                rec.tuition_fees = 300

    @api.depends("lib_fees", "tuition_fees", "picnic_fees")
    def compute_fees(self):
        for rec in self:
            fees = 0
            if rec.lib_fees:
                fees += rec.lib_fees
            if rec.tuition_fees:
                fees += rec.tuition_fees
            if rec.picnic_fees:
                fees += rec.picnic_fees
            rec.fees = fees

    @api.constrains("name")
    def check_name(self):
        for rec in self:
            schools = self.env["school.management"].search(
                [("name", "=", rec.name), ("code", "!=", "rec.code")]
            )
            print(schools)
            if len(schools) > 1:
                raise ValidationError(("Name - %s already exists" % rec.name))

    @api.constrains("phone")
    def check_phone(self):
        for rec in self:
            if len(rec.phone) < 10 or len(rec.phone) > 10:
                raise ValidationError(("Phone number should be of 10 digit only"))
