DNI = "01"
CARNET = "03"
PASAPORTE = "06"

TYPE_DOCUMENT = [
    (DNI,"DNI"),
    (CARNET,"CARNET DE EXTANJERIA"),
    (PASAPORTE,"PASAPORTE")
]

BORRADOR = "draft"
REGISTRO = "register"
PREPARACION = "preparation"
REALIZADO = "done"

TYPE_STATE = [
    (BORRADOR,"Borrador"),
    (REGISTRO,"Registrado"),
    (PREPARACION,"En Preparacion"),
    (REALIZADO,"Realizado")
]