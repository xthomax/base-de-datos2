"""

Módulo de acceso a datos para el Sistema de Gestión de Biblioteca Combarranquilla.

Usa SQLite (incluido en la librería estándar de Python, no requiere instalación aparte).

"""

import sqlite3

import os

from datetime import datetime


 

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "biblioteca.db")



 

def get_connection():

    """Devuelve una nueva conexión a la base de datos con claves foráneas activas."""

    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = ON")

    conn.row_factory = sqlite3.Row

    return conn



 

def log_auditoria(tabla, operacion, id_registro, descripcion):

    """Registra una operación (INSERT/UPDATE/DELETE) en la tabla de auditoría."""

    conn = get_connection()

    cur = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(

        "INSERT INTO auditoria (tabla, operacion, id_registro, fecha, descripcion) VALUES (?,?,?,?,?)",

        (tabla, operacion, id_registro, fecha, descripcion),

    )

    conn.commit()

    conn.close()



 

def init_db():

    """Crea las tablas si no existen y siembra datos de ejemplo la primera vez."""

    fresh = not os.path.exists(DB_PATH)

    conn = get_connection()

    cur = conn.cursor()


 

    cur.executescript(

        """

        CREATE TABLE IF NOT EXISTS sistema_usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        );


 

        CREATE TABLE IF NOT EXISTS categorias (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT UNIQUE NOT NULL

        );


 

        CREATE TABLE IF NOT EXISTS editoriales (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT UNIQUE NOT NULL

        );


 

        CREATE TABLE IF NOT EXISTS autores (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            nacionalidad TEXT

        );


 

        CREATE TABLE IF NOT EXISTS usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombres TEXT NOT NULL,

            apellidos TEXT NOT NULL,

            documento TEXT UNIQUE NOT NULL,

            telefono TEXT,

            correo TEXT,

            direccion TEXT,

            fecha_registro TEXT

        );


 

        CREATE TABLE IF NOT EXISTS libros (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            titulo TEXT NOT NULL,

            isbn TEXT UNIQUE,

            anio_publicacion TEXT,

            autor_id INTEGER,

            editorial_id INTEGER,

            categoria_id INTEGER,

            FOREIGN KEY (autor_id) REFERENCES autores(id),

            FOREIGN KEY (editorial_id) REFERENCES editoriales(id),

            FOREIGN KEY (categoria_id) REFERENCES categorias(id)

        );


 

        CREATE TABLE IF NOT EXISTS prestamos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            usuario_id INTEGER NOT NULL,

            fecha_prestamo TEXT,

            fecha_devolucion TEXT,

            estado TEXT DEFAULT 'PRESTADO',

            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)

        );


 

        CREATE TABLE IF NOT EXISTS prestamo_libros (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            prestamo_id INTEGER NOT NULL,

            libro_id INTEGER NOT NULL,

            cantidad INTEGER DEFAULT 1,

            FOREIGN KEY (prestamo_id) REFERENCES prestamos(id) ON DELETE CASCADE,

            FOREIGN KEY (libro_id) REFERENCES libros(id)

        );


 

        CREATE TABLE IF NOT EXISTS auditoria (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tabla TEXT,

            operacion TEXT,

            id_registro INTEGER,

            fecha TEXT,

            descripcion TEXT

        );

        """

    )

    conn.commit()


 

    if fresh:

        seed_data(conn)


 

    conn.close()



 

def seed_data(conn):

    """Inserta datos de ejemplo similares a los del mockup, para que el sistema

    se pueda probar de inmediato con información realista."""

    cur = conn.cursor()


 

    cur.execute("INSERT INTO sistema_usuarios (usuario, password) VALUES ('admin','admin123')")


 

    categorias = ["Novela", "Clásicos", "Ciencia Ficción", "Historia", "Poesía", "Otros"]

    for c in categorias:

        cur.execute("INSERT INTO categorias (nombre) VALUES (?)", (c,))


 

    editoriales = ["Editorial Sudamericana", "Planeta", "Diana", "Espasa"]

    for e in editoriales:

        cur.execute("INSERT INTO editoriales (nombre) VALUES (?)", (e,))


 

    autores = [

        ("Gabriel García Márquez", "Colombiana"),

        ("Mario Vargas Llosa", "Peruana"),

        ("Isabel Allende", "Chilena"),

        ("Julio Cortázar", "Argentina"),

        ("Pablo Neruda", "Chilena"),

        ("Miguel de Cervantes", "Española"),

        ("Carlos Ruiz Zafón", "Española"),

    ]

    for n, nac in autores:

        cur.execute("INSERT INTO autores (nombre, nacionalidad) VALUES (?,?)", (n, nac))


 

    hoy = datetime.now().strftime("%Y-%m-%d")

    usuarios = [

        ("Juan Carlos", "Pérez Ramírez", "123456789", "3001234567", "juan.perez@gmail.com", "Barranquilla, Atlántico"),

        ("María Fernanda", "Gómez López", "987654321", "3012345678", "maria.gomez@gmail.com", "Barranquilla, Atlántico"),

        ("Luis Alberto", "Martínez Díaz", "112233445", "3023456789", "luis.martinez@gmail.com", "Cartagena, Bolívar"),

        ("Ana Sofía", "Torres Castro", "556677889", "3034567890", "ana.torres@gmail.com", "Barranquilla, Atlántico"),

        ("Pedro Miguel", "Rodríguez Silva", "998877665", "3045678901", "pedro.rodriguez@gmail.com", "Soledad, Atlántico"),

    ]

    for nom, ape, doc, tel, cor, dire in usuarios:

        cur.execute(

            """INSERT INTO usuarios (nombres, apellidos, documento, telefono, correo, direccion, fecha_registro)

               VALUES (?,?,?,?,?,?,?)""",

            (nom, ape, doc, tel, cor, dire, hoy),

        )


 

    libros = [

        ("Cien años de soledad", "9780307474728", "1967", 1, 1, 1),

        ("El amor en los tiempos del cólera", "9788497592208", "1985", 1, 3, 1),

        ("La ciudad y los perros", "9788432217145", "1963", 2, 2, 1),

        ("Don Quijote de la Mancha", "9788467033402", "1605", 6, 4, 2),

        ("La sombra del viento", "9788408043645", "2001", 7, 2, 1),

    ]

    for t, isbn, anio, aut, edi, cat in libros:

        cur.execute(

            """INSERT INTO libros (titulo, isbn, anio_publicacion, autor_id, editorial_id, categoria_id)

               VALUES (?,?,?,?,?,?)""",

            (t, isbn, anio, aut, edi, cat),

        )


 

    conn.commit()


