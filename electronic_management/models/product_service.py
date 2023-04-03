from odoo import fields, api, models, _
from datetime import date, datetime
from odoo.exceptions import ValidationError


class ProductService(models.Model):
    _name = "product.service"
    _description = "Provide Service to Product"
    _rec_name = "invoice"

    invoice = fields.Many2one("account.move", "Select Invoice")
    state = fields.Selection(
        [
            ("unavailable", "Unavailable"),
            ("available", "Available"),
        ],
        default="unavailable",
        string="Status",
    )
    customer_name = fields.Many2one(
        string="Customer Name", related="invoice.partner_id"
    )
    invoice_date = fields.Date(
        "Invoice Date", related="invoice.invoice_date", readonly=True
    )
    product = fields.Many2one(
        string="Product Name",
        related="invoice.invoice_line_ids.product_id",
        readonly=True,
    )
    phone = fields.Char(string="Contact Number", related="customer_name.phone")
    invoice_currency_id = fields.Many2one(
        string="Currency ID", related="invoice.currency_id"
    )
    invoice_price = fields.Float(
        string="Product Price",
        related="invoice.invoice_line_ids.price_unit",
        readonly=True,
    )
    fault = fields.Text(string="Fault in product")
    service_date = fields.Date(
        string="Service Date", default=datetime.today(), readonly=True
    )
    pickup_date = fields.Date(string="Pickup Date")

    """ Here service available or not is determined """

    def check_difference(self):
        today = fields.Date.today()
        for rec in self:
            if rec.invoice.invoice_date:
                x = today - rec.invoice.invoice_date
                print(x.days, "\n\ndifference\n\n")
                if x.days <= 365:
                    print("\nService Available\n")
                    self.state = "available"
                else:
                    message = "Service Unavailable"
                    return {
                        "type": "ir.actions.client",
                        "tag": "display_notification",
                        "params": {
                            "message": message,
                            "type": "warning",
                            "sticky": False,
                        },
                    }

    """WhatsApp Integration to send information through whatsapp"""

    def whatsapp_invoice(self):
        message = (
            "Hi %s, we received your service request for product %s has fault of %s.Please collect your product on %s"
            % (self.customer_name.name, self.product.name, self.fault, self.pickup_date)
        )
        whatsapp_api_url = "https://api.whatsapp.com/send?phone=%s&text=%s" % (
            self.phone,
            message,
        )
        return {"type": "ir.actions.act_url", "target": "new", "url": whatsapp_api_url}

    """ValidationError for pickup date should be greater than today date"""

    @api.constrains("service_date", "pickup_date")
    def date_constrains(self):
        for rec in self:
            if rec.pickup_date:
                if rec.pickup_date <= rec.service_date:
                    raise ValidationError(
                        _("Pickup Date Must be greater than Today Date...")
                    )

    """ValidationError to delete record"""

    @api.ondelete(at_uninstall=False)
    def check_state(self):
        for record in self:
            if record.state == "available":
                raise ValidationError(
                    _("You can delete record of unavailable state only")
                )

    """Server action to delete unavailable service"""

    def action_archieved_unavailable_service(self):
        self.env["product.service"].search([("state", "=", "unavailable")]).write(
            {"active": False}
        )
