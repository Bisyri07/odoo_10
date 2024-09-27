{
    'name':'Booking Order',
    'version':'1.0',
    'category':'Sales',
    'summary':'service_team, sale.order, work_order',

    'description':"""
    This module aims to pass technical test
    """,

    'authon':'Bisyri',
    'website':'https://github.com/Bisyri07/odoo_10',
    'application':True,
    'depends':[
        'base','crm'
    ],

    'data':[
        # security
        'security/ir.model.access.csv',

        # view
        'views/service_team.xml',
        # 'views/main_menu.xml'
    ]
}