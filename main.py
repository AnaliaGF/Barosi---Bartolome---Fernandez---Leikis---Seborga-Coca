#from modelo_orm import *
from gestionar_obras import GestionarObra

gestion = GestionarObra()

gestion.conectar_db()

#SOLO SE TIENE QUE EJECUTAR LA PRIMERA VEZ
if (gestion.chequear_base() == False):
    gestion.mapear_orm()
    gestion.extraer_datos()
    gestion.limpiar_datos()
    gestion.cargar_datos()
#SOLO SE TIENE QUE EJECUTAR LA PRIMERA VEZ

# Ejercicio 6
obra1 = gestion.nueva_obra()
obra2 = gestion.nueva_obra()

# Inicio Ejercicio 7
# Ejercicio 8
obra1.nuevo_proyecto()
obra2.nuevo_proyecto()

# Ejercicio 9
obra1.iniciar_contratacion()
obra2.iniciar_contratacion()

# Ejercicio 10
obra1.adjudicar_obra()
obra2.adjudicar_obra()

# Ejercicio 11
obra1.iniciar_obra()
obra2.iniciar_obra()

# Ejercicio 12
obra1.actualizar_porcentaje_avance()
obra2.actualizar_porcentaje_avance()

# Ejercicio 13 (opcional)
obra1.incrementar_plazo()

# Ejercicio 14 (opcional)
obra2.incrementar_mano_obra()

# Ejercicio 15
obra1.finalizar_obra()

# Ejercicio 16
obra2.rescindir_obra()

# Ejercicio 17
gestion.obtener_indicadores()

#NuevaObra = Obra()

# NuevaObra.id_etapa = 10
# NuevaObra.nombre = "Soterramiento Tren Sarmiento"

# NuevaObra.nuevo_proyecto()

# obra1.nuevo_proyecto()
# obra2.nuevo_proyecto()

# print("Información de la primera obra despues de iniciar el proyecto:")
# for key, value in obra1.__dict__.items():
#     print(f"{key}: {value}")
    
# print("Información de la primera obra despues de iniciar el proyecto:")
# for key, value in obra2.__dict__.items():
#     print(f"{key}: {value}")
