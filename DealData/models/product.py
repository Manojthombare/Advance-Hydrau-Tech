import requests
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.template'

    freshworks_id = fields.Char('Freshworks ID')
    category = fields.Char('Category')
    cf_subcategory_of_spares = fields.Char('Subcategory of Spares')
    cf_weight_in_tons = fields.Float('Weight in Tons')
    cf_uom = fields.Char('UOM')
    # cf_hsn_no = fields.Char('HSN No')
    cf_file_no = fields.Char('File No')
    product_code = fields.Char('Product Code')
    sku_number = fields.Char('SKU Number')
    parent_product = fields.Char('Parent Product')
    territory_id = fields.Char('Territory ID')
    valid_till = fields.Date('Valid Till')
    is_active = fields.Boolean('Is Active')
    owner_id = fields.Char('Owner ID')
    is_deleted = fields.Boolean('Is Deleted')
    created_at = fields.Char('Created At')
    updated_at = fields.Char('Updated At')
    pricing_type = fields.Integer('Pricing Type')
    product_pricings = fields.Text('Product Pricings')
    avatar = fields.Char('Avatar')
    # base_currency_amount = fields.Float('Base Currency Amount')
    creater_id = fields.Char('Creator ID')
    updater_id = fields.Char('Updater ID')
    description = fields.Text('Description')
    external_source_id = fields.Char('External Source ID')
    is_fresh = fields.Boolean()

    @api.model
    def fetch_all_products(self):
        base_url = 'https://advancehydrautech.myfreshworks.com/crm/sales/api/cpq/products/'
        headers = {
            'Authorization': 'Token token=IQfwrun6IMHcuOpj67YAQQ',
            'Content-Type': 'application/json'
        }
        for page in range(1, 82):  # Fetch from page 1 to 80
            response = requests.get(f'{base_url}?page={page}&per_page=25&include=product_pricings', headers=headers)
            if response.status_code == 200:
                data = response.json()
                print('\n\n\n----------data----------', data)
                products = data.get('products', [])
                print('\n\n\n\n----------products----------', products)
                if not products:
                    break
                for product in products:
                    existing_product = self.search([('freshworks_id', '=', product.get('id'))], limit=1)
                    custom_fields = product.get('custom_field', {})
                    vals = {
                        'is_fresh': True,
                        'name': product.get('name'),
                        'list_price' : product.get('base_currency_amount'),
                        'freshworks_id': product.get('id'),
                        'category': product.get('category'),
                        'cf_subcategory_of_spares': custom_fields.get('cf_subcategory_of_spares'),
                        'cf_weight_in_tons': custom_fields.get('cf_weight_in_tons'),
                        'cf_uom': custom_fields.get('cf_uom'),
                        'l10n_in_hsn_code': custom_fields.get('cf_hsn_no'),
                        'cf_file_no': custom_fields.get('cf_file_no'),
                        'product_code': product.get('product_code'),
                        'sku_number': product.get('sku_number'),
                        'parent_product': product.get('parent_product'),
                        'territory_id': product.get('territory_id'),
                        'valid_till': product.get('valid_till'),
                        'is_active': product.get('is_active'),
                        'owner_id': product.get('owner_id'),
                        'is_deleted': product.get('is_deleted'),
                        'created_at': product.get('created_at'),
                        'updated_at': product.get('updated_at'),
                        'pricing_type': product.get('pricing_type'),
                        'product_pricings': str(product.get('product_pricings')),  # Convert list to string
                        'avatar': product.get('avatar'),
                        # 'base_currency_amount': product.get('base_currency_amount'),
                        'creater_id': product.get('creater_id'),
                        'updater_id': product.get('updater_id'),
                        'description': product.get('description'),
                        'external_source_id': product.get('external_source_id'),
                    }
                    print('=========vals=======', vals)
                    if existing_product:
                        existing_product.write(vals)
                    else:
                        self.create(vals)
            else:
                _logger.error("Failed to retrieve data for page %s, status code: %s, message: %s", page,
                              response.status_code, response.text)
                break
