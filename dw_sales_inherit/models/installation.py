from odoo import api, fields, models, _

class InstallationReport(models.Model):
    _name = "installation.report"
    _description = "Installation Report Form"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'company_name'
    
    company_name = fields.Many2one('res.partner', string='Company Name', required=True, tracking=True)
    complaint_no = fields.Char(string='Complaint No.',readonly=True, default=lambda self: _('New'))
    installation_date = fields.Date(string='Date')
    engineer_name = fields.Char(string='Engineer Name', tracking=True)
    machine_no = fields.Char(string='Machine No.', tracking=True)
    no_of_leakage_1 = fields.Char(string='1.', tracking=True)
    no_of_leakage_2 = fields.Char(string='2', tracking=True)
    no_of_leakage_3 = fields.Char(string='3.' ,tracking=True)
    missing_part_1 = fields.Char(string='1.', tracking=True)
    missing_part_2 = fields.Char(string='2.', tracking=True)
    missing_part_3 = fields.Char(string='3.', tracking=True)
    welding_problem_in_machine_1 = fields.Char(string='1.', tracking=True)
    welding_problem_in_machine_2 = fields.Char(string='2.', tracking=True)
    welding_problem_in_machine_3 = fields.Char(string='3.', tracking=True)
    problem_in_machine_1 = fields.Char(string='1.', tracking=True)
    problem_in_machine_2 = fields.Char(string='2.', tracking=True)
    problem_in_machine_3 = fields.Char(string='3.', tracking=True)
    nut_bolt_checked = fields.Boolean(string='Nut bolt of machine')
    wire_checked = fields.Boolean(string='Wire checked')
    hose_pipe_tightened = fields.Boolean(string='Hose pipe tightened')
    oil_checked = fields.Boolean(string='Oil checked')
    power_supply_checked = fields.Boolean(string='Power supply')
    machine_working_mode = fields.Selection([
        ('manual', 'Manual'),
        ('auto', 'Auto')
    ], string='Machine Working in Manual / Auto')
    party_signature = fields.Char(string="Party's Sign")
    service_engineer = fields.Char(string='Service Engineer')
    
    # Page 2 form
    scrap_type = fields.Text(string='Type of Scrap Used by Customer')
    bales_made = fields.Integer(string='No of Bales Made by Customer')
    training_given_to = fields.Char(string='Training & Maintenance Tips Given To')
    trainee_name = fields.Char(string='Trainee Name')
    trainee_designation = fields.Char(string='Trainee Designation')

    @api.model
    def create(self, vals):
        if vals.get('complaint_no', _('New')) == _('New'):
            vals['complaint_no'] = self.env['ir.sequence'].next_by_code('installation.report.sequence') or _('New')
        return super(InstallationReport, self).create(vals)
