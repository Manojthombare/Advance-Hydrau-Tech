from odoo import api, fields, models, _

class WarrantyReport(models.Model):
    _name = "warranty.report"
    _description = "Warranty Report Form"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_of_company'

    name_of_company = fields.Many2one('res.partner', string='Company Name', required=True, tracking=True)
    complaint_no = fields.Char(string='Complaint No.', readonly=True, default=lambda self: _('New'))
    date = fields.Date(string='Date')
    representative_name = fields.Char(string='Representative Name', tracking=True)
    model_no = fields.Char(string="1. Model No.")
    date_of_dispatch = fields.Date(string='2. Date of dispatch')
    date_of_installation = fields.Date(string='3. Date of installation')
    expiry_of_warranty = fields.Date(string='4. Expiry of Warranty')
    date_of_arrival = fields.Date(string='5. Date of Arrival')
    date_of_departure = fields.Date(string='6. Date of Departure')
    no_of_days_worked = fields.Char(string='7. Number of Days worked')
    nature_of_problem = fields.Text(string='8. Nature of Problem')
    work_done = fields.Text(string='9. Work Done')
    details_of_spare_part = fields.Text(string='10. Details of spare part')
    machine_status = fields.Text(string='11. Machine Commissioned/Repair & Working Satisfactory')
    sign_service_engineer = fields.Char(string='Sign of Service Engineer')
    stamp_sign_party = fields.Char(string="Stamp and Sign of party")

    @api.model
    def create(self, vals):
        if vals.get('complaint_no', _('New')) == _('New'):
            vals['complaint_no'] = self.env['ir.sequence'].next_by_code('warranty.report.sequence') or _('New')
        return super(WarrantyReport, self).create(vals)
