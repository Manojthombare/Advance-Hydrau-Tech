from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class Deal(models.Model):
    _name = 'crm.deal'
    _description = 'CRM Deal'

    deal_id = fields.Char(string='Deal Id')
    name = fields.Char(string='Name')
    amount = fields.Float(string='Amount')
    base_currency_amount = fields.Float(string='Base Currency Amount')
    expected_close = fields.Char(string='Expected Close')
    closed_date = fields.Char(string='Closed Char')
    stage_updated_time = fields.Char(string='Stage Updated Time')
    probability = fields.Float(string='Probability')
    updated_at = fields.Char(string='Updated At')
    created_at = fields.Char(string='Created At')
    deal_pipeline_id = fields.Char(string='Deal Pipeline ID')
    deal_stage_id = fields.Char(string='Deal Stage ID')
    age = fields.Char(string='Age')
    last_assigned_at = fields.Char(string='Last Assigned At')
    last_contacted_sales_activity_mode = fields.Char(string='Last Contacted Sales Activity Mode')
    last_contacted_via_sales_activity = fields.Char(string='Last Contacted Via Sales Activity')
    expected_deal_value = fields.Float(string='Expected Deal Value')
    is_deleted = fields.Boolean(string='Is Deleted')
    partial = fields.Boolean(string='Is Partial')
    rotten_days = fields.Char(string='Rotten Days')
    collaboration_id = fields.Many2one('crm.deal.collaboration', string='Collaboration')
    widget_collaboration_id = fields.Many2one('crm.deal.widget.collaboration', string='Widget Collaboration')
    custom_field_ids = fields.One2many('crm.deal.custom.field', 'deal_id', string='Custom Fields')

    # Define links field
    conversations_link = fields.Char(string='Conversations Link')
    document_associations_link = fields.Char(string='Document Associations Link')
    notes_link = fields.Char(string='Notes Link')
    tasks_link = fields.Char(string='Tasks Link')
    appointments_link = fields.Char(string='Appointments Link')


    cf_metal_scrap_caterogy = fields.Char(string='Referred By')
    cf_referred_by = fields.Char(string='Referred By')
    cf_scrap_type = fields.Char(string='Scrap Type')
    cf_metal_scrap_category = fields.Char(string='Metal Scrap Category')
    cf_please_specify_the_metal_type = fields.Char(string='Please Specify the Metal Type')
    cf_nonmetal_category = fields.Char(string='Nonmetal Category')
    cf_please_specify_the_nonmetal_type = fields.Char(string='Please Specify the Nonmetal Type')
    cf_both_type = fields.Char(string='Both Type')
    cf_requirement_type = fields.Char(string='Requirement Type')
    cf_probability = fields.Char(string='Probability')
    cf_asap = fields.Char(string='ASAP')
    cf_deal_collaborator = fields.Char(string='Deal Collaborator')
    cf_order_confirmation = fields.Boolean(string='Order Confirmation')
    cf_add_quotation = fields.Boolean(string='Add Quotation')
    cf_reason_for_lost_deal = fields.Char(string='Reason for Lost Deal')
    cf_drop_reasons = fields.Char(string='Drop Reasons')
    cf_please_specify_others_drop_reason = fields.Char(string='Please Specify Others Drop Reason')
    cf_date_of_dispatch = fields.Char(string='Char of Dispatch')
    cf_payment_type = fields.Char(string='Payment Type')
    cf_notes_of_deals = fields.Text(string='Notes of Deals')
    cf_deal_related_to = fields.Char(string='Deal Related To')
    cf_metal_scrap_caterogy = fields.Char()
    cf_related_clients_contacts_of_servicespares = fields.Char(string='Related Clients Contacts of Services/Spares')
    cf_related_clients_contacts_of_service = fields.Char(string='Related Clients Contacts of Service')
    cf_country_name = fields.Char(string='Country Name')
    cf_hsn_no = fields.Char(string='HSN No')
    cf_hsn = fields.Char(string='HSN')

    open_deals_amount = fields.Char()
    open_deals_count = fields.Char()
    won_deals_amount = fields.Char()
    won_deals_count = fields.Char()
    last_contacted = fields.Char()
    position = fields.Char()

    @api.model
    def fetch_deal_payment_status(self):
        base_url = 'https://advancehydrautech.myfreshworks.com/crm/sales/deals/view/402004721313'
        headers = {
            'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
            'Content-Type': 'application/json'
        }

        for page in range(1, 82):  # Fetch from page 1 to 80
            response = requests.get(f'{base_url}?page={page}&per_page=25', headers=headers)
            if response.status_code == 200:
                data = response.json()
                deals = data.get("deals", [])
                if not deals:
                    break
                for deal in deals:
                    existing_record = self.env['crm.deal'].search([('deal_id', '=', deal.get('id'))], limit=1)
                    vals = {
                        'name': deal.get('name'),
                        'deal_id': deal.get('id'),
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
                        'cf_referred_by': deal.get('custom_field').get('cf_referred_by'),
                        'cf_scrap_type': deal.get('custom_field').get('cf_scrap_type'),
                        'cf_metal_scrap_category': deal.get('custom_field').get('cf_metal_scrap_category'),
                        'cf_please_specify_the_metal_type': deal.get('custom_field').get(
                            'cf_please_specify_the_metal_type'),
                        'cf_nonmetal_category': deal.get('custom_field').get('cf_nonmetal_category'),
                        'cf_please_specify_the_nonmetal_type': deal.get('custom_field').get(
                            'cf_please_specify_the_nonmetal_type'),
                        'cf_both_type': deal.get('custom_field').get('cf_both_type'),
                        'cf_requirement_type': deal.get('custom_field').get('cf_requirement_type'),
                        'cf_probability': deal.get('custom_field').get('cf_probability'),
                        'cf_asap': deal.get('custom_field').get('cf_asap'),
                        'cf_deal_collaborator': deal.get('custom_field').get('cf_deal_collaborator'),
                        'cf_order_confirmation': deal.get('custom_field').get('cf_order_confirmation'),
                        'cf_add_quotation': deal.get('custom_field').get('cf_add_quotation'),
                        'cf_reason_for_lost_deal': deal.get('custom_field').get('cf_reason_for_lost_deal'),
                        'cf_drop_reasons': deal.get('custom_field').get('cf_drop_reasons'),
                        'cf_date_of_dispatch': deal.get('custom_field').get('cf_date_of_dispatch'),
                        'cf_payment_type': deal.get('custom_field').get('cf_payment_type'),
                        'cf_notes_of_deals': deal.get('custom_field').get('cf_notes_of_deals'),
                        'cf_deal_related_to': deal.get('custom_field').get('cf_deal_related_to'),
                        'cf_country_name': deal.get('custom_field').get('cf_country_name'),
                        'cf_hsn_no': deal.get('custom_field').get('cf_hsn_no'),
                        'cf_hsn': deal.get('custom_field').get('cf_hsn'),
                        'conversations_link': deal.get('links').get('conversations'),
                        'document_associations_link': deal.get('links').get('document_associations'),
                        'notes_link': deal.get('links').get('notes'),
                        'tasks_link': deal.get('links').get('tasks'),
                        'appointments_link': deal.get('links').get('appointments'),
                    }
                    if existing_record:
                        existing_record.write(vals)
                        print(f'---------deal id {deal.get("id")} Updated =======')
                    else:
                        self.env['crm.deal'].create(vals)
                        print(f'---------deal id {deal.get("id")} Created =======')
            else:
                _logger.error("Failed to retrieve data for page %s, status code: %s, message: %s", page,
                              response.status_code, response.text)
                break
    # @api.model
    # def fetch_deal_payment_status(self):
    #     filter_url = 'https://advancehydrautech.myfreshworks.com/crm/sales/api/deals/filters'
    #     headers = {
    #         'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
    #         'Content-Type': 'application/json'
    #     }
    #     filter_response = requests.get(filter_url, headers=headers)
    #     if filter_response.status_code == 200:
    #         filter_data = filter_response.json()
    #         view_ids = [filter_item['id'] for filter_item in filter_data.get('filters', [])]
    #         print('--------view_ids-------', view_ids)
    #         for view_id in view_ids:
    #             url = f'https://advancehydrautech.myfreshworks.com/crm/sales/api/deals/view/{view_id}'
    #             # url = f'https://advancehydrautech.myfreshworks.com/crm/sales/api/deals/view/{view_id}?include=owner,sales_activities,creater,updater,source,contacts,sales_account,deal_stage,deal_type,deal_reason,campaign,deal_payment_status,deal_product,currency'
    #             headers = {
    #                 'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
    #                 'Content-Type': 'application/json'
    #             }
    #             response = requests.get(url, headers=headers)
    #             if response.status_code == 200:
    #                 _logger.info("API call successful")
    #                 data = response.json()
    #                 print('======Deal data=====view_id==\n\n\n======',view_id, len(data.get("deals")))
    #                 # if data.get("sales_accounts"):
    #                 #     for deal in data.get("sales_accounts"):
    #                 #         existing_record = self.search([('deal_id', '=', deal.get('id'))], limit=1)
    #                 #         vals = {
    #                 #             'name': deal.get('name'),
    #                 #             'partial': deal.get('partial') if deal.get('partial') else False,
    #                 #             'deal_id': deal.get('id'),
    #                 #             "open_deals_amount": deal.get('open_deals_amount'),
    #                 #             "open_deals_count": deal.get('open_deals_count'),
    #                 #             "won_deals_amount": deal.get('won_deals_amount'),
    #                 #             "won_deals_count": deal.get('won_deals_count'),
    #                 #             "last_contacted": deal.get('last_contacted'),
    #                 #         }
    #                 #         if existing_record:
    #                 #             existing_record.write(vals)
    #                 #         else:
    #                 #             self.create(vals)
    #                 # if data.get("lead_sources"):
    #                 #     for deal in data.get("lead_sources"):
    #                 #         existing_record = self.search([('deal_id', '=', deal.get('id'))], limit=1)
    #                 #         vals = {
    #                 #             'name': deal.get('name'),
    #                 #             'partial': deal.get('partial') if deal.get('partial') else False,
    #                 #             'deal_id': deal.get('id'),
    #                 #             "position": deal.get('position'),
    #                 #         }
    #                 #         if existing_record:
    #                 #             existing_record.write(vals)
    #                 #         else:
    #                 #             self.create(vals)
    #                 for deal in data.get("deals"):
    #                     existing_record = self.search([('deal_id', '=', deal.get('id'))], limit=1)
    #                     vals = {
    #                         'name': deal.get('name'),
    #                         # 'partial': deal.get('partial') if deal.get('partial') else False,
    #                         'deal_id': deal.get('id'),
    #                         'amount': deal.get('amount'),
    #                         'base_currency_amount': deal.get('base_currency_amount'),
    #                         'expected_close': deal.get('expected_close'),
    #                         'closed_date': deal.get('closed_date'),
    #                         'stage_updated_time': deal.get('stage_updated_time'),
    #                         'probability': deal.get('probability'),
    #                         'updated_at': deal.get('updated_at'),
    #                         'created_at': deal.get('created_at'),
    #                         'deal_pipeline_id': deal.get('deal_pipeline_id'),
    #                         'deal_stage_id': deal.get('deal_stage_id'),
    #                         'age': deal.get('age'),
    #                         'expected_deal_value': deal.get('expected_deal_value'),
    #                         'is_deleted': deal.get('is_deleted'),
    #                         'rotten_days': deal.get('rotten_days'),
    #                         'cf_referred_by': deal.get('custom_field').get('cf_referred_by'),
    #                         'cf_scrap_type': deal.get('custom_field').get('cf_scrap_type'),
    #                         'cf_metal_scrap_category': deal.get('custom_field').get('cf_metal_scrap_category'),
    #                         'cf_please_specify_the_metal_type': deal.get('custom_field').get(
    #                             'cf_please_specify_the_metal_type'),
    #                         'cf_nonmetal_category': deal.get('custom_field').get('cf_nonmetal_category'),
    #                         'cf_please_specify_the_nonmetal_type': deal.get('custom_field').get(
    #                             'cf_please_specify_the_nonmetal_type'),
    #                         'cf_both_type': deal.get('custom_field').get('cf_both_type'),
    #                         'cf_requirement_type': deal.get('custom_field').get('cf_requirement_type'),
    #                         'cf_probability': deal.get('custom_field').get('cf_probability'),
    #                         'cf_asap': deal.get('custom_field').get('cf_asap'),
    #                         'cf_deal_collaborator': deal.get('custom_field').get('cf_deal_collaborator'),
    #                         'cf_order_confirmation': deal.get('custom_field').get('cf_order_confirmation'),
    #                         'cf_add_quotation': deal.get('custom_field').get('cf_add_quotation'),
    #                         'cf_reason_for_lost_deal': deal.get('custom_field').get('cf_reason_for_lost_deal'),
    #                         'cf_drop_reasons': deal.get('custom_field').get('cf_drop_reasons'),
    #                         'cf_date_of_dispatch': deal.get('custom_field').get('cf_date_of_dispatch'),
    #                         'cf_payment_type': deal.get('custom_field').get('cf_payment_type'),
    #                         'cf_notes_of_deals': deal.get('custom_field').get('cf_notes_of_deals'),
    #                         'cf_deal_related_to': deal.get('custom_field').get('cf_deal_related_to'),
    #                         'cf_country_name': deal.get('custom_field').get('cf_country_name'),
    #                         'cf_hsn_no': deal.get('custom_field').get('cf_hsn_no'),
    #                         'cf_hsn': deal.get('custom_field').get('cf_hsn'),
    #                         'conversations_link': deal.get('links').get('conversations'),
    #                         'document_associations_link': deal.get('links').get('document_associations'),
    #                         'notes_link': deal.get('links').get('notes'),
    #                         'tasks_link': deal.get('links').get('tasks'),
    #                         'appointments_link': deal.get('links').get('appointments'),
    #                     }
    #                     if existing_record:
    #                         existing_record.write(vals)
    #                     else:
    #                         self.create(vals)
    #             else:
    #                 _logger.error("Failed to retrieve data, status code: %s", response.status_code)
    #     else:
    #         _logger.error("Failed to retrieve data, status code: %s", filter_response.status_code)


class DealCustomField(models.Model):
    _name = 'crm.deal.custom.field'
    _description = 'CRM Deal Custom Field'

    deal_id = fields.Many2one('crm.deal', string='Deal', ondelete='cascade', required=True)
    cf_referred_by = fields.Char(string='Referred By')
    cf_scrap_type = fields.Char(string='Scrap Type')
    cf_metal_scrap_category = fields.Char(string='Metal Scrap Category')
    cf_please_specify_the_metal_type = fields.Char(string='Please Specify the Metal Type')
    cf_nonmetal_category = fields.Char(string='Nonmetal Category')
    cf_please_specify_the_nonmetal_type = fields.Char(string='Please Specify the Nonmetal Type')
    cf_both_type = fields.Char(string='Both Type')
    cf_requirement_type = fields.Char(string='Requirement Type')
    cf_probability = fields.Char(string='Probability')
    cf_asap = fields.Char(string='ASAP')
    cf_deal_collaborator = fields.Many2one('res.partner', string='Deal Collaborator')
    cf_order_confirmation = fields.Boolean(string='Order Confirmation')
    cf_add_quotation = fields.Boolean(string='Add Quotation')
    cf_reason_for_lost_deal = fields.Char(string='Reason for Lost Deal')
    cf_drop_reasons = fields.Char(string='Drop Reasons')
    cf_please_specify_others_drop_reason = fields.Char(string='Please Specify Others Drop Reason')
    cf_date_of_dispatch = fields.Char(string='Char of Dispatch')
    cf_payment_type = fields.Char(string='Payment Type')
    cf_notes_of_deals = fields.Text(string='Notes of Deals')
    cf_deal_related_to = fields.Char(string='Deal Related To')
    cf_related_clients_contacts_of_servicespares = fields.Char(string='Related Clients Contacts of Services/Spares')
    cf_related_clients_contacts_of_service = fields.Many2one('res.partner', string='Related Clients Contacts of Service')
    cf_country_name = fields.Char(string='Country Name')
    cf_hsn_no = fields.Char(string='HSN No')
    cf_hsn = fields.Char(string='HSN')
    cf_metal_scrap_caterogy = fields.Char()

class DealCollaboration(models.Model):
    _name = 'crm.deal.collaboration'
    _description = 'CRM Deal Collaboration'

    deal_id = fields.Many2one('crm.deal', string='Deal', ondelete='cascade', required=True)
    # Add fields as needed for collaboration details

class DealWidgetCollaboration(models.Model):
    _name = 'crm.deal.widget.collaboration'
    _description = 'CRM Deal Widget Collaboration'

    deal_id = fields.Many2one('crm.deal', string='Deal', ondelete='cascade', required=True)
    convo_token = fields.Char(string='Conversation Token')
    auth_token = fields.Char(string='Auth Token')
    encoded_jwt_token = fields.Char(string='Encoded JWT Token')
