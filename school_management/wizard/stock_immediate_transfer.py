from odoo import models, _


class StockImmediateTransfer(models.TransientModel):
    _inherit = "stock.immediate.transfer"

    def process(self):
        sale_orders = self.env["sale.order"].browse(self._context.get("active_ids", []))
        sale_orders._create_invoices()
        if self._context.get("open_invoices", False):
            return sale_orders.action_view_invoice()
        view = self.env.ref("account.view_move_form")
        return {"type": "ir.actions.act_window_close"}
        # vals = super(StockImmediateTransfer, self).process()
        # ids = self.env[('stock.picking')].search([])
        # for rec in ids.move_lines:
        #     sale_id = rec.sale_line_id
        #     if sale_id:
        #         sale_id['product_weight'] = rec.product_weight
        # return vals
