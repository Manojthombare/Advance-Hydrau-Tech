from odoo import api, fields, models
from datetime import datetime


class DatewiseInstallationRecords(models.TransientModel):
    _name = 'installation.records'
    _description = 'Installation Records'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    installations_id = fields.Many2many('installation.report', string='Resultant Installations List')

    def fetch_records_between_dates(self):
        start_date = datetime.combine(self.from_date, datetime.min.time()).date()
        end_date = datetime.combine(self.to_date, datetime.max.time()).date()
        domain = [('installation_date', '>=', start_date),
                  ('installation_date', '<=', end_date)]

        return {
            'type': 'ir.actions.act_window',
            'name': 'Installation details',
            'res_model': 'installation.report',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'new',
        }
        
    def print_filter_records(self):
        start_date = datetime.combine(self.from_date, datetime.min.time()).date()
        end_date = datetime.combine(self.to_date, datetime.max.time()).date()
        domain = [('installation_date', '>=', start_date),
                  ('installation_date', '<=', end_date)]

        installations = self.env['installation.report'].search(domain)
    
        data = {        
            'docs': installations,
        }
        
        # Get the report template from the XML ID 'dw_sales_inherit.print_installation_report_qweb_report_id'
        template = self.env.ref('dw_sales_inherit.print_installation_report_qweb_report_id')
        print(installations)
        #return template.report_action(self.env['installation.report'].search(domain))
        #return template.report_action(self, data=data)
        return template.report_action(installations)
        # return self.env['ir.actions.report'].report_action(records, 'dw_sales_inherit.print_installation_report_qweb_report_id')
         






'''
  template = self.env.ref('dw_sales_inherit.report_installation_document_id')
        return self.env['ir.actions.report'].report_action(records, 'dw_sales_inherit.report_installation_document')
'''
    