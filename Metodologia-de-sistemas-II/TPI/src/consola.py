if __package__:
    from .dominio import DatosNuevaSolicitud
else:
    from dominio import DatosNuevaSolicitud


class Consola:

    def __init__(self, sistema):
        self.sistema = sistema

    def ejecutar(self):
        while True:
            print('\nSISTEMA DE GESTIÓN DE SOLICITUDES ACADÉMICAS')
            print('1. Registrar solicitud')
            print('2. Asignar responsable')
            print('3. Cambiar estado')
            print('4. Consultar solicitudes')
            print('5. Generar reporte')
            print('6. Ver estudiantes y responsables')
            print('0. Salir')
            opcion = input('Seleccione una opción: ').strip()
            try:
                if opcion == '1':
                    self._registrar()
                elif opcion == '2':
                    self._asignar()
                elif opcion == '3':
                    self._cambiar_estado()
                elif opcion == '4':
                    self._consultar()
                elif opcion == '5':
                    self._mostrar_reporte()
                elif opcion == '6':
                    self._mostrar_catalogos()
                elif opcion == '0':
                    print('Programa finalizado.')
                    break
                else:
                    print('La opción ingresada no es válida.')
            except ValueError as error:
                print(f'No se pudo completar la operación: {error}')
            except OSError as error:
                print(f'No se pudo acceder al archivo de datos: {error}')

    def _registrar(self):
        estudiante_id = input('ID del estudiante: ').strip().upper()
        descripcion = input('Descripción: ')
        print('Tipos: Certificado / Inscripción / Consulta')
        tipo = input('Tipo: ').strip()
        print('Prioridades: Baja / Media / Alta')
        prioridad = input('Prioridad: ').strip()
        nuevo_id = self.sistema.registrar_datos(DatosNuevaSolicitud(estudiante_id=estudiante_id, descripcion=descripcion, tipo=tipo, prioridad=prioridad))
        print(f'Solicitud registrada con ID {nuevo_id}.')

    def _asignar(self):
        solicitud_id = int(input('ID de la solicitud: '))
        responsable_id = input('ID del responsable: ').strip().upper()
        self.sistema.asignar(solicitud_id, responsable_id)
        print('Responsable asignado correctamente.')

    def _cambiar_estado(self):
        solicitud_id = int(input('ID de la solicitud: '))
        print('Estados: Pendiente / En atención / Resuelta / Cancelada')
        nuevo_estado = input('Nuevo estado: ').strip()
        self.sistema.cambiar_estado(solicitud_id, nuevo_estado)
        print('Estado actualizado correctamente.')

    def _consultar(self):
        print('Deje los campos vacíos para no aplicar ese filtro.')
        texto_id = input('ID de solicitud: ').strip()
        solicitud_id = int(texto_id) if texto_id else None
        estado = input('Estado: ').strip()
        tipo = input('Tipo: ').strip()
        prioridad = input('Prioridad: ').strip()
        resultados = self.sistema.consultar(solicitud_id, estado, tipo, prioridad)
        if not resultados:
            print('No se encontraron solicitudes.')
        for solicitud in resultados:
            print(f"\nID: {solicitud['id']}\nEstudiante: {solicitud['estudiante_id']}\nDescripción: {solicitud['descripcion']}\nTipo: {solicitud['tipo']}\nPrioridad: {solicitud['prioridad']}\nEstado: {solicitud['estado']}\nResponsable: {solicitud['responsable_id'] or 'Sin asignar'}")

    def _mostrar_reporte(self):
        reporte = self.sistema.reporte()
        print(f"\nTotal de solicitudes: {reporte['total']}")
        print('\nPor estado:')
        for estado, cantidad in reporte['por_estado'].items():
            print(f'  {estado}: {cantidad}')
        print('\nPor prioridad:')
        for prioridad, cantidad in reporte['por_prioridad'].items():
            print(f'  {prioridad}: {cantidad}')

    def _mostrar_catalogos(self):
        print('\nEstudiantes:')
        for estudiante in self.sistema.datos['estudiantes']:
            print(f"{estudiante['id']} - {estudiante['nombre']} - Legajo: {estudiante['legajo']}")
        print('\nResponsables:')
        for responsable in self.sistema.datos['responsables']:
            print(f"{responsable['id']} - {responsable['nombre']} - Área: {responsable['area']}")
