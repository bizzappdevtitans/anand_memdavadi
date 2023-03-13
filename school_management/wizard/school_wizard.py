from odoo import fields, models, _


class SchoolWizard(models.TransientModel):
    _name = "school.wizard"
    _description = "Basic wizard for school"

    name = fields.Char(string="Student Name", required=True)
    age = fields.Integer(string="Age", help="Student's Age")
    image = fields.Binary("Student Photo")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    school = fields.Many2one("school.management", string="School")
    hobby = fields.Text(string="Hobby")
    dob = fields.Date(string="Date of Birth")
    standard = fields.Integer(string="Standard")
    student_blood_group = fields.Selection(
        [("A+", "A+ve"), ("B+", "B+ve"), ("O+", "O+ve"), ("AB+", "AB+ve")]
    )
    joining_date = fields.Datetime(string="Date of joining")
    info = fields.Html(string="Information")
    course = fields.Many2one("school.course", string="Please select course")
    listening = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Listening",
        default="0",
    )
    reading = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Reading",
        default="0",
    )
    writing = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Writing",
        default="0",
    )
    speaking = fields.Selection(
        [("0", "Normal"), ("1", "Good"), ("2", "Very Good"), ("3", "Excellent")],
        "Speaking",
        default="0",
    )
    maths_marks = fields.Integer(string="Maths Marks")
    english_marks = fields.Integer(string="English Marks")
    science_marks = fields.Integer(string="Science Marks")

    def action_view_teacher_tree(self):
        action = self.env.ref('school_management.action_school_teacher').read()[0]
        return action

    def action_create_student_record(self):
        vals = {
            "name": self.name,
            "age": self.age,
            "image": self.image,
            "gender": self.gender,
            "hobby": self.hobby,
            "dob": self.dob,
            "standard": self.standard,
            "student_blood_group": self.student_blood_group,
            "joining_date": self.joining_date,
            "info": self.info,
            "course": self.course,
            "listening": self.listening,
            "reading": self.reading,
            "writing": self.writing,
            "speaking": self.speaking,
            "maths_marks": self.maths_marks,
            "english_marks": self.english_marks,
            "science_marks": self.science_marks,
        }
        student_record = self.env["school.student"].create(vals)
        print("Student Record", student_record.id)

        return {
            "name": _("Student Record"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "school.student",
            "res_id": student_record.id,
            "target": "current",
        }
