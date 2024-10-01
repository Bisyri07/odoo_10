{
    'name':'Booking Order',
    'version':'1.0',
    'category':'Sales',
    'summary':'service_team, sale.order, work_order',

    'description':"""
    This module aims to make booking order
    """,

    'authon':'Bisyri',
    'website':'https://github.com/Bisyri07/odoo_10',
    'application':True,
    'depends':[
        'base','sale'
    ],

    'data':[
        # security
        'security/ir.model.access.csv',

        # sequence
        'views/sequences/work_order_seq.xml',
        
        # view
        'views/booking_order.xml',
        'views/service_team.xml',
        'views/work_order.xml',
        'views/main_menu.xml',

        # report
        'views/reports/work_order_report.xml',
        'views/reports/report.xml',

    ]
}