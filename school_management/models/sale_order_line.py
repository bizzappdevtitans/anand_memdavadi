from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    no = fields.Integer(string="Number")

    def _timesheet_create_task_prepare_values(self, project):
        values = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(
            project
        )
        values.update({"task_des": self.order_id.project_des})
        return values

    def _timesheet_create_project_prepare_values(self):
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        values["pro_des"] = self.order_id.project_des
        return values
