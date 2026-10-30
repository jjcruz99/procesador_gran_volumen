import itertools
from typing import Optional, List, Dict
from src.database.file_dao import FileDAO
from config.layouts import ARCHIVO_MAE

class StructureService:
    """Lógica de negocio para procesar y buscar dentro de los registros."""

    def __init__(self, dao: FileDAO):
        self.dao = dao


    def get_field_coordinates(self,line:str) -> List[Dict[int, int]]:
        """Analiza la estructura de separadores ~{< en la primera línea."""

        if not line:
            return []

        campos = []
       
        start = 0
        while True:
            start = line.find(ARCHIVO_MAE['delimiter'], start)
            if start == -1: break
            
            campos.append({"inicio": start, "fin": start + 2})
            start += len(ARCHIVO_MAE['delimiter'])
            
        return campos
        

    def analizador_estructura(self, linea_objetivo: int ) -> List[Dict]:
        """
        Salta hasta la 'linea_objetivo' y analiza su estructura.
        Por defecto toma la línea 2 (donde suelen venir las longitudes).
        """
        stream = self.dao.get_stream()
        
        target_line = next(itertools.islice(stream, linea_objetivo - 1, linea_objetivo), None)

        if not target_line:
            print(f"⚠️ No se encontró la línea {linea_objetivo} en el archivo.")
            return []

        line = target_line.strip()
        delimiters = self.get_field_coordinates(line)
        estructura = []
        puntero_inicio = 0

        
        for i, delim in enumerate(delimiters):
            dato = line[puntero_inicio : delim["inicio"]]
            estructura.append({
                "campo": f"{i+1}".zfill(3),
                "dato": dato,
                "longitud": len(dato)
            })
            puntero_inicio = delim["fin"] + 1

        
        ultimo_dato = line[puntero_inicio:]
        estructura.append({
            "campo": f"{len(delimiters)+1}".zfill(3),
            "dato": ultimo_dato,
            "longitud": len(ultimo_dato)
        })

        return estructura


    def analizador_linea_a_linea(self):

        """
        Valida que todos los registros tengan la misma cantidad de campos
        que la primera línea del archivo.

        Retorna únicamente los registros con inconsistencias.
        """

        stream = self.dao.get_stream()
        delimiter = ARCHIVO_MAE["delimiter"]

        primera_linea = next(stream, None)

        if not primera_linea:
            return {
                "total_registros": 0,
                "errores": []
            }

        delimitadores_esperados = primera_linea.count(delimiter)

        total = 1
        errores = []

        for numero_registro, linea in enumerate(stream, start=2):

            total += 1

            delimitadores_actuales = linea.count(delimiter)

            if delimitadores_actuales != delimitadores_esperados:

                errores.append({
                    "registro": numero_registro,
                    "campos": delimitadores_actuales + 1
                })

        return {
            "total_registros": total,
            "campos_esperados": delimitadores_esperados + 1,
            "total_errores": len(errores),
            "errores": errores
        }
            


   