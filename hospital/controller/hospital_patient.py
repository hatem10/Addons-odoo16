from odoo import http
from odoo.http import request
from datetime import date
import json

class Patient(http.Controller):

    @http.route("/create-patient",methods=["GET"],type="http",auth="user",website=True)
    def create_patient(self,**kwargs):
        obj_hospital_patient = request.env["hospital.patient"]
        data = {
            "name":"Nelson Condori Andrade Lorenzo",
            "full_name":"Nelson Condori",
            "father_last_name":"Andrade",
            "mother_last_name":"Lorenzo",
            "date_birth":date(1995,6,13),
            "age":23,
            "type_document":"01",
            "number_document":75385145
        }
        obj_hospital_patient.create(data)
        context = {
                "message":"Se creo el registro exitosamente"
            }
        return json.dumps(context)
    @http.route("/list-patient",methods=["GET"],type="http",auth="user",website=True)
    def List_Patient(self,**kwargs):
        #obj_hospital_patient = request.env["hospital.patient"].search([])
        query1 = """
            SELECT  id,
                    name,
                    full_name,
                    father_last_name,
                    mother_last_name,
                    TO_CHAR(date_birth,'YYYY/MM/DD') AS date,
                    age,
                    type_document,
                    number_document
            FROM hospital_patient
        """
        request.env.cr.execute(query1)
        obj_hospital_patient = request.env.cr.dictfetchall()

        if obj_hospital_patient:
            context={
                "patient":obj_hospital_patient
            }
        else :
            context={
                "message":"No existe Registros"
            }
        return request.render("hospital.list_patient",context)

    @http.route("/update-patient/<id_patient>",methods=["GET"],type="http",auth="user",website=True)
    def Update_Patient(self,**kwargs):
        id_hospital_patient = kwargs.get("id_patient",False)
        print("****Id**",id_hospital_patient)
        obj_hospital_patient = request.env["hospital.patient"].search([("id","=",id_hospital_patient)])
        if obj_hospital_patient:
            data = {
                "date_birth":date(2000,2,27),
                "age":28
            }
            obj_hospital_patient.write(data)
            context = {
                "message":"Se actualizo el paciente %s" %(obj_hospital_patient.name)
            }
        else:
            context = {
                "message": "No existe el paciente "
            }

        return json.dumps(context)

    @http.route("/delete-patient/<id_patient>",methods=["GET"],type="http",auth="user",website=True)
    def Delete_Patient(self,**kwargs):
        id_hospital_patient = kwargs.get("id_patient",False)
        obj_hospital_patient = request.env["hospital.patient"].search([("id","=",id_hospital_patient)])
        if obj_hospital_patient:
            obj_hospital_patient.unlink()
            context ={
                "message":"Se elimino correctamente"
            }
        else:
            context = {
                "message":"No existe paciente a eliminar"
            }
        return json.dumps(context)