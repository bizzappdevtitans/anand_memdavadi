from odoo import models, fields, api


class SchoolManipulation(models.Model):
    _name = "school.manipulation"
    _description = "Data Manipulation"

    name = fields.Char(string="Student Name")
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")], string="Gender"
    )
    stud = fields.Many2one("school.student", string="Select Student to delete")
    school_id = fields.Many2one("school.management", string="Select School to delete")

    @api.model
    def create_details(self, vals):
        vals = {
            "name": self.name,
            "dob": self.dob,
            "gender": self.gender,
        }
        self.env["school.student"].create(vals)
        print("DATA INSERTED--------->")

    def action_browse_details(self):
        ans = self.env["school.student"].browse([38]).name
        print("Browse Answer------->", ans)

    def write_details(self):
        vals = {"name": self.name, "dob": self.dob, "gender": self.gender}
        self.env["school.student"].browse(25).write(vals)

    def search_details(self):
        ans = self.env["school.student"].search([("gender", "=", "male")])
        print("Search Details-------->", ans)

    def search_count_details(self):
        ans = self.env["school.student"].search_count([("gender", "=", "male")])
        print("Search Count Details-------->", ans)

    def ensure_one_details(self):
        self.ensure_one()
        ans = self.env["school.student"].browse([1]).name
        print("Check ENSUREONE", ans)

    def query_action(self):
        query = """select id , name from school_management"""
        self.env.cr.execute(query)
        stu = self.env.cr.fetchall()
        print(stu)
