from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    crm_account_id = fields.Char(string='CRM Account ID')
    sales_account_id = fields.Char(string='Sales Account ID')
    industry = fields.Char()
    created_at = fields.Char()
    owner_id = fields.Char()
    address = fields.Char()
    updated_at = fields.Char(string='Industry')
    annual_revenue = fields.Float(string='Annual Revenue')
    employees_count = fields.Integer(string='Employees Count')
    tags = fields.Char(string='Tags')
    is_fresh = fields.Boolean()

    @api.model
    def fetch_all_accounts(self):
        base_url = 'https://advancehydrautech.myfreshworks.com/crm/sales/api/sales_accounts/view//402003374765'
        # base_url = 'https://advancehydrautech.myfreshworks.com/crm/sales/api/accounts/view/402003374765'
        headers = {
            'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
            'Content-Type': 'application/json'
        }

        for page in range(1, 82):  # Fetch from page 1 to 80
            response = requests.get(f'{base_url}?page={page}&per_page=25', headers=headers)
            if response.status_code == 200:
                data = response.json()
                # print('-----fetch_all_accounts----data--------', data)
                accounts = data.get("sales_accounts", [])
                if not accounts:
                    break
                for account in accounts:
                    print('\n\n\n---------account--------', account)
                    country_name = account['custom_field'].get('cf_country_')  # This might be 'India'
                    state_name = account['custom_field'].get('cf_states')  # This might be 'Telangana'

                    # Search for the country in the 'res.country' model
                    if country_name:
                        country = self.env['res.country'].search([('name', '=', country_name)], limit=1)
                        if country:
                            account['country_id'] = country.id  # Use the ID for the many2one field
                        else:
                            account['country_id'] = None  # Handle case where country is not found
                    else:
                        account['country_id'] = None  # If country name is not provided

                    # Search for the state in the 'res.country.state' model
                    if state_name:
                        state = self.env['res.country.state'].search([('name', '=', state_name)], limit=1)
                        if state:
                            account['state_id'] = state.id  # Use the ID for the many2one field
                        else:
                            account['state_id'] = None  # Handle case where state is not found
                    else:
                        account['state_id'] = None  # If state name is not provided

                    vals = {
                        'name': account.get('name'),
                        'is_fresh': True,
                        'crm_account_id': account.get('id'),
                        'sales_account_id': account.get('sales_account_id'),
                        'email': account['custom_field'].get('cf_email'),
                        'phone': account.get('phone') ,
                        'street': account.get('address'),
                        'city': account.get('city'),
                        'state_id': account['state_id'],  # Use the resolved state ID
                        'country_id': account['country_id'],  # Use the resolved country ID
                        'zip': account.get('zipcode'),
                        'vat': account['custom_field'].get('cf_gst_no'),
                        'website': account.get('website'),
                        'industry': account.get('industry'),
                        'annual_revenue': account.get('annual_revenue'),
                        'employees_count': account.get('employees_count'),
                        'category_id': account.get('tags'),
                    }
                    print('\n\n\n----------vals----------', vals)
                    existing_record = self.env['res.partner'].search([('crm_account_id', '=', account.get('id'))],
                                                                     limit=1)
                    print('-------existing_record------', existing_record)
                    if existing_record:
                        print('------Updated Contact Records---------', existing_record)
                        existing_record.write(vals)
                        _logger.info(f'Account ID {account.get("id")} updated.')
                    else:
                        s = self.env['res.partner'].create(vals)
                        print('------created Contact Records---------', s)
                        _logger.info(f'Account ID {account.get("id")} created.')
            else:
                _logger.error("Failed to retrieve data for page %s, status code: %s, message: %s", page, response.status_code, response)
                break
