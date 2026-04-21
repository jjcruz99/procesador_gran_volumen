from pathlib import Path
from dataclasses import dataclass

@dataclass
class FileConfig:
    """Configuración centralizada para el procesamiento de archivos."""
    file_path: Path
    delimiter: str = "~{<"
    encoding: str = "latin-1"
    
    def validate_file(self) -> bool:
        return self.file_path.exists() and self.file_path.is_file()