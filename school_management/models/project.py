from odoo import models, fields


class Project(models.Model):
    _inherit = "project.project"

    pro_des = fields.Char(string="Description from SaleOrder")


class Task(models.Model):
    _inherit = "project.task"

    task_des = fields.Char(string="Task Description")
