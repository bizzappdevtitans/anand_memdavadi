from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class StudentStudent(models.Model):
    _name = "school.student"
    _description = "school.student"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Student Name", required=True)
    reference_no = fields.Char(
        string="Student Reference",
        readonly=True,
        required=True,
        default=lambda self: _("New"),
    )
    age = fields.Integer(
        string="Age", help="Student's Age", compute="_compute_age", tracking=True
    )
    id = fields.Integer(string="School")
    transport = fields.Boolean(string="Transportaion")
    is_favorite = fields.Boolean(string="Fav")
    image = fields.Binary("Student Photo")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    hobby = fields.Text(string="Hobby")
    dob = fields.Date(string="Date of Birth")
    standard = fields.Integer(string="Standard", tracking=True)
    student_blood_group = fields.Selection(
        [("A+", "A+ve"), ("B+", "B+ve"), ("O+", "O+ve"), ("AB+", "AB+ve")]
    )
    joining_date = fields.Datetime(string="Date of joining")
    info = fields.Html(string="Information")
    course = fields.Many2one("school.course", string="Please select course")
    listening = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Listening",
        default="1",
    )
    reading = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Reading",
        default="1",
    )
    writing = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Writing",
        default="1",
    )
    speaking = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Speaking",
        default="1")
    mentor = fields.Many2one("school.teacher", string="Mentor")
    school = fields.Many2one("school.management", string="School", ondelete="cascade")

    id = fields.Integer(string="School ID", related="name.id")

    maths_marks = fields.Integer(string="Maths Marks", tracking=True)
    english_marks = fields.Integer(string="English Marks", tracking=True)
    science_marks = fields.Integer(string="Science Marks", tracking=True)
    count_student = fields.Integer(compute="_comput_student")

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
                    ("school_code", operator, name),
                ]
            )
            return rec.name_get()
        return self.search([("name", operator, name)] + args, limit=limit).name_get()

    @api.constrains("maths_marks", "english_marks", "science_marks")
    def check_marks(self):
        for rec in self:
            if (
                rec.maths_marks > 100
                or rec.english_marks > 100
                or rec.science_marks > 100
            ):
                raise ValidationError(("Marks should be less than 100"))

    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    _sql_constraints = [("unique_tag_name", "unique (name)", "Student already exists")]

    @api.onchange("school")
    def names(self):
        print("school", self.school)

    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "school.student"
            ) or _("New")
            res = super(StudentStudent, self).create(vals)
            if not vals.get("gender"):
                vals["gender"] = "others"
                if vals.get("gender") == "male":
                    res["name"] = "Mr." + res["name"]
                elif vals.get("gender") == "female":
                    res["name"] = "Mrs." + res["name"]
                else:
                    return res
        return res

    @api.model
    def default_get(self, fields):
        rec = super(StudentStudent, self).default_get(fields)
        print("Fields--------->", fields)
        print("rec------------>", rec)
        return rec

    def name_get(self):
        stud_list = []
        for rec in self:
            stud_list.append((rec.id, "%s - %s" % (rec.reference_no, rec.name)))
        return stud_list
