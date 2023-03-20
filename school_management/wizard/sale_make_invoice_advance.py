from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        invoice_vals.update({"invoice_des": order.des})
        print("invoice_vals", invoice_vals)
        return invoice_vals
