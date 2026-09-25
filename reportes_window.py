import tkinter as tk

from tkinter import messagebox, filedialog

from database import get_connection


 

try:

    from reportlab.lib.pagesizes import letter

    from reportlab.lib import colors

    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

    from reportlab.lib.styles import getSampleStyleSheet


 

    REPORTLAB_OK = True

except ImportError:

    REPORTLAB_OK = False


 

try:

    from openpyxl import Workbook


 

    OPENPYXL_OK = True

except ImportError:

    OPENPYXL_OK = False



 

class ReportesWindow(tk.Toplevel):

    """Genera reportes en PDF y Excel a partir de los datos de la base de datos.

    Requiere: pip install reportlab openpyxl"""


 

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Reportes")

        self.geometry("500x380")

        self._build_ui()


 

    def _build_ui(self):

        tk.Label(self, text="REPORTES", font=("Segoe UI", 16, "bold")).pack(pady=15)

        grid = tk.Frame(self)

        grid.pack(pady=10)


 

        reportes = [

            ("📄 Usuarios PDF", self._pdf_usuarios),

            ("📊 Usuarios Excel", self._excel_usuarios),

            ("📄 Libros PDF", self._pdf_libros),

            ("📊 Libros Excel", self._excel_libros),

            ("📄 Préstamos PDF", self._pdf_prestamos),

            ("📄 Categorías PDF", self._pdf_categorias),

        ]

        for i, (label, cmd) in enumerate(reportes):

            b = tk.Button(grid, text=label, width=18, height=3, bg="#f3f4f6", command=cmd)

            b.grid(row=i // 2, column=i % 2, padx=10, pady=10)


 

        if not REPORTLAB_OK or not OPENPYXL_OK:

            faltantes = []

            if not REPORTLAB_OK:

                faltantes.append("reportlab")

            if not OPENPYXL_OK:

                faltantes.append("openpyxl")

            tk.Label(

                self,

                text=f"⚠ Instale con: pip install {' '.join(faltantes)}",

                fg="#dc2626",

                font=("Segoe UI", 9),

            ).pack(pady=5)


 

    def _pick_save_path(self, default_name, ext):

        return filedialog.asksaveasfilename(

            defaultextension=ext, initialfile=default_name, filetypes=[(ext.upper(), f"*{ext}")]

        )


 

    def _pdf_generico(self, titulo, columnas, filas, default_name):

        if not REPORTLAB_OK:

            messagebox.showerror("Error", "Falta instalar la librería 'reportlab' (pip install reportlab).")

            return

        path = self._pick_save_path(default_name, ".pdf")

        if not path:

            return

        doc = SimpleDocTemplate(path, pagesize=letter)

        styles = getSampleStyleSheet()

        elementos = [Paragraph(titulo, styles["Title"]), Spacer(1, 12)]

        data = [columnas] + filas

        tabla = Table(data, repeatRows=1)

        tabla.setStyle(

            TableStyle(

                [

                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),

                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                    ("FONTSIZE", (0, 0), (-1, -1), 8),

                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f2f5")]),

                ]

            )

        )

        elementos.append(tabla)

        doc.build(elementos)

        messagebox.showinfo("Éxito", f"Reporte generado en:\n{path}")


 

    def _excel_generico(self, titulo, columnas, filas, default_name):

        if not OPENPYXL_OK:

            messagebox.showerror("Error", "Falta instalar la librería 'openpyxl' (pip install openpyxl).")

            return

        path = self._pick_save_path(default_name, ".xlsx")

        if not path:

            return

        wb = Workbook()

        ws = wb.active

        ws.title = titulo[:30]

        ws.append(columnas)

        for fila in filas:

            ws.append(fila)

        wb.save(path)

        messagebox.showinfo("Éxito", f"Reporte generado en:\n{path}")


 

    def _pdf_usuarios(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT nombres, apellidos, documento, telefono, correo FROM usuarios ORDER BY id")

        filas = [[r["nombres"], r["apellidos"], r["documento"], r["telefono"], r["correo"]] for r in cur.fetchall()]

        conn.close()

        self._pdf_generico(

            "Reporte de Usuarios", ["Nombres", "Apellidos", "Documento", "Teléfono", "Correo"], filas, "usuarios.pdf"

        )


 

    def _excel_usuarios(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT nombres, apellidos, documento, telefono, correo FROM usuarios ORDER BY id")

        filas = [[r["nombres"], r["apellidos"], r["documento"], r["telefono"], r["correo"]] for r in cur.fetchall()]

        conn.close()

        self._excel_generico(

            "Usuarios", ["Nombres", "Apellidos", "Documento", "Teléfono", "Correo"], filas, "usuarios.xlsx"

        )


 

    def _pdf_libros(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(

            """SELECT l.titulo, a.nombre as autor, e.nombre as editorial, c.nombre as categoria, l.anio_publicacion

               FROM libros l LEFT JOIN autores a ON l.autor_id=a.id

               LEFT JOIN editoriales e ON l.editorial_id=e.id

               LEFT JOIN categorias c ON l.categoria_id=c.id ORDER BY l.id"""

        )

        filas = [

            [r["titulo"], r["autor"], r["editorial"], r["categoria"], r["anio_publicacion"]] for r in cur.fetchall()

        ]

        conn.close()

        self._pdf_generico(

            "Reporte de Libros", ["Título", "Autor", "Editorial", "Categoría", "Año"], filas, "libros.pdf"

        )


 

    def _excel_libros(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(

            """SELECT l.titulo, a.nombre as autor, e.nombre as editorial, c.nombre as categoria, l.anio_publicacion

               FROM libros l LEFT JOIN autores a ON l.autor_id=a.id

               LEFT JOIN editoriales e ON l.editorial_id=e.id

               LEFT JOIN categorias c ON l.categoria_id=c.id ORDER BY l.id"""

        )

        filas = [

            [r["titulo"], r["autor"], r["editorial"], r["categoria"], r["anio_publicacion"]] for r in cur.fetchall()

        ]

        conn.close()

        self._excel_generico("Libros", ["Título", "Autor", "Editorial", "Categoría", "Año"], filas, "libros.xlsx")


 

    def _pdf_prestamos(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(

            """SELECT p.id, u.nombres || ' ' || u.apellidos as usuario, p.fecha_prestamo,

                      p.fecha_devolucion, p.estado FROM prestamos p LEFT JOIN usuarios u ON p.usuario_id=u.id

               ORDER BY p.id"""

        )

        filas = [

            [str(r["id"]), r["usuario"], r["fecha_prestamo"], r["fecha_devolucion"] or "-", r["estado"]]

            for r in cur.fetchall()

        ]

        conn.close()

        self._pdf_generico(

            "Reporte de Préstamos",

            ["ID", "Usuario", "Fecha Préstamo", "Fecha Devolución", "Estado"],

            filas,

            "prestamos.pdf",

        )


 

    def _pdf_categorias(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(

            """SELECT c.nombre, COUNT(l.id) as total FROM categorias c

               LEFT JOIN libros l ON l.categoria_id=c.id GROUP BY c.id ORDER BY total DESC"""

        )

        filas = [[r["nombre"], str(r["total"])] for r in cur.fetchall()]

        conn.close()

        self._pdf_generico("Reporte de Categorías", ["Categoría", "Total de Libros"], filas, "categorias.pdf")

