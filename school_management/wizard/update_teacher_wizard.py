from odoo import fields, models, _


class UpdateTeacher(models.TransientModel):
    _name = "update.teacher"
    _description = "Update values of Teacher using wizard"

    experience = fields.Integer(string="Years of Experience")
    school = fields.Many2one("school.management", string="School", ondelete="cascade")

    def action_update_teacher_record(self):
        active_id = self._context.get('active_id')
        teacher_record = self.env["school.teacher"].browse(active_id)
        vals = {
            "experience": self.experience,
            "school": self.school
        }
        teacher_record.write(vals)

        print("Upadted Record", teacher_record.id)
        return {
            "name": _("Teacher Record Updated"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "school.teacher",
            "res_id": teacher_record.id,
            "target": "current",
        }
