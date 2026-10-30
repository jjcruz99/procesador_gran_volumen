from typing import Optional, List, Dict
from src.database.file_dao import FileDAO
from config.layouts import ARCHIVO_MAE
from datetime import datetime

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
                #print(f"Delimitadores encontrados{len(space_delimiters)}")
  
                val_bin = line[space_delimiters[0]['inicio']-ARCHIVO_MAE['campos']['BIN']: space_delimiters[0]['inicio']]
                val_tar = line[space_delimiters[0]['fin']+1 : space_delimiters[1]['inicio']]
                val_tipo = line[space_delimiters[2]['fin']+1 : space_delimiters[3]['inicio']]
                val_afi = line[space_delimiters[4]['fin']+1 : space_delimiters[5]['inicio']]
                val_grupo = line[space_delimiters[29]['fin']+1 : space_delimiters[30]['inicio']]
                val_est = line[space_delimiters[32]['fin']+1 : space_delimiters[33]['inicio']]
                val_fec = line[space_delimiters[44]['fin']+1 : space_delimiters[45]['inicio']]
                val_iden = line[space_delimiters[78]['fin']+1 : space_delimiters[79]['inicio']]

                

                if bin_target and val_bin != bin_target:
                    continue
                
                if afi_target and val_afi != afi_target:
                    continue
                    
                if est_target and val_est != est_target:
                    continue

                fecha1 = datetime.strptime(val_fec, "%Y%m%d")
                fecha2 = datetime.strptime( "20280501", "%Y%m%d")
             
                if fecha2 > fecha1:
                    continue

                resultados.append({
                    "bin": val_bin[1:9],
                    "tar": val_tar[7:16],
                    "tipo": val_tipo[1:3],
                    "afinidad": val_afi[3:5],
                    "estado": val_est,
                    "grupo": val_grupo[1:3],
                    "fecha":val_fec,
                    "identificacion":val_iden[0:13]
                })

                
                if len(resultados) >= 20:
                    print("⚠️ Se alcanzó el límite de 20 resultados.")
                    break

            return resultados