from odoo import models, fields, api, _



class InheritCompany(models.Model):
   _inherit = 'res.company'
   _description = "Inherit res company form view & add new fields"
   
   #pan_no = fields.Char(string="PAN No")
   
