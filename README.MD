
```
procesador_gran_volumen/
│
├── main.py                     # Punto de entrada principal (Orquestador)
│
├── config/
│   ├── __init__.py
│   ├── settings.py             # Configuraciones globales (rutas base, variables de entorno)
│   └── layouts.py              
│
├── src/
│   ├── __init__.py
│   │
│   ├── models/                 # Clases de Dominio (POO)
│   │   ├── __init__.py
│   │   └── record_model.py     # Clase genérica que representa un registro en memoria
│   │
│   ├── database/               # Capa de Acceso a Datos (I/O)
│   │   ├── __init__.py
│   │   ├── file_manager.py     
│   │   └── file_dao.py        
│   │
│   ├── gui/                    # (Reservado para la interfaz)
│   │   ├── __init__.py
│   │   └── main_window.py      
│   │
│   ├── services/               # Lógica de Negocio
│   │   ├── __init__.py
│   │   ├── parser_service.py   # Lógica para cortar la línea según las posiciones (layouts)
│   │   └── search_service.py   # Lógica para aplicar los filtros (ibt, afinidad, oficina, etc.)
│   │
│   └── utils/
│       ├── __init__.py
│       └── logger_config.py    # Para monitorear el procesamiento en consola/archivo
│
├── tests/
│   ├── __init__.py
│   └── test_parser.py          # Pruebas unitarias para asegurar que los recortes son exactos
│
├── requirements.txt
└── README.md
```