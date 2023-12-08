{
    "name":"hospital",
    "version":"16.0.0.1",
    "author":"Johao Marcos Maldonado Roman",
    "description":"Modulo para hospitales",
    "category":"Sector Salud",
    "depends":[
        "base"
    ],
    "data":[
        #views
        "views/hospital_patient_view.xml",
        "views/menu.xml",
        "static/template/patient.xml",
        #security
        "security/res_groups.xml",
        "security/ir.model.access.csv"
    ],
    "assets":{
        "web.assets_frontend":[],
        "web.assets_backend":[]
    },
    "instalabale":True
}