# -*- coding: utf-8 -*-
{
    'name': "hotel",
    'summary': "Hotel Management System",
    'description': "Hotel Guest Registration and Billing System",
    'author': "ROYTEK",
    'website': "https://www.roytek.odoo.com",

    'category': 'Uncategorized',
    'version': '18.0.1.4.0',

    'depends': ['base', 'web'],

    'license': 'LGPL-3',

    # Always loaded data
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/mainmenu.xml',
        'views/guestregistration.xml',
        'views/guests.xml',         
        'views/rooms.xml',         
        'views/roomtypes.xml',   
        'views/charges.xml', 
    
    ],

    'installable': True,
    'application': True,
}