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
                "campo": f"{i}".zfill(3),
                "dato": dato,
                "longitud": len(dato)
            })
            puntero_inicio = delim["fin"] + 1

        
        ultimo_dato = line[puntero_inicio:]
        estructura.append({
            "campo": f"{len(delimiters)}".zfill(3),
            "dato": ultimo_dato,
            "longitud": len(ultimo_dato)
        })

        return estructura


            


   