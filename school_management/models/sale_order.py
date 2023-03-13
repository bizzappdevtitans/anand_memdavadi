from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    no = fields.Integer(string="Number")
    des = fields.Char(string="Description For Invoice")
    delivery_des = fields.Char(string="Description For Delivery")
    project_des = fields.Char(string="Description For Project")
    purchase_order_des = fields.Char(string="Description For PO")
    manu_order_des = fields.Char(string="Description for MO")

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals["invoice_des"] = self.des
        return invoice_vals
