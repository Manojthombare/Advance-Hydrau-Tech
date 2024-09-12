from odoo import models, fields, api, _



class InheritPartner(models.Model):
   _inherit = 'res.partner'
   _description = "Inherit res partner form view & add new fields"
   
   #pan_no = fields.Char(string="PAN No")
  