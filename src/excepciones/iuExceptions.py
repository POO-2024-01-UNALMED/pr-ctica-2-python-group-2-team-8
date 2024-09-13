class iuExceptions(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self._mensaje = mensaje
    
    def mostrarMensaje(self):
        return self._mensaje
    
    def _formatearCriterios(self, criterios):
        criteriosFormateados = ''

        for i in range (0,len(criterios)):
            if i < len(criterios) - 1:
                criteriosFormateados += ' ' + criterios[i].strip(':') + ','
            else:
                criteriosFormateados = criteriosFormateados[:-2]
                criteriosFormateados += ' y ' + criterios[i].strip(':')

        return criteriosFormateados
            
class iuDefaultValues(iuExceptions):
    def __init__(self, *criterios):
        super().__init__(self._crearMensaje(*criterios))
    
    def _crearMensaje(self, criterios):
        if len(criterios) == 1:

            return f'El campo {criterios[0].strip(':')} tiene un valor por defecto'
        
        elif len(criterios) > 1:

            criteriosFormateados = self._formatearCriterios(criterios)

            return f'Los campos:{criteriosFormateados} tienen valores por defecto'

class iuEmptyValues(iuExceptions):
    def __init__(self, *criterios):
        super().__init__(self._crearMensaje(*criterios))
    
    def _crearMensaje(self, criterios):
        if len(criterios) == 1:
            
            return f'El campo {criterios[0].strip(':')} está vacío'
        
        elif len(criterios) > 1:

            criteriosFormateados = self._formatearCriterios(criterios)

            return f'Los campos:{criteriosFormateados} tienen valores vacíos'

