from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class DealWizard(models.TransientModel):
    _name = 'deal.wizard'
    _description = 'Deal Wizard'

    deal_id = fields.Char(string='Deal ID', required=True)

    def fetch_deal_based_on_id(self):
        deal_id = int(self.deal_id)
        print('\n\n\n\n\n================deal_id=========', deal_id, type(deal_id))
        # url = 'https://advancehydrautech.myfreshworks.com/crm/sales/deals/402001266362'
        url = f'https://advancehydrautech.myfreshworks.com/crm/sales/deals/{deal_id}'
        print('-----------url-----------\n\n\n', url)
        headers = {
            'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("API call successful")
            data = response.json()
            deal = data.get("deal")
            if deal:
                existing_record = self.env['crm.deal'].search([('name', '=', deal.get('name'))], limit=1)
                vals = {
                    'name': deal.get('name'),
                    'amount': deal.get('amount'),
                    'base_currency_amount': deal.get('base_currency_amount'),
                    'expected_close': deal.get('expected_close'),
                    'closed_date': deal.get('closed_date'),
                    'stage_updated_time': deal.get('stage_updated_time'),
                    'probability': deal.get('probability'),
                    'updated_at': deal.get('updated_at'),
                    'created_at': deal.get('created_at'),
                    'deal_pipeline_id': deal.get('deal_pipeline_id'),
                    'deal_stage_id': deal.get('deal_stage_id'),
                    'age': deal.get('age'),
                    'expected_deal_value': deal.get('expected_deal_value'),
                    'is_deleted': deal.get('is_deleted'),
                    'rotten_days': deal.get('rotten_days'),
                    'cf_referred_by': deal.get('custom_field', {}).get('cf_referred_by'),
                    'cf_scrap_type': deal.get('custom_field', {}).get('cf_scrap_type'),
                    'cf_metal_scrap_category': deal.get('custom_field', {}).get('cf_metal_scrap_category'),
                    'cf_please_specify_the_metal_type': deal.get('custom_field', {}).get('cf_please_specify_the_metal_type'),
                    'cf_nonmetal_category': deal.get('custom_field', {}).get('cf_nonmetal_category'),
                    'cf_please_specify_the_nonmetal_type': deal.get('custom_field', {}).get('cf_please_specify_the_nonmetal_type'),
                    'cf_both_type': deal.get('custom_field', {}).get('cf_both_type'),
                    'cf_requirement_type': deal.get('custom_field', {}).get('cf_requirement_type'),
                    'cf_probability': deal.get('custom_field', {}).get('cf_probability'),
                    'cf_asap': deal.get('custom_field', {}).get('cf_asap'),
                    'cf_deal_collaborator': deal.get('custom_field', {}).get('cf_deal_collaborator'),
                    'cf_order_confirmation': deal.get('custom_field', {}).get('cf_order_confirmation'),
                    'cf_add_quotation': deal.get('custom_field', {}).get('cf_add_quotation'),
                    'cf_reason_for_lost_deal': deal.get('custom_field', {}).get('cf_reason_for_lost_deal'),
                    'cf_drop_reasons': deal.get('custom_field', {}).get('cf_drop_reasons'),
                    'cf_date_of_dispatch': deal.get('custom_field', {}).get('cf_date_of_dispatch'),
                    'cf_payment_type': deal.get('custom_field', {}).get('cf_payment_type'),
                    'cf_notes_of_deals': deal.get('custom_field', {}).get('cf_notes_of_deals'),
                    'cf_deal_related_to': deal.get('custom_field', {}).get('cf_deal_related_to'),
                    'cf_country_name': deal.get('custom_field', {}).get('cf_country_name'),
                    'cf_hsn_no': deal.get('custom_field', {}).get('cf_hsn_no'),
                    'cf_hsn': deal.get('custom_field', {}).get('cf_hsn'),
                    'conversations_link': deal.get('links', {}).get('conversations'),
                    'document_associations_link': deal.get('links', {}).get('document_associations'),
                    'notes_link': deal.get('links', {}).get('notes'),
                    'tasks_link': deal.get('links', {}).get('tasks'),
                    'appointments_link': deal.get('links', {}).get('appointments'),
                }
                if existing_record:
                    existing_record.write(vals)
                    record_id = existing_record.id
                else:
                    new_record = self.env['crm.deal'].create(vals)
                    record_id = new_record.id
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Deal Data',
                    'res_model': 'crm.deal',
                    'view_mode': 'form',
                    'res_id': record_id,
                    'target': 'current',
                }
        else:
            _logger.error("Failed to retrieve data, status code: %s", response.status_code)
