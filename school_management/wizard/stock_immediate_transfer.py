from odoo import models


class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        vals = super(StockImmediateTransfer, self).process()
        ids = self.env[('stock.picking')].search([])
        for rec in ids.move_lines:
            sale_id = rec.sale_line_id
            if sale_id:
                sale_id['product_weight'] = rec.product_weight
        return vals
