from pathlib import Path
from config.settings import FileConfig
from src.database.file_dao import FileDAO
from src.services.search_service import SearchService
from config.layouts import DATOS_PRUEBA
from src.services.structure_service import StructureService

def buscar_datos():
   
    path = Path(r"D:\JJ\Proyectos\procesador_gran_volumen\data\CRMAE_20260411_020349_20260331.DAT")
    config = FileConfig(file_path=path)
    
    if not config.validate_file():
        print("❌ Archivo no encontrado.")
        return

    
    dao = FileDAO(config)
    service = SearchService(dao)


    encontrados = service.buscar_registros(bin_val=DATOS_PRUEBA['BIN_1'],afinidad=DATOS_PRUEBA['afinidad1'],estado="N")

    if encontrados:
        print(f"✅ Se encontraron {len(encontrados)} registros coincidentes.")

        for i,reg in enumerate(encontrados):
            id= f"{i}".zfill(3)
            print(f"{id}: {reg['bin']} - {reg['tar']} - Estado:{reg['estado']} - Tipo:{reg['tipo']} - Afi:{reg['afinidad']} - Grupo:{reg['grupo']} - FV:{reg['fecha']}") 

    else:
        print("❌ Ningún registro cumple con todos los filtros.")


def validar_estructura():
    #prueba de estructura 
    path2 = Path(r"D:\JJ\Proyectos\procesador_gran_volumen\data\CLCIU_20260420_230537_20260501.DAT")
    config2 = FileConfig(file_path=path2)
    
    if not config2.validate_file():
        print("❌ Archivo no encontrado.")
        return

    
    dao2 = FileDAO(config2)
    service2 = StructureService(dao2)
    num_fila = 3
    campos = service2.analizador_estructura(linea_objetivo=num_fila)

    if campos:
        print("\n" + f" Se encontraron {len(campos)} delimitadores ".center(100,"*"))

        for campo in campos:
            print(f"{campo['campo']} = {campo['dato']}: {campo["longitud"]} Caracteres")



if __name__ == "__main__":
    
    buscar_datos()

    #validar_estructura()