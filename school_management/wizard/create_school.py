from odoo import fields, models, api, _


class CreateSchool(models.TransientModel):
    _name = "create.school"
    _description = "Create School from Admission"

    name = fields.Char(string="School Name", required=True)
    address = fields.Text(string="Address of School")
    phone = fields.Char(string="Phone Number")
    online_class = fields.Boolean(string="Online Class", required=True)
    website = fields.Char(string="Website")
    image = fields.Image(string="School Photo")
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

    def action_create_school_record(self):
        vals = {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "online_class": self.online_class,
            "website": self.website,
            "image": self.image,
            "code": self.code,
            "school_type": self.school_type,
            "fees": self.fees,
            "picnic_fees": self.picnic_fees,
            "tuition_fees": self.tuition_fees,
            "lib_fees": self.lib_fees,
        }
        school_record = self.env["school.management"].create(vals)
        print("School Record", school_record.id)

        return {
            "name": _("School Record"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "school.management",
            "res_id": school_record.id,
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
