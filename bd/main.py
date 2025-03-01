from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from database_mysql import create_connection

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Función para insertar contacto en MySQL
def insert_usuario(nombre: str, cargo: str, email: str) -> int:
    conn = create_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuario (nombre, cargo, email)
            VALUES (%s, %s, %s)
        ''', (nombre, cargo, email))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")
    finally:
        cursor.close()
        conn.close()