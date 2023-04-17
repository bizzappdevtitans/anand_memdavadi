from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_emp = fields.Many2one(
        "electronic.employee", string="Sale Employee", required=True, ondelete="cascade"
    )
    branch = fields.Many2one(
        "electronic.management", string="Branch", ondelete="cascade"
    )

    """WhatsApp Integration in SO"""

    def whatsapp_invoice(self):
        message = (
            "Hi %s, we received your order %s for product %s. Your payment amount is %s. Thank you!"
            % (
                self.partner_id.name,
                self.name,
                self.order_line.product_id.name,
                self.amount_total,
            )
        )
        whatsapp_api_url = "https://api.whatsapp.com/send?phone=%s&text=%s" % (
            self.partner_id.phone,
            message,
        )
        return {"type": "ir.actions.act_url", "target": "new", "url": whatsapp_api_url}

    """When branch changes than employee list will be shown of that particular branch"""

    @api.onchange("branch")
    def onchange_branch(self):
        return {"domain": {"sale_emp": [("branch", "=", self.branch.id)]}}

    """ When partner id has child ids and if they have boolean-True and type delivery
    than returns in partner_delivery_id in Sale Order, if doesn't exist than return other type """

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        vals = super(SaleOrder, self).onchange_partner_id()
        delivery_type_id = self.partner_id.child_ids.filtered(
            lambda la: la.bool_true == True and la.type == "delivery"
        )
        self.partner_shipping_id = delivery_type_id[:1]
        if not delivery_type_id:
            other_type_id = self.partner_id.child_ids.filtered(
                lambda la: la.type == "other"
            )
            self.partner_shipping_id = other_type_id[:1]
        return vals

    def _action_confirm(self):
        return
