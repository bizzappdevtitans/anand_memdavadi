from odoo import fields, api, models, _


class Employee(models.TransientModel):
    _name = "create.emp.wizard"
    _description = "Create Employee with Wizard"

    emp_name = fields.Char(string="Employee Name", required=True)
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
    )
    email = fields.Char(string="Email")
    joining_date = fields.Datetime(string="Date of joining")
    contact_no = fields.Char(string="Phone Number")
    adhaar_no = fields.Char(string="Adhaar Number")
    pan_no = fields.Char(string="PAN Number")
    qualification = fields.Selection(
        [
            ("under_graduate", "Under Graduate"),
            ("graduate", "Graduate"),
            ("post_graduate", "Post Graduate"),
        ],
        string="Qualification",
    )
    address = fields.Text(string="Residential Address")
    user_id = fields.Many2one("res.users", string="Select User")
    branch = fields.Many2one(
        "electronic.management", string="Branch"
    )

    def action_create_employee_record(self):
        vals = {
            "emp_name": self.emp_name,
            "dob": self.dob,
            "gender": self.gender,
            "email": self.email,
            "joining_date": self.joining_date,
            "contact_no": self.contact_no,
            "adhaar_no": self.adhaar_no,
            "pan_no": self.pan_no,
            "qualification": self.qualification,
            "address": self.address,

        }
        emp_record = self.env["electronic.employee"].create(vals)

        return {
            "name": _("Employee Record"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "electronic.employee",
            "res_id": emp_record.id,
            "target": "current",
        }
