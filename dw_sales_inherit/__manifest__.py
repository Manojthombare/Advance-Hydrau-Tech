{
    'name' : 'DW Sales',
    'version':'1.0.0',
    'author':'Dreamwarez',    
    'website':'www.dreamwarez.in',
    'name':  'Advance Hydrau-Tech Pvt. Ltd.',
    'description': " This module developed tpo do some custom functionalities in sales module",
    'category': 'sales',
    'sequence': -103,
    'depends' : ['sale','web','product'],
    "data": [
        'data/ir_sequence_data.xml',
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "reports/report_menu.xml",
        "reports/quatation_page_format.xml",
        "reports/quotation_template.xml",
        "reports/quotation_order_template.xml",
        "reports/proforma_invoice_template.xml",
        # "reports/report_saleorder.xml",
        "reports/installlation_template.xml",
        "reports/warranty_template.xml",
        "views/installation_view.xml",
        "views/warranty_view.xml",
      #  "views/warranty_report_views.xml",
        "views/contact_list_view.xml",
        "reports/datewise_installation_records.xml",
        "views/datwise_installation_records_view.xml",
    ],
    'installable':True, 
    'auto-install':False,
    'application':True,
    'license' :'LGPL-3',
    'assets':{}
}
