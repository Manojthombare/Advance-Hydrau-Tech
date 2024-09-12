from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, ValidationError, UserError
from datetime import datetime, time, date, timedelta
import json
from num2words import num2words
from odoo.tools.date_utils import get_month, get_fiscal_year
from odoo.tools.misc import format_date

import re
from collections import defaultdict

class ResPartner(models.Model):
    _inherit = "res.partner"
    property_account_payable_id = fields.Many2one(required=False)
    property_account_receivable_id = fields.Many2one(required=False)

# class ProductProduct(models.Model):
#     _inherit = "product.product"

#     description = fields.Html()
    

class SaleOrderInherit(models.Model):
   _inherit = 'sale.order'
   _description = "Inherit sale sales order form view & add new fields"
   
   consignee_name = fields.Many2one('res.partner' ,string="Ship To")
   
   po_ref = fields.Char(string="PO Reference")
   compalint_no = fields.Char(string="Complaint Number")
   advance_bal = fields.Float(string="Advance Amount")
   packing_id = fields.Float(string="Packing Charges")
   fret = fields.Float(string="Freight")
   stamp = fields.Binary(string='Stamp')
   signature = fields.Binary(string='Signature')
   dispatch_message = fields.Text(string="Dispatch Message", default="""Sir, your machine will be ready for dispatch 2 - 3 days and request you to release the payment as the
    earliest.""")
   proforma_invoice_number = fields.Char(string='Proforma Invoice Number', readonly=True, copy=False)
   
         
   @api.model
   def create(self, vals):
      if not vals.get('proforma_invoice_number'):
            company = self.env.company
            if company.id == 1:
                sequence_code = 'sale.order.proforma.invoice.company1'
            elif company.id == 2:
                sequence_code = 'sale.order.proforma.invoice.company2'
            else:
                sequence_code = 'sale.order.proforma.invoice'
            vals['proforma_invoice_number'] = self.env['ir.sequence'].next_by_code(sequence_code) or '/'
      return super(SaleOrderInherit, self).create(vals)

   note = fields.Html(string='Note' , default="""
    <style>
        .terms-table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        .terms-row {
            display: grid;
            grid-template-columns: auto auto auto;
            gap: 10px; /* Space between columns */
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        .terms-number {
            text-align: left;
            
        .terms-colon {
            text-align: center;
           
        }
        .terms-description {
            text-align: right;
           
        }
    </style>
    <table class="terms-table">
        <tr class="terms-row">
            <td class="terms-number">1. Price</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">The above prices are Ex. Our Works, Delhi.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">2. Payment</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">40% Advance, Balance against P.I.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">3. Delivery</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">100 - 120 Days, From the advance received date along with P.O.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">4. Machine Logistics</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">Buyer Scope.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">5. Machine Unloading</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">Buyer Scope.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">6. Hydraulic Oil</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">Buyer Scope.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">7. Insurance</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">Buyer Scope.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">8. GST</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">Extra as applicable. Presently @ 18%.</td>
        </tr>
        <tr class="terms-row">
            <td class="terms-number">9. Quotation Validity</td>
            <td class="terms-colon" style="padding-left: 10px;padding-right: 10px;">:</td>
            <td class="terms-description">7 Days, In view of unstable steel prices.</td>
        </tr>
    </table>
    """) 
   export_terms_condn =fields.Html(string="Export terms and Conditions", default="""
        <p><strong><u>OTHER TERMS & CONDITIONS</u></strong></p>
       <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="white-space: nowrap;">
                <strong>1. Delivery </strong>
            </td>
            <td >
                : &nbsp;Can be dispatched from New Delhi within 120-150 days from the date of receipt of confirmed order along with advance.
            </td>
        </tr>
        <tr>
            <td style="white-space: nowrap;">
                <strong>2. Payment  </strong>
            </td>
            <td >
                :&nbsp; 40% advance through T.T. and balance before dispatch.
                 (Note: Balance payment against scanned copy of Bill of Lading is subject to C&F order. Otherwise, payment must be made before dispatch).
            </td>
        </tr>
        <tr>
            <td style="white-space: nowrap;">
                <strong>3. Our Bank Detail: </strong>
            </td>
            <td >
                :&nbsp;BENEFICIARY NAME    : ADVANCE HYDRAU-TECH PVT. LTD.<br/>
                 BENEFICIARY A/C NO. : 916030006062915<br/>
                 BENEFICIARY BANK 	 : AXIS BANK LTD.<br/>
                 Branch Address 	 : T-13/2366, Bawana Road, NARELA, Delhi – 110040<br/>
                 AXIS BANK SWIFT CODE: AXISINBB040<br/>
                 Corresponding Bank 	: JP Morgan Chase Bank<br/>
                 Corresponding Bank Swift Code: CHASUS33<br/>
                 Axis Bank Account No. with Corresponding Bank: 001-1-407376<br/>

            </td>
        </tr>
        <tr>
            <td style="white-space: nowrap;">
                <strong>4. Transit Insurance</strong>
            </td>
            <td >
                :&nbsp;Buyer’s Scope.
            </td>
        </tr>
        <tr>
            <td style="white-space: nowrap;">
                <strong>5. Third Party Inspection<br/>
                /Certification (If Any)</strong>
            </td>
            <td >
                :&nbsp;Buyer’s Scope.
            </td>
        </tr>
        <tr>
            <td style="white-space: nowrap;">
                <strong>6. Warranty</strong>
            </td>
            <td >
                :&nbsp;The machines manufactured by us are warranted for one year (from the date of invoice) against any manufacturing defects, (excluding rubber parts, shearing blades, pressure gauge and electrical parts, being bought out items does not form part of our warranty. However the warranty card given by the outside manufacturer can be given to you the warranty does not cover the machine against any misuse, neglect, poor storage, improper maintenance or normal wear and tear, also no claim for carriage freight, duty, and loss of profit or consequential damages any type will be entertained and all the replacement or repair shall be carried at our works Delhi during warranty.<br/>
                :&nbsp;1st time the installation should be done under the supervision of AHTPL Engineer only else
                 AHTPL will not be responsible for any damage and it will not be covered under warranty.
            </td>
        </tr>
        <tr>
            <td style="white-space: nowrap;">
                <strong><u>7. Installation/Maintenance</u></strong>
            </td>
            <td >
               :&nbsp; <strong><u>SUPPLIER’S SCOPE: </u></strong><br/>
                Our following technician can supervise the installation/Maintenance of the machine at your site.a. Erection Staff: 1-2 Nos. depending upon requirement.<br/>
               : &nbsp;<strong> <u>BUYER’S SCOPE: </u> </strong>  <br/>
               <strong> 1.</strong><br/>
               a) Return air ticket (Economy Class).<br/>
               b)  Arrangement of pick up and drop facility (client’s airport).<br/>
               c) Visa.<br/>
               d) Lodging.<br/>
               e) Boarding.<br/>
               f) Local Conveyance.<br/>
               g) All Covid test, yellow fever card etc…(In case if it’s required).<br/>
               h) Medical Facility (In case if it’s required).<br/>
               <strong> I)&nbsp; <u>OUT OF POCKET EXPENSES:</u></strong><br/> 
                -  In Case of Installation	 : USD 100.00 Per day per person from the date of departure upto arrival in India.<br/>
                -  During Warranty Period : USD 100.00 Per day per person from the date of departure upto arrival in India.<br/>
                -  After Warranty Period	 : USD 100.00 Per day per person from the date of departure upto arrival in India.

            </td>
        </tr>
        <tr>
            <td style="white-space: nowrap;">
            </td>
            <td >
              <strong> j)&nbsp; <u>LABOUR CHARGES:</u></strong><br/>
               - 	In Case of Installation	  : NIL<br/>
               -  	During Warranty Period  : NIL<br/>
               -    After Warranty Period	  : USD 75.00 Per day per person from the date of departure upto arrival in India.<br/> 
               2. Normal tools and tackles.<br/>
               3. Local Support / Helpers.<br/>
               4. Welding machine/gas cutter with LPG and oxygen cylinder (If required).<br/>
               5. Civil works (if any).<br/>
               6. Crane with shilling. <br/>
               7. Power supply up to machine panel. <br/>
               8. Hydraulic Oil.<br/>
               9. Proper water leveled firm ground.
            </td>
        </tr>    
        <tr>
            <td style="white-space: nowrap;">
                <strong>8. Special Note</strong>
            </td>
            <td >
               :&nbsp;The Oil Seals should be replaced within 50,000 cycles of operation as a Standard 
                    Preventive Maintenance Procedure. After expiring of above cycle, the worn out Oil Seals 
                    can damage the internal surface of Cylinder.<br/>
                Damage due to worn out Seals shall be out of our warranty.<br/>
                <strong>:The machine productivity is strongly dependent on the size and composition 
                of Input material, feeding mechanism of the material as well as the skills of machine
                operator.</strong><br/>
                :&nbsp;Buyers will not be permitted to cancel the order once placed and demand refunds of advance paid when the order is booked.<br/>
                :&nbsp;If any disputes or differences shall arise between the supplier and buyer effect this contract, the same shall be amicably settled by direct negotiation between the parties here to, failing which such matter shall be referred to arbitration and adjudication under the Indian arbitration act. Arbitration shall be at New Delhi only.<br/>
                <strong>:&nbsp;Any other thing which is not mentioned in the specification shall not form part of the machine unless agreed to by us in writing.</strong> <br/> 
                :&nbsp;Any other clause, which is not mentioned in our offer, shall not be binding on us unless agreed to by us in writing.
            </td>
        </tr>
        </table>
        <div class="company-info" style="text-align: left;font-family: Arial, sans-serif;">
        <p><strong>For Advance Hydrau-Tech Pvt. Ltd</strong></p>
        <p>(Director)</p>
    </div>
   """)
   note1 = fields.Html(string='Notes One' , default="""
          <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="white-space: nowrap;">
                <strong>Transit Insurance </strong>
            </td>
            <td >
                :Buyer’s Scope.
            </td>
        </tr>
        <tr>
            <td  style="white-space: nowrap;">
                <strong>Hydraulic Oil :</strong>
            </td>
            <td style="padding-bottom: 10px;">
                Buyer’s Scope.
            </td>
        </tr>
        <tr>
            <td style="padding-bottom: 10px;">
                <strong>Warranty :</strong>
            </td>
            <td style="padding-bottom: 10px;">
                The machines manufactured by us are warranted for one year (from the date of invoice) against any manufacturing defects, (excluding rubber parts, shearing blades, pressure gauge and electrical parts, being bought out items does not form part of our warranty. However the warranty card given by the outside manufacturer can be given to you the warranty does not cover the machine against any misuse, neglect, poor storage, improper maintenance or normal wear and tear, also no claim for carriage freight, duty, and loss of profit or consequential damages any type will be entertained and all the replacement or repair shall be carried at our works Delhi during warranty.
            </td>
        </tr>
        <tr>
            <td style="padding-bottom: 10px;">
                <strong>Installation :</strong>
            </td>
            <td style="padding-bottom: 10px;">
                <strong>Supplier’s Scope:</strong><br/>
                1. Our following technician shall guide / supervise free of charge for the installation and commissioning of the machine at your site.<br/>
                a. Erection Staff : 1 No.<br/>
                <strong>Buyer’s Scope:</strong><br/>
                1. Lodging, boarding and local conveyance of our technician.<br/>
                2. Normal tools and tackles.<br/>
                3. Local Support / Helpers.<br/>
                4. Welding machine / gas cutter with LPG and oxygen cylinder (If required).<br/>
                5. Civil works (if any).<br/>
                6. Crane with shilling.<br/>
                7. Power supply up to machine panel.<br/>
                8. Hydraulic Oil.<br/>
                9. Proper water leveled firm ground.
            </td>
        </tr>
        <tr>
            <td style="padding-bottom: 10px;">
                <strong>Special Note :</strong>
            </td>
            <td style="padding-bottom: 10px;">
                The Oil Seals should be replaced within 50,000 cycles of operation as a Standard Preventive Maintenance Procedure. After expiring of above cycle, the worn out Oil Seals can damage the internal surface of Cylinder. Damage due to worn out Seals shall be out of our Warranty.<br/>
                <strong>The machine productivity is strongly dependent on the size and composition of Input material, feeding mechanism of the material as well as the skills of machine operator.</strong><br/>
                Buyers will not be permitted to cancel the order once placed and demand refunds of advance paid when the order is booked.<br/>
                If any disputes or differences shall arise between the supplier and buyer effect this contract, the same shall be amicably settled by direct negotiation between the parties failing which such matter shall be referred to arbitration and adjudication under the Indian arbitration act. Arbitration shall take place at New Delhi only.<br/>
                <strong>Any other thing which is not mentioned in the specification shall not form part of the machine unless agreed to by us in writing. </strong><br/>
                Any other clause, which is not mentioned in our offer, shall not be binding on us unless agreed to by us inwriting.<br/>
            </td>
        </tr>
     </table>
     <div class="company-info" style="text-align: left;font-family: Arial, sans-serif;">
        <p><strong>For Advance Hydrau-Tech Pvt. Ltd</strong></p>
        <p>(SANJEEV CHAUDHARY)</p>
        <p><i>*This is a computer generated document and does not require a signature.</i></p>
    </div>
     
          """)
   term_and_condn = fields.Html(string='Terms And Conditions', default="""<p><strong>Terms & Conditions :- </strong> <br/>
                1&nbsp;.&nbsp;DELIVERY TIME /DAY&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;CAN BE EFFECTED WITH IN 7 TO 8 WORKING DAYS FROM THE DATE OF RECEIPT OF CONFIRM ORDER. <br/>
                2&nbsp;.&nbsp;TAX&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;IGST 18% EXTRA. <br/>
                3&nbsp;.&nbsp;FREIGHT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;TO PAY BASIS. <br/>             
                4&nbsp;.&nbsp;PAYMENT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;FULL AGAINST P.I.BEFORE DISPATCH. <br/>
                5&nbsp;.&nbsp;PACKING&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;&nbsp;EXTRA.  <br/>
                6&nbsp;.&nbsp;QUOTATION VALIDITY&nbsp;&nbsp;:&nbsp;&nbsp;7 DAY. <br/>
            </p>""") 
   note2 = fields.Html(string='Notes Two')
   note3 = fields.Html(string='Notes Three')
   note4 = fields.Html(string='Notes Four', default="""<div class="content" style="margin: 30px; font-family: Arial, sans-serif;">

    <!-- Title -->
    <h2 style="text-align: left; font-weight: bold; margin-bottom: 20px;">
        Salient Features of Triple Action Baler: -
    </h2>

    <!-- Features List -->
    <ul style="list-style: none; padding-left: 0; line-height: 2;">
        <li><strong>Fabricated Body with Quality plates.</strong></li>
        <li><strong>2 Ton Chiller/ A/C for cooling the Hydraulic Oil.</strong></li>
        <li><strong>Bale is thrown out of the chamber by Hydraulic Operated Robotic Arm.</strong></li>
        <li><strong>Push Button operation (PLC Controlled)</strong></li>
        <li><strong>Fastest Machine in its category.</strong></li>
        <li><strong>Latest Hydraulic System which causes less oil heating during production.</strong></li>
        <li><strong>No foundation is required for the machine.</strong></li>
        <li><strong>Machine can easily shift from one place to another place.</strong></li>
        <li><strong>Hydraulic Pumps are easily replaceable.</strong></li>
        <li><strong>No Specialized Operator is required for operating the machine.</strong></li>
        <li><strong>No need to dig pit in floor for bale ejection cylinder.</strong></li>
    </ul>

</div>   
           """)
   #vehicle_no = fields.Many2one('vehicle.no',string="Vehicle No.")
   #driver_name = fields.Many2one('res.partner',string="Driver Name")
   bank_details = fields.Html(string='Bank details', default="""
    <style>
        .terms-table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        .terms-row {
            display: grid;
            grid-template-columns: auto auto auto;
            gap: 10px; /* Space between columns */
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        .terms-number {
            text-align: left;
            
        }
        .terms-colon {
            text-align: center;
            
        }
        .terms-description {
            text-align: right;
           
        }
    </style>
    <table class="terms-table">
        <tr class="terms-row">
            <td class="terms-number">10.Bank A/c. details</td>
            <td class="terms-colon" style="padding-left: 15px;padding-right: 10px;">:</td>
            <td class="terms-description">ADVANCE HYDRAU – TECH PVT. LTD.<br/>AXIS BANK LTD, NARELA, DELHI BRANCH , BRANCH CODE – 1260<br/>A/C NO. 916030006062915<br/>RTGS – UTIB0001260</td>
        </tr>
    </table>    
        """)
   
   def get_tax_data(self):
        tax_data_lst = []
        taxes = []
        tax_totals_json = json.loads(self.tax_totals_json)
        if 'Untaxed Amount' in tax_totals_json['groups_by_subtotal']:
            tax_vals = tax_totals_json['groups_by_subtotal']['Untaxed Amount']
            for tax in tax_vals:
                taxes.append(tax['tax_group_name'])
        for tax_type in ['CGST', 'SGST', 'IGST']:
            tax_data = []
            tax_data.append(tax_type)
            if tax_type in taxes:
                for tax in tax_vals:
                    if tax['tax_group_name'] == tax_type:
                        tax_rate = (tax['tax_group_amount']/tax['tax_group_base_amount']) * 100
                        tax_data.append(tax_rate)
                        tax_data.append(tax['tax_group_base_amount'])
                        tax_data.append(float(tax['tax_group_amount']))
                        
                        tax_data_lst.append(tax_data)
                        # break
                   
            else:
                if tax_type in ['CGST', 'SGST']:
                    tax_rate = 9.0
                elif tax_type == 'IGST':
                    tax_rate = 18.0
                tax_data.append(tax_rate)
                tax_data.append('-')
                tax_data.append('-')
                tax_data_lst.append(tax_data)
        return tax_data_lst
        

   def number_in_words(self, number):
        Paise="0"
        list=str(number).split('.')
        if len(list)<2:
            list.append(Paise)
        value = " Rupees " + num2words(int(list[0]),lang='en_IN')+ " " + " And " +  num2words(int(list[1]),lang='en_IN') + " Paise Only"
        return value.title()
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('flat', 'Flat Amount'),
    ], string='Discount Type', default='percentage')

    flat_discount = fields.Float(string='Flat Discount', default=0.0)
    percentage_discount = fields.Float(string='Percentage Discount (%)', default=0.0)

    @api.depends('product_uom_qty', 'price_unit', 'tax_id', 'flat_discount', 'percentage_discount', 'discount_type')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line, considering the selected discount type.
        """
        for line in self:
            # Apply the selected discount type
            if line.discount_type == 'percentage':
                # Apply percentage discount
                discounted_price = line.price_unit * (1 - (line.percentage_discount / 100.0))
            else:
                # Apply flat discount
                discounted_price = line.price_unit - line.flat_discount

            # Ensure that the discounted price doesn't go negative
            if discounted_price < 0:
                discounted_price = 0

            taxes = line.tax_id.compute_all(discounted_price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
