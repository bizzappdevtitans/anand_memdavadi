from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _prepare_stock_move_vals(self):
        vals = super(StockMoveLine, self)._prepare_stock_move_vals()
        vals["product_weight"] = self.picking_id.product_weight
        return vals
