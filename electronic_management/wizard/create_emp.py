from odoo import fields, api, models


class Employee(models.TransientModel):
    _name = "create.emp.wizard"
    _description = "Create Employee with Wizard"

    emp_name = fields.Char(string="Employee Name", required=True)
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age")
