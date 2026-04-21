from typing import Generator, Optional
from src.config import FileConfig

class DatProcessor:
    """Procesador de alto rendimiento para archivos de ancho fijo (.dat)."""
    
    def __init__(self, config: FileConfig):
        self.config = config


    def stream_lines(self) -> Generator[str, None, None]:
        """Lee el archivo línea por línea sin cargar nada en RAM."""
        try:
            with open(self.config.file_path, mode='r', encoding=self.config.encoding) as file:
                for line in file:
                    yield line 
        except Exception as e:
            print(f"❌ Error al abrir el archivo: {e}")

  
    # def find_by_BIN(self, BIN_target: str) -> Optional[str]:
    #     """
    #     Busca un registro basándose en el IBT (caracteres 1 al 9).
    #     Aplica padding automático de ceros a la izquierda para la búsqueda.
    #     """
       
    #     BIN_normalized = BIN_target.strip().zfill(9)
        
    #     print(f"\n🔍 Buscando IBT: '{BIN_normalized}' (Original: '{BIN_target}')")

    #     for line in self.stream_lines():
           
    #         BIN_in_file = line[0:9]

    #         if BIN_in_file == BIN_normalized:
    #             return line[747:758]
        
    #     return None
    
    def count_items(self):
        """
        Busca cuantos ~{< existen en una linea y la posicion de cada uno.
        """
        contador = 0

        for line in self.stream_lines():
               
            indices = [i for i,car in enumerate(line) if car == "~"]
            caracteres = ""
            campos = []

            for posicion in indices:
                caracteres = f"{line[posicion]}{line[posicion+1]}{line[posicion+2]}"

                if(caracteres == "~{<"):
                    campos.append({posicion,posicion+2})

            return campos
    
        return None