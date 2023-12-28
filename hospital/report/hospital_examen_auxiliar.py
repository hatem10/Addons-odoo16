from odoo import models,fields,api

class ReportExamen_auxiliar(models.AbstractModel):
    _name = "report.hospital.report_hospital_examen_auxiliar"

    @api.model
    def _get_report_values(self,docids,data=None):
        query1 = """
            SELECT examen_aux.name as nr_solicitud,
               examen_aux.type_examen,
               examen_aux.date as fecha_exam_aux,
               examen_aux.type_seguro,
               examen_aux.acto_medico,
               examen_aux.date_atention,
               examen_aux.activity_specific,
               examen_aux.department,
               examen_aux.province,
               examen_aux.district,
               examen_aux.address,
               examen_aux.reference,
               examen_aux.mobile,
               examen_aux.phone,
               examen_aux.email,
               hosp_patient.name as patient,
               hosp_patient.type_document,
               hosp_patient.number_document,
               hosp_patient.sexo,
               hosp_patient.age,
               hist_clini.name as nr_history_clini,
               hosp_doctor.name as name_doctor,
               hosp_doctor.last_name last_name_doctor,
               hosp_speciality.name AS speciality
               FROM hospital_patient hosp_patient INNER JOIN hospital_examen_auxiliar examen_aux
            ON hosp_patient.id = examen_aux.patient_id INNER JOIN hospital_history_clinic hist_clini 
            ON examen_aux.history_clinic_id = hist_clini.id INNER JOIN hospital_doctor hosp_doctor
            ON hosp_doctor.id  = examen_aux.doctor_id INNER JOIN hospital_speciality hosp_speciality
            ON hosp_speciality.id = examen_aux.speciality_id
        """
        self.env.cr.execute(query1)
        obj_hospital_examen_auxiliar = self.env.cr.dictfetchall()
        print(obj_hospital_examen_auxiliar)
        data ={
            "data_examen_aux": obj_hospital_examen_auxiliar
        }
        return data