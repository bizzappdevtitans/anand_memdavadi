from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import date
import datetime


class Partner(models.Model):
    _inherit = "res.partner"

    has_child = fields.Boolean(string="Has Child ?", compute="compute_child")
    bool_true = fields.Boolean(string="True?")

    @api.depends("child_ids")
    def compute_child(self):
        for rec in self:
            if rec.child_ids:
                rec.has_child = True
            else:
                rec.has_child = False

    """used for checking Independence day for Cronjob"""

    def check_independence_day(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        customers = self.env["res.partner"].search([])
        for customer in customers:
            if customer.email:
                d = datetime.date(2023, 8, 15)
                independence_month = d.strftime("%m")
                independence_date = d.strftime("%d")
                if (
                    today_date == independence_date
                    and today_month == independence_month
                ):
                    template = self.env.ref(
                        "electronic_management.Independence_Day_Mail_Template"
                    )
                    template.send_mail(customer.id)

    """used for checking republic day for Cronjob"""

    def check_republic_day(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        customers = self.env["res.partner"].search([])
        for customer in customers:
            if customer.email:
                d = datetime.date(2023, 1, 26)
                republic_month = d.strftime("%m")
                republic_date = d.strftime("%d")
                print(republic_date)
                if today_date == republic_date and today_month == republic_month:
                    template = self.env.ref(
                        "electronic_management.Republic_Day_Mail_Template"
                    )
                    template.send_mail(customer.id)

    """used for checking new year for Cronjob"""

    def check_new_year(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        customers = self.env["res.partner"].search([])
        for customer in customers:
            print(customer.name)
            if customer.email:
                d = datetime.date(2023, 1, 1)
                ny_month = d.strftime("%m")
                ny_date = d.strftime("%d")
                print(ny_date)
                if today_date == ny_date and today_month == ny_month:
                    template = self.env.ref(
                        "electronic_management.New_Year_Mail_Template"
                    )
                    template.send_mail(customer.id)

    """Used for checking for halloween day for Cronjob"""

    def check_halloween_day(self):
        today = fields.Date.today()
        today_month = today.strftime("%m")
        today_date = today.strftime("%d")
        customers = self.env["res.partner"].search([])
        for customer in customers:
            print(customer.name)
            if customer.email:
                d = datetime.date(2023, 10, 31)
                hallowen_month = d.strftime("%m")
                hallowen_date = d.strftime("%d")
                print(hallowen_date)
                if today_date == hallowen_date and today_month == hallowen_month:
                    template = self.env.ref(
                        "electronic_management.Halloween_Day_Mail_Template"
                    )
                    template.send_mail(customer.id)
