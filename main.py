from modelo_orm import *
from gestionar_obras import GestionarObra

gestion = GestionarObra()

gestion.conectar_db()
gestion.mapear_orm()

# Ejercicio 6
obra1 = gestion.nueva_obra()
obra2 = gestion.nueva_obra()

# Inicio Ejercicio 7

# Ejercicio 8

NuevaObra = Obra()

NuevaObra.id_etapa = 10
NuevaObra.nombre = "Soterramiento Tren Sarmiento"

NuevaObra.nuevo_proyecto()

obra1.nuevo_proyecto()
obra2.nuevo_proyecto()

print("Información de la primera obra despues de iniciar el proyecto:")
for key, value in obra1.__dict__.items():
    print(f"{key}: {value}")
    
print("Información de la primera obra despues de iniciar el proyecto:")
for key, value in obra2.__dict__.items():
    print(f"{key}: {value}")