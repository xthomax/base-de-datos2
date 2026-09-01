from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import os
from pathlib import Path
from PIL import Image, ImageTk

#RUTA DEL PROYECTO
BASE_DIR=Path(__file__).resolve().parent
RUTA_BBDD=BASE_DIR/"BaseUsuariosTMHM.db"
RUTA_ICONO=BASE_DIR/"interface_grafica.ico"
RUTA_IMAGEN_FONDO=BASE_DIR/"fondo_usuario.jpeg"

# ==========================================
# CONFIGURACIÓN DE LA VENTANA
# ==========================================

raiz = Tk()
raiz.title("Sistema de Gestión de Usuarios")
raiz.geometry("1150x750")
raiz.resizable(True, True)

# ==========================================
# COLORES - CAMBIA ESTOS HEX CODES
# ==========================================
COLOR_FONDO_VENTANA = "#2C3E50"        # Color de fondo de la ventana principal
COLOR_FONDO_FRAME = "#011E25"          # Color de fondo del formulario (el "body")
COLOR_TEXTO_FRAME = "#FFFFFF"          # Color de texto para todos los labels
COLOR_TEXTO_TITULO = "#D2D8DD"         # Color del texto del título
COLOR_FONDO_MENU = "#34495E"           # Color de fondo del menú
COLOR_TEXTO_MENU = "#0FA4CA"           # Color del texto del menú
COLOR_MENU_ACTIVO = "#1ABC9C"          # Color cuando el mouse pasa sobre el menú
COLOR_TEXTO_MENU_ACTIVO = "#FFFFFF"    # Color del texto del menú al pasar el mouse
COLOR_BOTON_INSERTAR = "#27AE60"       # Color del botón Insertar
COLOR_BOTON_ACTUALIZAR = "#F39C12"     # Color del botón Actualizar
COLOR_BOTON_ELIMINAR = "#E74C3C"       # Color del botón Eliminar
COLOR_BOTON_LIMPIAR = "#34495E"        # Color del botón Limpiar
COLOR_BOTON_SALIR = "#7F8C8D"          # Color del botón Salir
COLOR_BOTON_BUSCAR = "#2980B9"         # Color del botón Buscar
COLOR_BOTON_MOSTRAR = "#16A085"        # Color del botón Mostrar Todos
COLOR_FONDO_COMBOBOX = "#1A3A45"       # Color de fondo del combobox
COLOR_SELECCION_COMBOBOX = "#406B76"   # Color de selección en el dropdown

# ==========================================
# CONFIGURAR COLOR DE FONDO DE LA VENTANA
# ==========================================
raiz.configure(bg=COLOR_FONDO_VENTANA)

#ICONO DE LA VENTANA
if RUTA_ICONO.exists():
    try:
        raiz.iconbitmap(str(RUTA_ICONO))
    except Exception as e:
        print("No se pudo cargar el icono: ",e)
else:
    print("Advertencia: no se encontro el icono:")
    print(RUTA_ICONO)

# ==========================================
# CREAR MENÚ CON COLORES
# ==========================================

# Crear la barra de menú principal
barra_menu = Menu(raiz, bg=COLOR_FONDO_MENU, fg=COLOR_TEXTO_MENU)
raiz.config(menu=barra_menu)

# Crear el menú "BBDD" con colores
menu_bbdd = Menu(
    barra_menu, 
    tearoff=0, 
    bg=COLOR_FONDO_MENU, 
    fg=COLOR_TEXTO_MENU,
    activebackground=COLOR_MENU_ACTIVO,
    activeforeground=COLOR_TEXTO_MENU_ACTIVO
)
barra_menu.add_cascade(label="BBDD", menu=menu_bbdd)

# MENU AYUDA
menu_ayuda = Menu(
    barra_menu,
    tearoff=0,
    bg=COLOR_FONDO_MENU, 
    fg=COLOR_TEXTO_MENU,
    activebackground=COLOR_MENU_ACTIVO,
    activeforeground=COLOR_TEXTO_MENU_ACTIVO
)
menu_ayuda.add_command(
    label="Acerca de",
    command=lambda: messagebox.showinfo(
        "Acerca de",
        "Proyecto Unificado 1\n"
        "CRUD con Tkinter y SQLite\n"
        "Desarrollado en Python\n"
        "CREADO POR: Thomas Mendoza y Harold Morales\n"
    )
)
barra_menu.add_cascade(
    label="Ayuda",
    menu=menu_ayuda
)

# Función para conectar a la base de datos
def conectar_bbdd():
    try:
        conexion = sqlite3.connect(str(RUTA_BBDD))
        conexion.close()
        messagebox.showinfo(
            "Conexión",
            f"Conexión a la base de datos establecida correctamente.\n{RUTA_BBDD}"
        )
    except Exception as e:
        messagebox.showerror(
            "Error de conexión",
            f"No se pudo conectar a la base de datos:\n{e}"
        )

# Función para salir
def salir_aplicacion():
    respuesta = messagebox.askyesno(
        "Salir",
        "¿Está seguro de que desea salir de la aplicación?"
    )
    if respuesta:
        raiz.destroy()

# Agregar opciones al menú BBDD
menu_bbdd.add_command(label="Conectar", command=conectar_bbdd)
menu_bbdd.add_separator()
menu_bbdd.add_command(label="Salir", command=salir_aplicacion)

# ==========================================
# CONFIGURAR ESTILO DE LOS COMBOBOX
# ==========================================

style = ttk.Style()
style.theme_use("clam")

# Configurar el estilo del combobox
style.configure("Custom.TCombobox",
                fieldbackground=COLOR_FONDO_COMBOBOX,
                background=COLOR_FONDO_COMBOBOX,
                foreground=COLOR_TEXTO_FRAME,
                arrowcolor=COLOR_TEXTO_FRAME,
                selectbackground=COLOR_SELECCION_COMBOBOX,
                selectforeground=COLOR_TEXTO_FRAME,
                bordercolor=COLOR_FONDO_COMBOBOX,
                lightcolor=COLOR_FONDO_COMBOBOX,
                darkcolor=COLOR_FONDO_COMBOBOX)

style.map("Custom.TCombobox",
          fieldbackground=[("readonly", COLOR_FONDO_COMBOBOX)],
          background=[("readonly", COLOR_FONDO_COMBOBOX)],
          foreground=[("readonly", COLOR_TEXTO_FRAME)])

style.configure("Custom.TCombobox.popdown",
                background=COLOR_FONDO_COMBOBOX,
                foreground=COLOR_TEXTO_FRAME)

style.configure("Custom.TCombobox.Listbox",
                background=COLOR_FONDO_COMBOBOX,
                foreground=COLOR_TEXTO_FRAME,
                selectbackground=COLOR_SELECCION_COMBOBOX,
                selectforeground=COLOR_TEXTO_FRAME,
                borderwidth=0,
                relief="flat")

# ==========================================
# CONFIGURACIÓN DE IMÁGENES
# ==========================================
TAMANO_IMAGEN_USUARIO = (300, 300)  # Cambia el tamaño de la imagen aquí

# ==========================================
# VARIABLES
# ==========================================

id_seleccionado = StringVar()

nombre = StringVar()
contraseña = StringVar()
apellido = StringVar()
direccion = StringVar()
ciudad = StringVar()
codigo_postal = StringVar()
correo = StringVar()
comentarios = StringVar()

genero = StringVar(value="Masculino")
estado = IntVar()
grupo_sanguineo = StringVar(value="Seleccione")

tipo_usuario = StringVar(value="Seleccione")

ruta_imagen = StringVar()
ruta_archivo = StringVar()

# ==========================================
# CONEXIÓN A BASE DE DATOS
# ==========================================

def conexion_bbdd():

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contraseña TEXT,
        apellido TEXT NOT NULL,
        direccion TEXT,
        ciudad TEXT,
        codigo_postal TEXT,
        correo TEXT,
        comentarios TEXT,
        genero TEXT,
        grupo_sanguineo TEXT,
        estado INTEGER,
        tipo_usuario TEXT,
        imagen TEXT,
        archivo TEXT
    )
    """)

    conexion.commit()
    conexion.close()


conexion_bbdd()

# ==========================================
# FUNCIÓN LIMPIAR - CORREGIDA
# ==========================================

def limpiar():

    id_seleccionado.set("")

    nombre.set("")
    contraseña.set("")
    apellido.set("")
    direccion.set("")
    ciudad.set("")
    codigo_postal.set("")
    correo.set("")
    comentarios.set("")

    genero.set("Masculino")
    estado.set(0)
    grupo_sanguineo.set("Seleccione")

    tipo_usuario.set("Seleccione")

    ruta_imagen.set("")
    ruta_archivo.set("")

    # Limpiar el campo de texto de comentarios
    texto_comentarios.delete(1.0, END)

    etiqueta_imagen.config(image="")
    etiqueta_imagen.image = None

    etiqueta_archivo.config(text="Archivo: No adjunto")

# ==========================================
# ADJUNTAR IMAGEN
# ==========================================

def seleccionar_imagen():

    archivo = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.gif"),
            ("Todos los archivos", "*.*")
        ]
    )

    if archivo:

        ruta_imagen.set(archivo)

        try:

            imagen = Image.open(archivo)
            
            imagen = imagen.resize(TAMANO_IMAGEN_USUARIO, Image.Resampling.LANCZOS)

            imagen_tk = ImageTk.PhotoImage(imagen)

            etiqueta_imagen.config(image=imagen_tk)

            etiqueta_imagen.image = imagen_tk

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo cargar la imagen:\n{error}"
            )

# ==========================================
# ADJUNTAR ARCHIVO
# ==========================================

def seleccionar_archivo():

    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[
            ("Documentos", "*.pdf *.docx *.xlsx *.txt"),
            ("Todos los archivos", "*.*")
        ]
    )

    if archivo:

        ruta_archivo.set(archivo)

        nombre_archivo = os.path.basename(archivo)

        etiqueta_archivo.config(
            text=f"Archivo: {nombre_archivo}"
        )

# ==========================================
# INSERTAR
# ==========================================

def insertar():

    if nombre.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el nombre."
        )
        return

    if contraseña.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar la contraseña."
        )
        return

    if apellido.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el apellido."
        )
        return

    if correo.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el correo electronico."
        )
        return

    if direccion.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar la direccion."
        )
        return

    if ciudad.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar la ciudad."
        )
        return

    if codigo_postal.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Debe ingresar el codigo postal."
        )
        return

    if grupo_sanguineo.get() == "Seleccione":
        messagebox.showwarning(
            "Advertencia",
            "Debe seleccionar el grupo sanguineo."
        )
        return

    if tipo_usuario.get() == "Seleccione":
        messagebox.showwarning(
            "Advertencia",
            "Debe seleccionar el tipo de usuario."
        )
        return

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            grupo_sanguineo,
            estado,
            tipo_usuario,
            imagen,
            archivo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        nombre.get(),
        contraseña.get(),
        apellido.get(),
        direccion.get(),
        ciudad.get(),
        codigo_postal.get(),
        correo.get(),
        comentarios.get(),
        genero.get(),
        grupo_sanguineo.get(),
        estado.get(),
        tipo_usuario.get(),
        ruta_imagen.get(),
        ruta_archivo.get()
    ))

    conexion.commit()
    conexion.close()

    messagebox.showinfo(
        "Registro",
        "Usuario registrado correctamente."
    )

    mostrar_datos()
    limpiar()


# ==========================================
# MOSTRAR DATOS
# ==========================================

def mostrar_datos():

    for elemento in tabla.get_children():
        tabla.delete(elemento)

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            grupo_sanguineo,
            estado,
            tipo_usuario,
            imagen,
            archivo
        FROM usuarios
        ORDER BY id DESC
    """)

    registros = cursor.fetchall()

    conexion.close()

    for registro in registros:

        estado_texto = "Activo" if registro[11] == 1 else "Inactivo"

        tabla.insert(
            "",
            END,
            values=(
                registro[0],
                registro[1],
                registro[3],
                registro[4],
                registro[5],
                registro[6],
                registro[9],
                registro[10],
                estado_texto,
                registro[12]
            )
        )


# ==========================================
# SELECCIONAR REGISTRO DEL TREEVIEW
# ==========================================

def seleccionar_registro(event):

    seleccionado = tabla.focus()

    if not seleccionado:
        return

    datos = tabla.item(seleccionado, "values")

    if not datos:
        return

    id_seleccionado.set(datos[0])

    # Cargar todos los campos desde la base de datos
    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT 
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            grupo_sanguineo,
            estado,
            tipo_usuario
        FROM usuarios
        WHERE id = ?
    """, (datos[0],))
    
    registro = cursor.fetchone()
    conexion.close()
    
    if registro:
        nombre.set(registro[0])
        contraseña.set(registro[1])
        apellido.set(registro[2])
        direccion.set(registro[3])
        ciudad.set(registro[4])
        codigo_postal.set(registro[5])
        correo.set(registro[6])
        comentarios.set(registro[7])
        genero.set(registro[8])
        grupo_sanguineo.set(registro[9])
        
        if registro[10] == 1:
            estado.set(1)
        else:
            estado.set(0)
        
        tipo_usuario.set(registro[11])

        # Cargar comentarios en el Text widget
        texto_comentarios.delete(1.0, END)
        texto_comentarios.insert(1.0, registro[7])

    cargar_archivos_registro(datos[0])


# ==========================================
# CARGAR IMAGEN Y ARCHIVO DEL REGISTRO
# ==========================================

def cargar_archivos_registro(id_usuario):

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT imagen, archivo
        FROM usuarios
        WHERE id = ?
    """, (id_usuario,))

    registro = cursor.fetchone()

    conexion.close()

    if not registro:
        return

    imagen = registro[0]
    archivo = registro[1]

    ruta_imagen.set(imagen if imagen else "")
    ruta_archivo.set(archivo if archivo else "")

    if archivo:
        etiqueta_archivo.config(
            text=f"Archivo: {os.path.basename(archivo)}"
        )
    else:
        etiqueta_archivo.config(
            text="Archivo: No adjunto"
        )

    if imagen and os.path.exists(imagen):

        try:

            img = Image.open(imagen)
            
            img = img.resize(TAMANO_IMAGEN_USUARIO, Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            etiqueta_imagen.config(image=img_tk)

            etiqueta_imagen.image = img_tk

        except:
            etiqueta_imagen.config(image="")
            etiqueta_imagen.image = None

    else:

        etiqueta_imagen.config(image="")
        etiqueta_imagen.image = None


# ==========================================
# ACTUALIZAR
# ==========================================

def actualizar():

    if id_seleccionado.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Seleccione primero un registro."
        )
        return

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET
            nombre = ?,
            contraseña = ?,
            apellido = ?,
            direccion = ?,
            ciudad = ?,
            codigo_postal = ?,
            correo = ?,
            comentarios = ?,
            genero = ?,
            grupo_sanguineo = ?,
            estado = ?,
            tipo_usuario = ?,
            imagen = ?,
            archivo = ?
        WHERE id = ?
    """, (
        nombre.get(),
        contraseña.get(),
        apellido.get(),
        direccion.get(),
        ciudad.get(),
        codigo_postal.get(),
        correo.get(),
        comentarios.get(),
        genero.get(),
        grupo_sanguineo.get(),
        estado.get(),
        tipo_usuario.get(),
        ruta_imagen.get(),
        ruta_archivo.get(),
        id_seleccionado.get()
    ))

    conexion.commit()
    conexion.close()

    messagebox.showinfo(
        "Actualizar",
        "Registro actualizado correctamente."
    )

    mostrar_datos()
    limpiar()


# ==========================================
# ELIMINAR
# ==========================================

def eliminar():

    if id_seleccionado.get() == "":
        messagebox.showwarning(
            "Advertencia",
            "Seleccione un registro."
        )
        return

    respuesta = messagebox.askyesno(
        "Eliminar",
        "¿Está seguro de eliminar este registro?"
    )

    if respuesta:

        conexion = sqlite3.connect(str(RUTA_BBDD))
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM usuarios
            WHERE id = ?
        """, (id_seleccionado.get(),))

        conexion.commit()
        conexion.close()

        messagebox.showinfo(
            "Eliminar",
            "Registro eliminado correctamente."
        )

        mostrar_datos()
        limpiar()


# ==========================================
# BUSCAR
# ==========================================

def buscar():

    texto = entrada_buscar.get()

    for elemento in tabla.get_children():
        tabla.delete(elemento)

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            contraseña,
            apellido,
            direccion,
            ciudad,
            codigo_postal,
            correo,
            comentarios,
            genero,
            grupo_sanguineo,
            estado,
            tipo_usuario
        FROM usuarios
        WHERE nombre LIKE ?
        OR apellido LIKE ?
        OR ciudad LIKE ?
        ORDER BY id DESC
    """, (
        "%" + texto + "%",
        "%" + texto + "%",
        "%" + texto + "%"
    ))

    registros = cursor.fetchall()

    conexion.close()

    for registro in registros:

        estado_texto = (
            "Activo"
            if registro[11] == 1
            else "Inactivo"
        )

        tabla.insert(
            "",
            END,
            values=(
                registro[0],
                registro[1],
                registro[3],
                registro[4],
                registro[5],
                registro[6],
                registro[9],
                registro[10],
                estado_texto,
                registro[12]
            )
        )


# ==========================================
# FRAME PRINCIPAL DEL FORMULARIO (EL "BODY")
# ==========================================

miFrame = Frame(
    raiz,
    bd=2,
    relief="groove",
    padx=10,
    pady=10,
    bg=COLOR_FONDO_FRAME
)

miFrame.pack(
    padx=10,
    pady=10,
    fill="x"
)

# ==========================================
# TÍTULO
# ==========================================

Label(
    miFrame,
    text="FORMULARIO DE REGISTRO DE USUARIOS",
    font=("Arial", 16, "bold"),
    fg=COLOR_TEXTO_TITULO,
    bg=COLOR_FONDO_FRAME
).grid(
    row=0,
    column=0,
    columnspan=5,
    pady=10
)

# ==========================================
# NOMBRE
# ==========================================

Label(
    miFrame,
    text="Nombre:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=nombre,
    width=25,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# APELLIDO
# ==========================================

Label(
    miFrame,
    text="Apellido:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=apellido,
    width=25,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
).grid(
    row=1,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# IMAGEN DECORATIVA EN COLUMNA 4
# ==========================================

# Cargar la imagen decorativa
imagen_decorativa = None
if RUTA_IMAGEN_FONDO.exists():
    try:
        img_deco = Image.open(str(RUTA_IMAGEN_FONDO))
        img_deco = img_deco.resize((280, 220), Image.Resampling.LANCZOS)
        imagen_decorativa = ImageTk.PhotoImage(img_deco)
    except Exception as e:
        print(f"No se pudo cargar la imagen decorativa: {e}")

# Crear label para la imagen decorativa
label_imagen_decorativa = Label(
    miFrame,
    image=imagen_decorativa if imagen_decorativa else "",
    relief="solid",
    bd=1,
    bg=COLOR_FONDO_FRAME
)
label_imagen_decorativa.grid(
    row=1,
    column=4,
    rowspan=11,
    padx=10,
    pady=5,
    sticky="n"
)

# Guardar referencia para evitar que se borre
label_imagen_decorativa.image = imagen_decorativa

# ==========================================
# CONTRASEÑA
# ==========================================

Label(
    miFrame,
    text="Contraseña:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=contraseña,
    width=25,
    show="*",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
).grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# CORREO
# ==========================================

Label(
    miFrame,
    text="Correo:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=2,
    column=2,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=correo,
    width=25,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
).grid(
    row=2,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# DIRECCIÓN
# ==========================================

Label(
    miFrame,
    text="Dirección:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=direccion,
    width=25,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
).grid(
    row=3,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# CIUDAD
# ==========================================

Label(
    miFrame,
    text="Ciudad:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=3,
    column=2,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=ciudad,
    width=25,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
).grid(
    row=3,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# CÓDIGO POSTAL
# ==========================================

Label(
    miFrame,
    text="Código Postal:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=4,
    column=0,
    padx=5,
    pady=5,
    sticky="e"
)

Entry(
    miFrame,
    textvariable=codigo_postal,
    width=25,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
).grid(
    row=4,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# RADIOBUTTON
# ==========================================

Label(
    miFrame,
    text="Género:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=4,
    column=2,
    padx=5,
    pady=5
)

Radiobutton(
    miFrame,
    text="Masculino",
    variable=genero,
    value="Masculino",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME,
    selectcolor=COLOR_FONDO_COMBOBOX
).grid(
    row=4,
    column=3,
    sticky="w"
)

Radiobutton(
    miFrame,
    text="Femenino",
    variable=genero,
    value="Femenino",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME,
    selectcolor=COLOR_FONDO_COMBOBOX
).grid(
    row=5,
    column=3,
    sticky="w"
)

# ==========================================
# CHECKBUTTON
# ==========================================

Checkbutton(
    miFrame,
    text="Usuario activo",
    variable=estado,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME,
    selectcolor=COLOR_FONDO_COMBOBOX
).grid(
    row=6,
    column=1,
    pady=5
)

# ==========================================
# GRUPO SANGUINEO (COMBOBOX CON ESTILO)
# ==========================================

Label(
    miFrame,
    text="Grupo Sanguíneo:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=6,
    column=2,
    padx=5,
    pady=5
)

combo_grupo = ttk.Combobox(
    miFrame,
    textvariable=grupo_sanguineo,
    values=[
        "A+",
        "A-",
        "B+",
        "B-",
        "AB+",
        "AB-",
        "O+",
        "O-"
    ],
    state="readonly",
    width=22,
    style="Custom.TCombobox"
)

combo_grupo.grid(
    row=6,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# COMBOBOX TIPO USUARIO (COMBOBOX CON ESTILO)
# ==========================================

Label(
    miFrame,
    text="Tipo de usuario:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=7,
    column=2,
    padx=5,
    pady=5
)

combo_tipo = ttk.Combobox(
    miFrame,
    textvariable=tipo_usuario,
    values=[
        "Administrador",
        "Docente",
        "Estudiante",
        "Invitado"
    ],
    state="readonly",
    width=22,
    style="Custom.TCombobox"
)

combo_tipo.grid(
    row=7,
    column=3,
    padx=5,
    pady=5
)

# ==========================================
# COMENTARIOS
# ==========================================

Label(
    miFrame,
    text="Comentarios:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=8,
    column=0,
    padx=5,
    pady=5,
    sticky="ne"
)

texto_comentarios = Text(
    miFrame,
    height=3,
    width=23,
    wrap=WORD,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
)

texto_comentarios.grid(
    row=8,
    column=1,
    padx=5,
    pady=5
)

# ==========================================
# IMAGEN
# ==========================================

Label(
    miFrame,
    text="Imagen:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
).grid(
    row=9,
    column=0,
    padx=5,
    pady=5
)

Button(
    miFrame,
    text="Seleccionar Imagen",
    command=seleccionar_imagen,
    bg="#3498DB",
    fg="white",
    width=20
).grid(
    row=9,
    column=1,
    padx=5,
    pady=5
)

etiqueta_imagen = Label(
    miFrame,
    relief="sunken",
    bg=COLOR_FONDO_COMBOBOX
)

etiqueta_imagen.grid(
    row=9,
    column=2,
    rowspan=3,
    padx=10,
    pady=5
)

# ==========================================
# ARCHIVO ADJUNTO
# ==========================================

Button(
    miFrame,
    text="📎 Adjuntar Archivo",
    command=seleccionar_archivo,
    bg="#9B59B6",
    fg="white",
    width=20
).grid(
    row=10,
    column=1,
    padx=5,
    pady=5
)

etiqueta_archivo = Label(
    miFrame,
    text="Archivo: No adjunto",
    width=30,
    anchor="w",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_FRAME
)

etiqueta_archivo.grid(
    row=11,
    column=0,
    columnspan=2,
    padx=5,
    pady=5
)

# ==========================================
# FRAME DE BOTONES
# ==========================================

frame_botones = Frame(
    raiz,
    bd=2,
    relief="groove",
    padx=10,
    pady=10,
    bg=COLOR_FONDO_FRAME
)

frame_botones.pack(
    padx=10,
    pady=5,
    fill="x"
)

# ==========================================
# BOTÓN INSERTAR
# ==========================================

Button(
    frame_botones,
    text="💾 INSERTAR",
    command=insertar,
    bg=COLOR_BOTON_INSERTAR,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTÓN ACTUALIZAR
# ==========================================

Button(
    frame_botones,
    text="♻️ ACTUALIZAR",
    command=actualizar,
    bg=COLOR_BOTON_ACTUALIZAR,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTÓN ELIMINAR
# ==========================================

Button(
    frame_botones,
    text="🗑️ ELIMINAR",
    command=eliminar,
    bg=COLOR_BOTON_ELIMINAR,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTON LIMPIAR
# ==========================================

Button(
    frame_botones,
    text="🧹 LIMPIAR",
    command=limpiar,
    bg=COLOR_BOTON_LIMPIAR,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BOTÓN SALIR
# ==========================================

Button(
    frame_botones,
    text="🚪 SALIR",
    command=raiz.destroy,
    bg=COLOR_BOTON_SALIR,
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# BUSCADOR
# ==========================================

frame_buscar = Frame(raiz, bg=COLOR_FONDO_VENTANA)
frame_buscar.pack(
    padx=10,
    pady=5,
    fill="x"
)

Label(
    frame_buscar,
    text="Buscar:",
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_VENTANA
).pack(
    side=LEFT,
    padx=5
)

entrada_buscar = Entry(
    frame_buscar,
    width=40,
    fg=COLOR_TEXTO_FRAME,
    bg=COLOR_FONDO_COMBOBOX
)

entrada_buscar.pack(
    side=LEFT,
    padx=5
)

Button(
    frame_buscar,
    text="🔍 BUSCAR",
    command=buscar,
    bg=COLOR_BOTON_BUSCAR,
    fg="white",
    width=15
).pack(
    side=LEFT,
    padx=5
)

Button(
    frame_buscar,
    text="MOSTRAR TODOS",
    command=mostrar_datos,
    bg=COLOR_BOTON_MOSTRAR,
    fg="white",
    width=15
).pack(
    side=LEFT,
    padx=5
)

# ==========================================
# FRAME DEL TREEVIEW
# ==========================================

frame_tabla = Frame(
    raiz,
    bd=2,
    relief="groove",
    bg=COLOR_FONDO_FRAME
)
frame_tabla.pack(
    padx=10,
    pady=5,
    fill="both",
    expand=True
)

# ==========================================
# SCROLLBAR VERTICAL
# ==========================================

scroll_vertical = Scrollbar(
    frame_tabla,
    orient=VERTICAL
)

scroll_vertical.pack(
    side=RIGHT,
    fill=Y
)

# ==========================================
# SCROLLBAR HORIZONTAL
# ==========================================

scroll_horizontal = Scrollbar(
    frame_tabla,
    orient=HORIZONTAL
)

scroll_horizontal.pack(
    side=BOTTOM,
    fill=X
)

# ==========================================
# TREEVIEW
# ==========================================

columnas = (
    "ID",
    "Nombre",
    "Apellido",
    "Dirección",
    "Ciudad",
    "Código Postal",
    "Género",
    "Grupo Sanguíneo",
    "Estado",
    "Tipo Usuario"
)

tabla = ttk.Treeview(
    frame_tabla,
    columns=columnas,
    show="headings",
    yscrollcommand=scroll_vertical.set,
    xscrollcommand=scroll_horizontal.set,
    height=10
)

# ==========================================
# CONFIGURAR COLUMNAS
# ==========================================

for columna in columnas:

    tabla.heading(
        columna,
        text=columna
    )

    tabla.column(
        columna,
        width=120,
        anchor="center"
    )

tabla.column("ID", width=50)
tabla.column("Nombre", width=120)
tabla.column("Apellido", width=120)
tabla.column("Dirección", width=180)
tabla.column("Ciudad", width=120)
tabla.column("Código Postal", width=100)
tabla.column("Género", width=100)
tabla.column("Grupo Sanguíneo", width=120)
tabla.column("Estado", width=100)
tabla.column("Tipo Usuario", width=130)

# Configurar colores del Treeview
style_treeview = ttk.Style()
style_treeview.theme_use("clam")
style_treeview.configure("Treeview", 
                background=COLOR_FONDO_COMBOBOX,
                foreground=COLOR_TEXTO_FRAME,
                fieldbackground=COLOR_FONDO_COMBOBOX)
style_treeview.configure("Treeview.Heading",
                background=COLOR_FONDO_MENU,
                foreground=COLOR_TEXTO_FRAME)

tabla.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)

# ==========================================
# CONECTAR SCROLLBAR
# ==========================================

scroll_vertical.config(
    command=tabla.yview
)

scroll_horizontal.config(
    command=tabla.xview
)

# ==========================================
# EVENTO TREEVIEW
# ==========================================

tabla.bind(
    "<ButtonRelease-1>",
    seleccionar_registro
)

# ==========================================
# CARGAR DATOS
# ==========================================

mostrar_datos()

# ==========================================
# EJECUTAR
# ==========================================

raiz.mainloop()