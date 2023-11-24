import datetime
from peewee import *
from funciones import *

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

class Tipo_contratacion(BaseModel):
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
    id_tipo_contratacion = ForeignKeyField(Tipo_contratacion, to_field="id", null=True, db_column="id_tipo_contratacion")
    nro_contratacion = CharField(null=True)
    mano_obra = CharField(null=True)
    numero_expediente = CharField(null=True)
    destacada = BooleanField(null=False)
    fuente_financiamiento = CharField(null=True)

    def nuevo_proyecto(self):      
        self.id_etapa = Etapa.get(Etapa.nombre == "PROYECTO")
        self.destacada = False

        if (self.nombre == None or self.id_etapa == None or self.id_area_responsable == None or self.id_barrio == None):
            return False
        else:
            self.save()
            return True    

    def iniciar_contratacion(self):
        tipos_contratacion = Tipo_contratacion.select()
        for tipo in tipos_contratacion:
            print(tipo.nombre)

        while True:
            tipo_contratacion_nombre = limpiar_input(input("Ingrese el tipo de contratación de la lista anterior: "))
            tipo_contratacion = next((tipo for tipo in tipos_contratacion if tipo.nombre == tipo_contratacion_nombre), None)
            if tipo_contratacion:
                self.id_contratacion_tipo = tipo_contratacion
                break
            else:
                print("Tipo de contratación inexistente. Por favor, elija un tipo existente.")

        self.nro_contratacion = input("Ingrese el número de contratación: ")

        etapa = Etapa.get(Etapa.nombre == "EN LICITACION")
        self.id_etapa = etapa

        self.save()
        print("Contratación iniciada correctamente.")    
     
    def adjudicar_obra(self):
        empresas = Empresa.select()
        for empresa in empresas:
            print(empresa.nombre)

        while True:
                self.empresa_nombre = limpiar_input(input("Ingrese la empresa a adjudicar de la lista anterior: "))
                empresa = next((emp for emp in empresas if emp.nombre == self.empresa_nombre), None)
                if empresa:
                    break
                else:
                    print("Empresa inexistente. Por favor, elija una empresa existente.")
        
        self.nro_expediente = input("Ingrese número de expediente: ")

        etapa = Etapa.get(Etapa.nombre == "EN CURSO")
        self.id_etapa = etapa

        self.save()
        print("Obra adjudicada correctamente.")

    def iniciar_obra(self):
        while True:
            self.destacada = limpiar_input(input("Indique si la obra es destacada (SI/NO): "))
            if self.destacada!='SI' and self.destacada!='NO':
                print("Debe escribir SI o NO.")
            else:
                break

        while True:           
            self.fecha_inicio = input("Ingrese fecha de inicio (DD/MM/AAAA): ")
            try:
                datetime.datetime.strptime(self.fecha_inicio, '%d/%m/%Y')
            except ValueError:
                print ('Fecha inválida.')
            else:
                break

        while True:
            self.fecha_fin_inicial = input("Ingrese fecha de fin estimada (DD/MM/AAAA): ")
            try:
                datetime.datetime.strptime(self.fecha_fin_inicial, '%d/%m/%Y')
            except ValueError:
                print ('Fecha inválida.')
            else:
                break
    
        while True:
            self.fuente_financiamiento = limpiar_input(input("Ingrese la fuente de financiamiento: "))       
            if self.fuente_financiamiento == "":
                print("Debe ingresar fuente financiamiento.")
            else:
                break

        while True:
            try:
                self.mano_obra = int(input("Ingrese en números la cantidad de mano de obra: "))
            except ValueError:
                print("Debe ingresar un número.")
            else:
                break

        etapa = Etapa.get(Etapa.nombre == "INICIADA")
        self.id_etapa = etapa

        self.save()
        print("Obra iniciada correctamente.")
        
    def actualizar_porcentaje_avance(self):
        while True:
            try:
                self.porcentaje_avance = float(input("Ingrese el porcentaje de avance actualizado: "))
            except ValueError:
                print("Debe ingresar un número.")
            else:
                break

        etapa = Etapa.get(Etapa.nombre == "EN OBRA")
        self.id_etapa = etapa

        self.save()
        print("Porcentaje de avance actualizado correctamente.")

    def incrementar_plazo(self):
        while True:
            try:
                self.plazo_meses = int(input("Ingrese el plazo en meses actualizado: "))
            except ValueError:
                print("Debe ingresar un número.")
            else:
                break

        etapa = Etapa.get(Etapa.nombre == "EN OBRA")
        self.id_etapa = etapa

        self.save()
        print("Plazo incrementado.")
        
    def incrementar_mano_obra(self):
        while True:
            try:
                self.mano_obra = int(input("Ingrese la cantidad de mano de obra actualizada: "))
            except ValueError:
                print("Debe ingresar un número.")
            else:
                break

        etapa = Etapa.get(Etapa.nombre == "EN OBRA")
        self.id_etapa = etapa

        self.save()
        print("Mano de obra incrementada.")
        
    def finalizar_obra(self):
        etapa = Etapa.get(Etapa.nombre == "FINALIZADA")
        self.id_etapa = etapa
            
        self.porcentaje_avance = 100

        self.save()
        print("Obra finalizada.")

    def rescindir_obra(self):
        etapa = Etapa.get(Etapa.nombre == "RESCINDIDA")
        self.id_etapa = etapa
    
        self.save()
        print("Obra rescindida.")