from pathlib import Path
from config.settings import FileConfig
from src.database.file_dao import FileDAO
from src.services.search_service import SearchService
from config.layouts import DATOS_PRUEBA
from src.services.structure_service import StructureService

def buscar_datos():
   
    path = Path(r"D:\JJ\Proyectos\procesador_gran_volumen\data\archivi.txt")
    config = FileConfig(file_path=path)
    
    if not config.validate_file():
        print("❌ Archivo no encontrado.")
        return

    
    dao = FileDAO(config)
    service = SearchService(dao)


    encontrados = service.buscar_registros(bin_val=DATOS_PRUEBA['BIN_4'],afinidad=DATOS_PRUEBA['afinidad3'],estado="N")

    #encontrados = service.buscar_registros(bin_val=DATOS_PRUEBA['BIN_1'],estado="O")


    if encontrados:
        print(f"✅ Se encontraron {len(encontrados)} registros coincidentes.")

        for i,reg in enumerate(encontrados):
            id= f"{i}".zfill(3)
            print(f"{id}: Iden:{reg["identificacion"]} - {reg['bin']} - {reg['tar']} - Estado:{reg['estado']} - Tipo:{reg['tipo']} - Afi:{reg['afinidad']} - Grupo:{reg['grupo']} - FV:{reg['fecha']}") 

    else:
        print("❌ Ningún registro cumple con todos los filtros.")


def validar_estructura():
    
    path2 = Path(r"D:\JJ\Proyectos\procesador_gran_volumen\data\archivi.txt")
    config2 = FileConfig(file_path=path2)
    
    if not config2.validate_file():
        print("❌ Archivo no encontrado.")
        return

    
    dao2 = FileDAO(config2)
    service2 = StructureService(dao2)
    num_fila = 96354
    campos = service2.analizador_estructura(linea_objetivo=num_fila)

    if campos:
        print("\n" + f" Se encontraron {len(campos)} delimitadores ".center(100,"*"))

        for campo in campos:
            print(f"{campo['campo']} = {campo['dato']}: {campo["longitud"]} Caracteres")


def validar_lina_a_linea():
    
    path3 = Path(r"D:\JJ\Proyectos\procesador_gran_volumen\data\archivi.txt")
    config3 = FileConfig(file_path=path3)
    
    if not config3.validate_file():
        print("❌ Archivo no encontrado.")
        return

    
    dao3 = FileDAO(config3)
    service3 = StructureService(dao3)
  
    resultado = service3.analizador_linea_a_linea()

    if resultado:
        print("\n" + f" Resultado de la validacion ".center(100,"*"))

    print(f"Total de registros : {resultado["total_registros"]}")
    print(f"Campos esperados : {resultado["campos_esperados"]} \n")
    print(f"❌ Errores encontrados : {resultado["total_errores"]}")

    for error in resultado["errores"]:
        print(
            f"linea: {error['registro']} "
            f"Cantidad de campos: {error['campos']}"
        )

    

if __name__ == "__main__":
    
    #buscar_datos()

    #validar_estructura()

    validar_lina_a_linea()

    print("\n")