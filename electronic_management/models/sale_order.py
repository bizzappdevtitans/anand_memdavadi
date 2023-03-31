from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_emp = fields.Many2one(
        "electronic.employee", string="Sale Employee", required=True, ondelete="cascade"
    )
    branch = fields.Many2one("electronic.management", string="Branch", ondelete="cascade")

    def whatsapp_invoice(self):
        message = 'Hi %s, we received your order %s for product %s. Your payment amount is %s. Thank you!'% (self.partner_id.name,self.name,self.order_line.product_id.name,self.amount_total)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.partner_id.phone, message)
        return {
                'type': 'ir.actions.act_url',
                'target': 'new',
                'url': whatsapp_api_url
                }

    def product_example(self):
        product = self.env["sale.order.line"].search([("order_line.product_template_id")])
        print(product)

    @api.onchange("branch")
    def onchange_branch(self):
        return {
                "domain": {"sale_emp": [("branch", "=", self.branch.id)]}
                }
