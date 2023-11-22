{
    "name":"food_order",
    "version":"16.0.0.1",
    "author":"Johao Marcos Maldonado Roman",
    "description":"Modulo Pedidos de Comida",
    "category":"Gastronomia",
    "depends":[
        "base",
        "mail"
    ],
    "data":[
        # security
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        #wizard
        "wizard/customer_whatsapp_wizard_view.xml",
        #views
        "views/order_customer_view.xml",
        "views/order_customer_address_view.xml",
        "views/order_product_view.xml",
        "views/order_view.xml",
        "views/menu.xml",
        #data
        "data/order_product.xml",
        "data/order.xml"
    ],
    "assets":{
        "web.assets_frontend":[],
        "web.assets_backend":[]
    },
    "instalabale":True
}