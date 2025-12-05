import sqlite3

DB_PATH = "database.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #==================================================
    # TABLA DE USUARIOS
    #==================================================
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS usuarios (
                   user_id INTEGER PRIMARY KEY,
                   nombre TEXT,
                   registrado_en TEXT)
                  """)

    #==================================================
    # TABLA DE DESAFIOS 
    #==================================================

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS desafios (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT NOT NULL,
                   descripcion TEXT NOT NULL,
                   fecha_inicio TEXT NOT NULL,
                   fecha_fin TEXT NOT NULL
                   )
                """)
    
    #==================================================
    # TABLA DE USUARIOS QUE COMPLETARON LOS DESAFIOS
    #==================================================

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS desafios_usuarios (
                   user_id INTEGER,
                   desafio_id INTEGER,
                   completado INTEGER DEFAULT 0,
                   PRIMARY KEY (user_id, desafio_id)
                   )
                """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS huella (
            user_id INTEGER PRIMARY KEY,
            transporte_km REAL DEFAULT 0,
            electricidad_kwh REAL DEFAULT 0,
            carne_kg REAL DEFAULT 0,
            residuos_kg REAL DEFAULT 0,
            updated_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()