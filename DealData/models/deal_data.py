from odoo import models, fields, api, _
import requests
import logging

_logger = logging.getLogger(__name__)


class DealData(models.Model):
    _name = 'deal.data'
    _description = 'Deal Data'

    name = fields.Char(string='Name')
    model_class_name = fields.Char(string='Model Class Name')
    user_id = fields.Char(string='User ID')
    is_default = fields.Boolean(string='Is Default')
    updated_at = fields.Char(string='Updated At')
    user_name = fields.Char(string='User Name')
    current_user_permissions = fields.Char(string='Current User Permissions')

    @api.model
    def fetch_deal(self):
        url = 'https://advancehydrautech.myfreshworks.com/crm/sales/api/deals/filters'
        headers = {
            'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            _logger.info("API call successful")
            data = response.json()
            # print('--------data-----\n\n\n', data)
            # print('--------fillterrrt-----\n\n\n', data.get('filters'))

            _logger.info("Fetched data: %s", data)

            # Assuming 'data' contains a list of deals
            for deal in data.get('filters'):
                print('--------deal-----\n\n\n', deal)
                existing_record = self.search([('name', '=', deal.get('name'))], limit=1)

                if not existing_record:
                    vals = {
                        'name': deal.get('name'),
                        'model_class_name': deal.get('model_class_name'),
                        # 'user': deal.get('user_id'),
                        'is_default': deal.get('is_default'),
                        'updated_at': deal.get('updated_at'),
                        'user_name': deal.get('user_name'),
                        'current_user_permissions': ', '.join(deal.get('current_user_permissions', [])),
                    }
                    print('---vals=========', vals)
                    self.create(vals)
        else:
            _logger.error("Failed to retrieve data, status code: %s", response.status_code)


class DealSettingFields(models.Model):
    _name = 'deal.setting.fields'
    _description = 'Deal Setting Fields'

    label = fields.Char(string='Label')
    name = fields.Char(string='Name')
    type = fields.Char()
    default = fields.Boolean(string='Default')
    actionable = fields.Boolean(string='Actionable')
    position = fields.Integer(string='Position')
    base_model = fields.Char(string='Base Model')
    required = fields.Boolean(string='Required')
    quick_add_position = fields.Integer(string='Quick Add Position')
    visible = fields.Boolean(string='Visible')
    choices_ids = fields.One2many('deal.payment.status.choice', 'deal_payment_status_id', string='Choices')

    def create_initial_data(self):
        # Create the deal payment status
        deal_payment_status = self.create({
            'label': 'Payment status',
            'name': 'deal_payment_status_id',
            'type': 'dropdown',
            'default': True,
            'actionable': True,
            'position': 11,
            'base_model': 'Deal',
            'required': False,
            'quick_add_position': 68,
            'visible': False,
        })

        # Create the choices
        choices = [
            {
                'deal_payment_status_id': deal_payment_status.id,
                'value': 'Telegraphic Transfer (TT)',
                'position': 1
            },
            {
                'deal_payment_status_id': deal_payment_status.id,
                'value': 'Letter of Credit (LC)',
                'position': 2
            }
        ]

        for choice in choices:
            self.env['deal.payment.status.choice'].create(choice)

    @api.model
    def fetch_deal_payment_status(self):
        url = 'https://advancehydrautech.myfreshworks.com/crm/sales/api/settings/deals/fields'
        headers = {
            'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            _logger.info("API call successful")
            data = response.json()
            _logger.info("Fetched data: %s", data)

            # Assuming 'data' contains a list of fields
            for field in data.get('fields', []):
                existing_record = self.search([('name', '=', field.get('name'))], limit=1)

                if not existing_record:
                    vals = {
                        'label': field.get('label'),
                        'name': field.get('name'),
                        'type': field.get('type'),
                        'default': field.get('default'),
                        'actionable': field.get('actionable'),
                        'position': field.get('position'),
                        'base_model': field.get('base_model'),
                        'required': field.get('required'),
                        'quick_add_position': field.get('quick_add_position'),
                        'visible': field.get('visible'),
                        'choices_ids': [(0, 0, {
                            'value': choice.get('value'),
                            'position': choice.get('position')
                        }) for choice in field.get('choices', [])]
                    }
                    self.create(vals)
        else:
            _logger.error("Failed to retrieve data, status code: %s", response.status_code)


class DealPaymentStatusChoice(models.Model):
    _name = 'deal.payment.status.choice'
    _description = 'Deal Payment Status Choice'

    deal_payment_status_id = fields.Many2one('deal.setting.fields', string='Deal Payment Status', ondelete='cascade', required=True)
    value = fields.Char(string='Value', required=True)
    position = fields.Integer(string='Position')
