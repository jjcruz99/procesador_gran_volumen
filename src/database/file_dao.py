from typing import Generator
from config.settings import FileConfig

class FileDAO:
    """Data Access Object: Responsable puro de la lectura física del archivo."""
    def __init__(self, config: FileConfig):
        self.config = config


    def get_stream(self) -> Generator[str, None, None]:
        """Generador de alto rendimiento para archivos pesados."""
        try:
            with open(self.config.file_path, mode='r', encoding=self.config.encoding) as file:
                for line in file:
                    yield line
        except Exception as e:
            print(f"❌ Error crítico de I/O: {e}")