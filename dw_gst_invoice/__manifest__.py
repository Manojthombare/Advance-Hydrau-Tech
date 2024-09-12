{
    'name': 'Gst Account Invoice',
    'version':'5.0.11',
    'description':"""
      5.0.3 Added Two hardcoded message on invoice print.
    """,
    'author': 'Dreamwarez',
    'depends': ['base','account'],
    'data': ['security/ir.model.access.csv',
              'account_taxes_view.xml'
            ],
    'installable': True,
    'license' :'LGPL-3',
    'sequence': -150,
    'auto_install': False,
    'application':True,
    }

################################################################################
#                                CHANGE LOG
#   1.0.0     Newly Created Module.
#   1.0.1---Added functionality to hide discount from Gst Invoice Print on boolean field selection and also inherited res partner form view to add Gstin no on partner profile aos print on Gst invoice Report .
#  Changes as follows:--------------BY Ganesh 
#        1)Added x_serial_no to account_invoice_line class and also inherit foem view to add after hsn code.
#        2)Chanhe in Gst Invoice Rerport -1)replaced string from  "Invoice Serial No" to--> "Invoice No" and set to bold  2]set to bold to dispatch detai columns
#                                                                 3)update "Details of receiver(Billed to ) details" --set to bold and added new field Zip ,phone /mobile no ,email
#       3)Added Sr No logic to print when sr_no is present then it will print on report under that product in ( ) parenthesis.
#      4)Added space for customer;s signature at bottom of Gst Invoice
# 2.0.0-#gst_invoice:-----------------------------------------------------------By Kalyani Ugale
#   1.GSTIN No in accounting-> put it after delivary category.
#   2.Hide the rate field like discount when we set the rate field as True.
#   3.Instead of Place of Supply on the form -> make it Site Address and pass the value of site address in it.
#3.0.0 --
#**************** Changes by Kalyani Ugale on 16th august in report*******************
#   1)Increased the size of Company Name and company Address.
#   2)Increased the size of companys logo.
#   3)Added mobile No., email and GST No. fields on the form below companys contact no. field and email field.
#   4)Contents of Details of receiver is shifted below the comapnys logo.
#   5)In Details of receiver contents , mobile number and email fields are added below state code & state fields and above GST No.
#   6)In Delivery Note field, challan no. is passed from warehouse and if their is any additional information written on the form is passed in it.
#   7)In Buyers order No. field, purchase order number is passed from warehouse.
#   8)In Buyers order Date field, purchase order date. is passed from warehouse.
#   9)Increase the size of Invoice serial number and make it bold.
#   10)Bold the Name of Details of receiver.
#   11)Increase the coloum size of description of goods and amounts of CGST,SGST and IGST taxes.
#   12)Reduce the coloum size of UOM, Discount and rate of CGST,SGST and IGST taxes.
#   13)Display the amount of invoice value(in words) infront of it. before Invoice total column.
#   14)Added Tax bifurcation table below Invoice value(in words) field.
#   15)Below Tax bifurcation table, certified that the particulars given above true and correct table is added.
#   16)Added 3 coloums of Term and condition of sale , Bank Details and SB ELECTRICALS in one table below certified that the particulars given above true   and correct table.
#   17)If there is any additional information written on the form , then it will get displayed on last line of Term and condition of sale.
#   18)Add the space in between each line of Sign and Stamp, Vehicle Number, Mobile Number and Name fields.
#   19)In Name of Details if receiver, Landmark field is added.
#   20)Remove print_type_field from form and report.
#   21)Add Buyers order number field infront of Buyers order date.
#   22)"is_a_consignee" is by default set to true.
#   23)On the top space is removed in 3 coloums of Term and condition of sale , Bank Details and SB ELECTRICALS in one table below certified that the particulars given above true   and correct table.
#   24)On the top space is removed of Sign and Stamp, Vehicle Number, Mobile Number and Name fields.
#4.0.0 -- 
#    1)Created and added 'x_print_count' integer field on the form and on tree view. Also get_print_count function is called.   on 18th august byKalyani Ugale
#    2)Created No print count i.e. x_no_print_count' field. ----------   on 19th august by Kalyani Ugale
#    3) Print Count, No Print Count and Invoice Print count fields are added in filters and group by. -----on 19th august by Kalyani Ugale
#5.0.0 -- Changes by kalyani ugale on 6th sept
#   1)Created the print format of invoice_print by code.
#   2)Added Serial no. on the invoice print.
#  5.0.1---Changes By Ganesh...
#   1)Changed name from 'Invoice Serial Number' to 'Tax Invoice Serial Number'
#   2)Added functionality to print Pin code of customer on print.
#   5.0.2--Changes By Ganesh.
#   1)Rearranged report.
# *****by chetan jadhav****
# 30 march 2018 
# changes in module gst invoice (Invoice No Bold)
#
# BY CHETAN JADHAV 16, may 18
# x_gstin_no which is already present in res.partner made him required
# ************** Krushna ****************
# 5.0.3 Added Two hardcoded message on invoice print.
#
# BY CHETAN JADHAV 22 dec 18,
#5.0.4 added two field 
#1) 'x_operation' - to select overdue or outstanding for customer to view its invoices ,
#2) 'x_set_priority' - to set rating to customer
#3) made invoice print small(font)
#5.0.5
#1) bug fix duplicate mobile number on print. 
#2) can print invoice in draft state also.
# 5.0.6  - 
#    1) On GST Print - printing sales person and its mobile No.
#5.0.7 -
#    1) SalesPerson Update smart button on partner profile to update salesperson on respected partners quatation,sales order and on invoices.
#5.0.8 - Gst Invoice print size change(small font size)
#5.0.9 - Code corrected only for hide discount on print equal to True (GST Invoice)
#5.0.10 - 1) Special Discount Product Hide from Invoice Print
#         2) Special Disocunt, Subtotal,Total shown on invoice
#5.0.11 - 1) sending ledger to all partners through email on 5th day of every month.
 ##################################################################
