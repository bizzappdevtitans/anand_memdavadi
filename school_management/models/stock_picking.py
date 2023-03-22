from odoo import models, fields


class Picking(models.Model):
    _inherit = "stock.picking"

    sp_des = fields.Char(string="Delivery Description")






 #     invoice_vals = self.env['sale_make_invoice_advance'].search(['invoice_line_ids'])
 # view = self.env.ref("account.view_move_form")
 #        return {
 #            "name": _("Create Invoice"),
 #            "type": "ir.actions.act_window",
 #            "view_mode": "form",
 #            "res_model": "account.move",
 #            "views": [(view.id, "form")],
 #            "view_id": view.id,
 #            "target": "new",
 #            "context": invoice_vals
 #        }
