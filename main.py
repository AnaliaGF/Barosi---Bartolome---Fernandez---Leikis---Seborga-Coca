#from modelo_orm import *
from gestionar_obras import GestionarObra
from funciones import *
from modelo_orm import Obra

gestion = GestionarObra()

gestion.conectar_db()

#SOLO SE TIENE QUE EJECUTAR LA PRIMERA VEZ
if (gestion.chequear_base() == False):
    gestion.mapear_orm()
    gestion.extraer_datos()
    gestion.limpiar_datos()
    gestion.cargar_datos()
#SOLO SE TIENE QUE EJECUTAR LA PRIMERA VEZ

print("*** SISTEMA DE CARGA Y MODIFICACIÓN DE OBRAS ***")

while True:
    respuesta = limpiar_input(input("¿Desea crear una nueva obra? (SI/NO): "))
    if respuesta !='SI' and respuesta !='NO':
       print("Debe escribir SI o NO.")
    else:  
        if respuesta == 'SI':
            obra = gestion.nueva_obra()
            obra.nuevo_proyecto()
            obra.iniciar_contratacion()
            obra.adjudicar_obra()
            obra.iniciar_obra()
            obra.actualizar_porcentaje_avance()

            while True:
                respuesta = limpiar_input(input("¿Desea incrementar el plazo? (SI/NO): "))
                if respuesta !='SI' and respuesta !='NO':   
                    print("Debe escribir SI o NO.")    
                else: 
                    if respuesta == 'SI':
                        obra.incrementar_plazo()
                    break
            
            while True:
                respuesta = limpiar_input(input("¿Desea incrementar la mano de obra? (SI/NO): "))
                if respuesta !='SI' and respuesta !='NO':   
                    print("Debe escribir SI o NO.")    
                else: 
                    if respuesta == 'SI':
                        obra.incrementar_mano_obra()
                    break
            
            continue
        else:
            break

while True:
    respuesta = limpiar_input(input("¿Desea finalizar una obra? (SI/NO): "))
    if respuesta != 'SI' and respuesta != 'NO':
        print("Debe escribir SI o NO.")
    else:
        if respuesta == 'SI':
            obras = Obra.select()
            for obra in obras:
                print(f"ID: {obra.id}, Nombre: {obra.nombre}, Porcentaje de avance: {obra.porcentaje_avance}")

            while True:
                try:
                    respuesta = int(limpiar_input(input("Ingrese el ID de obra a finalizar: ")))
                    obra = gestion.obtener_obra(respuesta)
                    if obra is None:
                        print('Obra Inexistente.')
                        continue
                    else:
                        obra.finalizar_obra()
                        break
                except ValueError:
                    print('El valor ingresado no es válido.')
                    continue
        else:
            break

while True:
    respuesta = limpiar_input(input("¿Desea rescindir una obra? (SI/NO): "))
    if respuesta !='SI' and respuesta !='NO':   
        print("Debe escribir SI o NO.")    
    else: 
        if respuesta == 'SI':
            obras = Obra.select()
            for obra in obras:
                print(f"ID: {obra.id}, Nombre: {obra.nombre}")

            while True:
                try:
                    respuesta = int(limpiar_input(input("Ingrese el ID de obra a rescindir: ")))
                    obra = gestion.obtener_obra(respuesta)
                    if obra == None:
                        print('Obra Inexistente.')
                        continue
                    else:
                        obra.rescindir_obra()
                        break
                except:                              
                    print('El valor ingresado no es valido.')
                    continue
        else:              
            break

respuesta = limpiar_input(input("¿Desea ver los indicadores? (SI/NO): "))

if respuesta !='SI' and respuesta !='NO':   
    print("Debe escribir SI o NO.")    
else: 

    if respuesta == 'SI':         
        gestion.obtener_indicadores()
        print ("Fin de los indicadores.")