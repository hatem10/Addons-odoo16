# -*- coding: utf-8 -*-
{
    'name': 'Culqi Tarjetas - Website Checkout',
    'description': "Recibe pagos con tarjetas a través del sitio web de comercio electrónico en divisa PEN & USD",
    'author': "ROCKSCRIPTS",
    'website': "https://wa.me/573128097090",
    'summary': "Culqi para sitio web de comercio electrónico",
    'version': '0.1',
    "license": "OPL-1",
    'price':'100',
    'currency':'USD',
    'support': 'rockscripts@gmail.com',
    'category': 'Website',
    "images": [
                "images/banner.png"
              ],
    'depends': [
                    'base',
                    'sale',
                    'website',
                    'website_sale',
                    'payment',
                    'account'
                ],
    'data': [
                'views/templates.xml',
                'views/payment_provider.xml',
                'views/sale_order.xml',
                'views/payment_transaction.xml',
                'views/partner.xml',
                'data/culqi.xml',
            ],
    'qweb': [
              
            ],
    'external_dependencies': {
                                "python" : [
                                                "culqi"
                                           ]
                             },
    "assets":{
        "web.assets_frontend":[
                "cards_culqi/static/src/js/jquery.js'",
                "cards_culqi/static/src/css/culqi.css",
                "cards_culqi/static/src/js/culqi.js",
        ],
        "web.assets_backend":[
                "/cards_culqi/static/src/css/culqi.css"
        ]
    },
    'installable': True,
}