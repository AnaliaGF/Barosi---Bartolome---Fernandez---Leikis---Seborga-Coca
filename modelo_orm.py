import datetime
from peewee import *

db = Proxy()

class BaseModel(Model):
    id = PrimaryKeyField()
    nombre = CharField()

    class Meta:
        database = db

class Entorno(BaseModel):
    pass

class Etapa(BaseModel):
    pass

class Tipo_obra(BaseModel):
    pass

class Area_responsable(BaseModel):
    pass

class Barrio(BaseModel):
    comuna = CharField()

class Empresa(BaseModel):
    cuit = CharField()

class Contratacion_tipo(BaseModel):
    pass

class Obra(BaseModel):
    id_entorno = ForeignKeyField(Entorno, to_field="id", null = True, db_column="id_entorno") 
    id_etapa = ForeignKeyField(Etapa, to_field="id", db_column="id_etapa")
    id_tipo_obra = ForeignKeyField(Tipo_obra, to_field="id", db_column="id_tipo_obra")
    id_area_responsable = ForeignKeyField(Area_responsable, to_field="id", db_column="id_area_responsable")
    descripcion = CharField(null=True)
    monto_contrato = IntegerField(null=True)
    id_barrio = ForeignKeyField(Barrio, to_field="id", db_column="id_barrio")
    direccion = CharField(null=True)
    fecha_inicio = DateTimeField(null=True)
    fecha_fin_inicial = DateTimeField(null=True)
    plazo_meses = IntegerField(null=True)
    porcentaje_avance = FloatField(null=True)
    imagen_1 = CharField(null=True)
    imagen_2 = CharField(null=True)
    imagen_3 = CharField(null=True)
    imagen_4 = CharField(null=True)
    id_empresa = ForeignKeyField(Empresa, to_field="id", null=True, db_column="id_empresa")
    licitacion_anio = IntegerField(null=True)
    id_contratacion_tipo = ForeignKeyField(Contratacion_tipo, to_field="id", null=True, db_column="id_contratacion_tipo")
    nro_contratacion = CharField(null=True)
    mano_obra = CharField(null=True)
    numero_expediente = CharField(null=True)
    destacada = BooleanField(null=False)
    fuente_financiamiento = CharField(null=True)

    # Inicio Ejercicio 5

    def nuevo_proyecto(self):
 
        # Opcion 1
        # self.nombre = input("Ingrese el nombre: ")
        # self.descripcion = input("Ingrese la descripcion: ")

        # etapa = Etapa.get(Etapa.nombre == "PROYECTO")
        # self.id_etapa = etapa

        # self.destacada = False

        # while True:
        #     try:
        #         self.id_tipo_obra = Tipo_obra.get(nombre=input("Ingrese el tipo de obra: "))
        #     except:
        #         print("Tipo de Obra inexistente.")
        #         continue
        #     else:
        #         break
 
        # while True:
        #     try:
        #         self.id_area_responsable = Area_responsable.get(nombre=input("Ingrese el área responsable: "))
        #     except:
        #         print("Área responsable inexistente.")
        #         continue
        #     else:
        #         break

        # while True:
        #     try:
        #         self.id_barrio = Barrio.get(nombre=input("Ingrese el nombre del barrio: "))
        #     except:
        #         print("Nombre de barrio inexistente.")
        #         continue
        #     else:
        #         break

        # self.save()
        # print("Nuevo proyecto de obra creado.")
    
        # Opcion 2
        
        self.id_etapa = Etapa.get(Etapa.nombre == "PROYECTO")
        self.destacada = False

        if (self.nombre == None or self.id_etapa == None or self.id_area_responsable == None or self.id_barrio == None):
            return False
        else:
            self.save()
            return True    

    def iniciar_contratacion(self):
        while True:
            try:
                self.id_contratacion_tipo = Contratacion_tipo.get(nombre=input("Ingrese el tipo de contratación: "))
            except:
                print("Tipo de contratacion inexistente.")
                continue
            else:
                break
        
        self.nro_contratacion = input("Ingrese el número de contratación: ")

        self.save()
        print("Contrato iniciado.")
        
    def adjudicar_obra(self):
        while True:
            try:
                self.cuit = Empresa.get(nombre=input("Ingrese la empresa a adjudicar la obra: "))
            except:
                print("Empresa inexistente.")
                continue
            else:
                break
        
        self.nro_expediente = input("Ingrese número de expediente: ")

        self.save()
        print("Obra adjudicada.")
        
    def iniciar_obra(self):
        self.destacada = input("Indique si la obra es destacada: ")
        self.fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        self.fecha_fin_inicial = input("Ingrese la fecha de fin inicial (YYYY-MM-DD): ")
        self.fuente_financiamiento = input("Ingrese la fuente de financiamiento: ")
        self.mano_obra = int(input("Ingrese la cantidad de mano de obra: "))

        self.save()
        print("Obra iniciada.")
        
    def actualizar_porcentaje_avance(self):
        self.porcentaje_avance = float(input("Ingrese el porcentaje de avance actualizado: "))

        self.save()
        print("Porcentaje de avance actualizado.")

    def incrementar_plazo(self):
        self.plazo_meses = int(input("Ingrese el plazo en meses actualizado: "))

        self.save()
        print("Plazo incrementado.")
        
    def incrementar_mano_obra(self):
        self.mano_obra = int(input("Ingrese la cantidad de mano de obra actualizada: "))

        self.save()
        print("Mano de obra incrementada.")
        
    def finalizar_obra(self):
        etapa = Etapa.get(Etapa.nombre == "FINALIZADA")
        self.id_etapa = etapa
            
        self.porcentaje_avance = Obra.get(Obra.porcentaje_avance == "100")

        self.save()
        print("Obra finalizada.")

    def rescindir_obra(self):
        etapa = Etapa.get(Etapa.nombre == "RESCINDIDA")
        self.id_etapa = etapa
    
        self.save()
        print("Obra rescindida.")