# -*- coding: utf-8 -*-
##############################################################################
#    
#   Dreamwarez
#   Copyright (C) 2014-Today Dreamwarez (<http://www.dreamwarez.in>).
#
#   Odoo Proprietary License v1.0 (OPL-1)
#
#   This software and associated files (the "Software") may only be used (executed,
#   modified, executed after modifications) if you have purchased a valid license
#   from the authors, typically via Odoo Apps, or if you have received a written
#   agreement from the authors of the Software.
#
#   You may develop Odoo modules that use the Software as a library (typically
#   by depending on it, importing it and using its resources), but without copying
#   any source code or material from the Software. You may distribute those
#   modules under the license of your choice, provided that this license is
#   compatible with the terms of the Odoo Proprietary License (For example:
#   LGPL, MIT, or proprietary licenses similar to this one).
#
#   It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#   or modified copies of the Software.
#
#   The above copyright notice and this permission notice must be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#  
#
##############################################################################


# import time
import logging
# from openerp.osv import fields, osv
# from openerp.tools.translate import _

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class account_tax(models.Model):
    _inherit = 'account.tax'
    
    def data_validation(self,cr,uid,ids,context=None):
        current_record=self.browse(cr,uid,ids,context=context)
        _logger.debug(".......current_record..."+str(current_record))
        if current_record:
            seq=current_record[0].x_tax_weight
            type=current_record[0].x_gst_type
            search_ids=self.search(cr,uid,[('x_tax_weight','=',seq),('x_gst_type','=',type)],context=context)
            _logger.debug(".......search_ids..."+str(search_ids))
            if len(search_ids) > 1:
                return False
            else:
                return True
        return True

    x_gst_type =  fields.Selection([('GST', 'GST'), ('CGST','CGST'),('SGST','SGST'),('IGST','IGST')], 'GST Tax Type')
    x_tax_weight = fields.Integer('Tax Weight')
    
    
    _constraints = [(data_validation, 'Error:coloumn Weight must be unique for each GST tax.', ['x_tax_weight'])]
