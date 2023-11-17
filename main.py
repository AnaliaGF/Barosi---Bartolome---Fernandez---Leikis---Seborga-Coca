<<<<<<< HEAD
from modelo_orm import *

obranueva = obra(nombre = "kakaka")

print(obranueva.nombre)


obranueva.nombre = "Soterramiento tren Sarmiento"

print(obranueva.nombre)


obranueva.descripcion = "El tren tiene que pasar por abajo"
obranueva.beneficiario = "La comunidad en su conjunto"

=======
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
obra1.nuevo_proyecto()
obra2.nuevo_proyecto()

print("Información de la primera obra despues de iniciar el proyecto:")
for key, value in obra1.__dict__.items():
    print(f"{key}: {value}")
    
print("Información de la primera obra despues de iniciar el proyecto:")
for key, value in obra2.__dict__.items():
    print(f"{key}: {value}")
>>>>>>> 98988099bb8fe4310ca757d2922ae40d23146660
