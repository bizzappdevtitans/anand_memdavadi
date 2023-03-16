from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "school.student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "standard asc"

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
    is_bday = fields.Boolean(string="B'day", default=False)
    image = fields.Binary("Student Photo")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    email = fields.Char(string="Email")
    user_id = fields.Many2one("res.users", string="Select User")
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
        default="1",
    )
    mentor = fields.Many2one("school.teacher", string="Mentor")
    school = fields.Many2one("school.management", string="School", ondelete="cascade")
    active = fields.Boolean("Active", default=True)
    maths_marks = fields.Integer(string="Maths Marks", tracking=True)
    english_marks = fields.Integer(string="English Marks", tracking=True)
    science_marks = fields.Integer(string="Science Marks", tracking=True)
    contact_number = fields.Integer(string="Phone Number")

    """This method is used for cron-job during student birthday"""

    def check_bday(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        students = self.env["school.student"].search([("active", "=", True)])
        for student in students:
            if student.email:
                bday_month = student.dob.strftime("%m")
                bday_date = student.dob.strftime("%d")
                if bday_date == today_date and bday_month == today_month:
                    print("Happy Birthday Dear", student.name)
                    template = self.env.ref(
                        "school_management.student_birthday_email_template"
                    )
                    template.send_mail(student.id)
            else:
                raise ValidationError(("Email is mandatory"))

    """This method is used for name search """

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

    """This method is used for validation that marks should not be greatter than 100"""

    @api.constrains("maths_marks", "english_marks", "science_marks")
    def check_marks(self):
        for rec in self:
            if (
                rec.maths_marks > 100
                or rec.english_marks > 100
                or rec.science_marks > 100
            ):
                raise ValidationError(("Marks should be less than 100"))

    """This method is used for calculating age of student"""

    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 0

    """Create ORM method"""

    @api.model
    def create(self, vals):
        if vals.get("reference_no", _("New")) == _("New"):
            vals["reference_no"] = self.env["ir.sequence"].next_by_code(
                "school.student"
            ) or _("New")
            res = super(SchoolStudent, self).create(vals)
            if not vals.get("gender"):
                vals["gender"] = "others"
                if vals.get("gender") == "male":
                    res["name"] = "Mr." + res["name"]
                elif vals.get("gender") == "female":
                    res["name"] = "Mrs." + res["name"]
                else:
                    return res
        return res

    """Default get method to return default values of fields"""

    @api.model
    def default_get(self, fields):
        rec = super(SchoolStudent, self).default_get(fields)
        print("Fields--------->", fields)
        print("rec------------>", rec)
        return rec

    """Name get function used add reference number and student name instead of student id"""

    def name_get(self):
        stud_list = []
        for rec in self:
            stud_list.append((rec.id, "%s - %s" % (rec.reference_no, rec.name)))
        return stud_list

    """This function is used to send mail using button"""

    def action_send_mail(self):
        template = self.env.ref("school_management.student_birthday_email_template")
        for rec in self:
            if rec.email:
                template.send_mail(rec.id, force_send=True)

    def action_share_whatsapp(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        students = self.env["school.student"].search([("active", "=", True)])
        for student in students:
            if student.contact_number:
                print(student.contact_number)
                bday_month = student.dob.strftime("%m")
                bday_date = student.dob.strftime("%d")
                if (
                    bday_date == today_date
                    and bday_month == today_month
                    and student.contact_number
                ):
                    print("BDAY MATCHED")
                    message = "Hi %s, Have happiest B'day & Enjoy yours day!"%(student.name)
                    wp_url = "https://api.whatsapp.com"
                    print(message)
                    return{
                        "type": "ir.actions.act_url",
                        "url": wp_url,
                        "target": "current"
                        }


    def message_in_general_channel(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        students = self.env["school.student"].search([("active", "=", True)])
        for student in students:
            bday_month = student.dob.strftime("%m")
            bday_date = student.dob.strftime("%d")
            if bday_date == today_date and bday_month == today_month:
                message = "Happy Birthday %s" % (student.name)
                channel_id = self.env.ref("mail.channel_all_employees").id
                channel = self.env["mail.channel"].browse(channel_id)
                channel.message_post(
                    body=(message),
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment",
                )
