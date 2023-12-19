{
    "name":"hospital",
    "version":"16.0.0.1",
    "author":"Johao Marcos Maldonado Roman",
    "description":"Modulo para hospitales",
    "category":"Sector Salud",
    "depends":[
        "base",
        "mail"
    ],
    "data":[
        #data
        "data/hospital_patient.xml",
        "data/hospital_doctor.xml",
        "data/hospital_history_clinic.xml",
        "data/hospital_type_examen.xml",
        #views
        "views/hospital_patient_view.xml",
        "views/hospital_doctor_view.xml",
        "views/hospital_history_clinic_view.xml",
        "views/hospital_examen_auxiliar_view.xml",
        "views/hospital_type_examen_view.xml",
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