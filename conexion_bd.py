import mysql.connector
from datetime import date
from typing import List, Dict

class InventarioDB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="tu_usuario",
            password="tu_password",
            database="inventario_documental"
        )
        self.cursor = self.connection.cursor(dictionary=True)
        self.crear_tablas()

    def crear_tablas(self):
        tablas = [
            """
            CREATE TABLE IF NOT EXISTS sede (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS unidad_administrativa (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS oficina_productora (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS inventario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sede_id INT,
                unidad_administrativa_id INT,
                oficina_productora_id INT,
                fecha_registro DATE,
                nut VARCHAR(50),
                objeto TEXT,
                hoja_numero INT,
                FOREIGN KEY (sede_id) REFERENCES sede(id),
                FOREIGN KEY (unidad_administrativa_id) REFERENCES unidad_administrativa(id),
                FOREIGN KEY (oficina_productora_id) REFERENCES oficina_productora(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS registro_item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                inventario_id INT,
                numero_item INT,
                codigo VARCHAR(50),
                nombre_serie TEXT,
                fecha_inicio DATE,
                fecha_final DATE,
                caja VARCHAR(50),
                carpeta VARCHAR(50),
                tomo VARCHAR(50),
                otro VARCHAR(50),
                folio_del INT,
                folio_al INT,
                soporte VARCHAR(255),
                frecuencia_consulta ENUM('Alta', 'Media', 'Baja', 'Ninguna'),
                notas TEXT,
                FOREIGN KEY (inventario_id) REFERENCES inventario(id)
            )
            """
        ]
        
        for tabla in tablas:
            self.cursor.execute(tabla)
        self.connection.commit()

    def crear_inventario(self, datos: Dict):
        try:
            # Insertar inventario
            sql = """
            INSERT INTO inventario (sede_id, unidad_administrativa_id, oficina_productora_id,
            fecha_registro, nut, objeto, hoja_numero)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                datos['sede_id'],
                datos['unidad_administrativa_id'],
                datos['oficina_productora_id'],
                date.today(),
                datos['nut'],
                datos['objeto'],
                datos['hoja_numero']
            )
            
            self.cursor.execute(sql, valores)
            inventario_id = self.cursor.lastrowid

            # Insertar items
            for item in datos['items']:
                sql = """
                INSERT INTO registro_item (inventario_id, numero_item, codigo, nombre_serie,
                fecha_inicio, fecha_final, caja, carpeta, tomo, otro, folio_del, folio_al,
                soporte, frecuencia_consulta, notas)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    inventario_id,
                    item['numero_item'],
                    item['codigo'],
                    item['nombre_serie'],
                    item['fecha_inicio'],
                    item['fecha_final'],
                    item['caja'],
                    item['carpeta'],
                    item['tomo'],
                    item['otro'],
                    item['folio_del'],
                    item['folio_al'],
                    item['soporte'],
                    item['frecuencia_consulta'],
                    item['notas']
                )
                self.cursor.execute(sql, valores)

            self.connection.commit()
            return inventario_id
        
        except mysql.connector.Error as error:
            self.connection.rollback()
            raise Exception(f"Error al crear inventario: {error}")

    def obtener_inventario(self, inventario_id: int) -> Dict:
        sql = "SELECT * FROM inventario WHERE id = %s"
        self.cursor.execute(sql, (inventario_id,))
        inventario = self.cursor.fetchone()
        
        if inventario:
            sql = "SELECT * FROM registro_item WHERE inventario_id = %s"
            self.cursor.execute(sql, (inventario_id,))
            items = self.cursor.fetchall()
            inventario['items'] = items
            
        return inventario

    def __del__(self):
        self.cursor.close()
        self.connection.close()