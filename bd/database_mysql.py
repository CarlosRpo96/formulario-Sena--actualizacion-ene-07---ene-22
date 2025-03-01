import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "root",      
    "password": "",
    "database": "formulario_inventario_documental"
}

def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None

# Crear tablas (ejecutar una vez)
def create_tables():
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        # Tabla usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                cargo VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla inventario_documental
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventario_documental (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT,
                sede VARCHAR(255) NOT NULL,
                unidad_administrativa VARCHAR(255) NOT NULL,
                año INT,
                mes INT,
                dia INT,
                nut INT,
                oficina_productora VARCHAR(255) NOT NULL,
                objeto TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuario(id)
            )
        ''')

        # Tabla items_inventario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items_inventario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                inventario_documental_id INT,
                codigo INT,
                nombre_serie TEXT,
                fecha_inicio DATE,
                fecha_final DATE,
                caja INT,
                carpeta INT,
                tomo INT,
                otro TEXT,
                folio_del INT,
                folio_al INT,
                soporte TEXT,
                frecuencia_consulta TEXT,
                notas TEXT,
                FOREIGN KEY (inventario_documental_id) REFERENCES inventario_documental(id)
            )
        ''')

        # Tabla firmas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS firmas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                inventario_id INT,
                nombre_elaborador VARCHAR(255),
                cargo_elaborador VARCHAR(255),
                nombre_entregador VARCHAR(255),
                cargo_entregador VARCHAR(255),
                nombre_receptor VARCHAR(255),
                cargo_receptor VARCHAR(255),
                fecha_elaboracion DATE,
                fecha_entrega DATE,
                fecha_recepcion DATE,
                FOREIGN KEY (inventario_id) REFERENCES inventarios(id)
            )
        ''')

        print("Tablas creadas exitosamente!")
    except Error as e:
        print(f"Error creando tablas: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()