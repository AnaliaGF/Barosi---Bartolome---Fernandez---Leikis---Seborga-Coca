# Sistema de Carga y Modificación de Obras

## Instalación de Dependencias
Asegúrate de tener instaladas las dependencias ejecutando el siguiente comando en consola:
'pip install -r requirements.txt'

## Uso del Sistema

1. Iniciar el Sistema
Ejecuta el archivo 'main.py' para iniciar el sistema de gestión de obras.

2. Crear una Nueva Obra
Al seleccionar la opción "¿Desea crear una nueva obra? (SI):", podrás ingresar los datos de una nueva obra que se cargarán en la base de datos.

2.1.1 Etapa: PROYECTO
Nombre, descripción, tipo, área responsable, y barrio.

2.1.2 Etapa: EN LICITACION
Tipo de Contratación y Número de Contratación.

2.1.3 Etapa: EN CURSO
Adjudicación a una Empresa y Número de Expediente.

2.1.4 Etapa: INICIADA
Verificación de si es una obra destacada, fecha de inicio, fecha de finalización estimada, fuente de financiamiento, y cantidad de mano de obra.

2.1.5 Etapa: EN OBRA
Porcentaje de avance.

2.2 Incrementar Plazo
Selecciona "¿Desea incrementar el plazo? (SI):" para ingresar el nuevo plazo en meses.

2.3 Incrementar Mano de Obra
Selecciona "¿Desea incrementar la mano de obra? (SI):" para ingresar el nuevo número de mano de obra, modificando el ingresado anteriormente.

3. Finalizar una Obra
Selecciona "¿Desea finalizar una obra? (SI):" para visualizar una lista de todas las obras. Ingresa el ID correspondiente para que la obra cambie a la etapa "FINALIZADA".

4. Rescindir una Obra
Selecciona "¿Desea rescindir una obra? (SI):" para visualizar una lista de todas las obras. Ingresa el ID correspondiente para que la obra canbie a la etapa "RESCINDIDA".

5. Ver datos y estadísticas
Selecciona "¿Desea ver los indicadores? (SI):" para visualizar una lista con los datos más relevantes extraídos de la base de datos.