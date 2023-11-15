from modelo_orm import *

obranueva = obra(nombre = "kakaka")

print(obranueva.nombre)


obranueva.nombre = "Soterramiento tren Sarmiento"

print(obranueva.nombre)


obranueva.descripcion = "El tren tiene que pasar por abajo"
obranueva.beneficiario = "La comunidad en su conjunto"

