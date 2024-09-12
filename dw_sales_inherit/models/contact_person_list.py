from odoo import api, fields, models

class ContactPerson(models.Model):
    _name = "contact.person"
    _description = "Details of Contact Persons"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name of Person', tracking=True)
    company_name = fields.Many2one('res.partner' , string='Company Name' , tracking=True)
    person_number = fields.Char(string='Mobile number', track_visibility='always')
    person_email = fields.Char(string='Email Address',tracking=True)