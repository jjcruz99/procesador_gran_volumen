from typing import Optional, List, Dict
from src.database.file_dao import FileDAO
from config.layouts import ARCHIVO_MAE

class SearchService:
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
        

    def buscar_registros(self, 
                            bin_val: Optional[str] = None, 
                            afinidad: Optional[str] = None, 
                            estado: Optional[str] = None) -> List[Dict]:
            """
            Método principal que filtra el archivo por múltiples criterios.
            Retorna una lista con los registros que coincidan con TODO lo enviado.
            """
            resultados = []
                        
            bin_target = bin_val.strip().zfill(9) if bin_val else None
            afi_target = afinidad.strip().zfill(5) if afinidad else None
            est_target = estado.strip() if estado else None
            
            print("\n")
            print(f" 🚀 Iniciando escaneo de gran volumen ".center(100,"*"))

            for line in self.dao.get_stream():

                
                space_delimiters = self.get_field_coordinates(line)
  
                val_bin = line[space_delimiters[0]['inicio']-ARCHIVO_MAE['campos']['BIN']: space_delimiters[0]['inicio']]
                val_tar = line[space_delimiters[0]['fin']+1 : space_delimiters[1]['inicio']]
                val_tipo = line[space_delimiters[2]['fin']+1 : space_delimiters[3]['inicio']]
                val_afi = line[space_delimiters[4]['fin']+1 : space_delimiters[5]['inicio']]
                val_grupo = line[space_delimiters[29]['fin']+1 : space_delimiters[30]['inicio']]
                val_est = line[space_delimiters[32]['fin']+1 : space_delimiters[33]['inicio']]
                val_fec = line[space_delimiters[44]['fin']+1 : space_delimiters[45]['inicio']]


                if bin_target and val_bin != bin_target:
                    continue
                
                if afi_target and val_afi != afi_target:
                    continue
                    
                if est_target and val_est != est_target:
                    continue

                resultados.append({
                    "bin": val_bin,
                    "tar": val_tar,
                    "tipo": val_tipo,
                    "afinidad": val_afi,
                    "estado": val_est,
                    "grupo": val_grupo,
                    "fecha":val_fec
                })

                
                if len(resultados) >= 30:
                    print("⚠️ Se alcanzó el límite de 30 resultados.")
                    break

            return resultados