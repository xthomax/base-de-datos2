import tkinter as tk

from tkinter import ttk, messagebox

from datetime import datetime

from database import get_connection, log_auditoria



 

class PrestamosWindow(tk.Toplevel):

    def __init__(self, parent, on_change=None):

        super().__init__(parent)

        self.on_change = on_change

        self.temp_libros = []  # [{"libro_id":.., "titulo":.., "cantidad":..}]

        self.selected_prestamo_id = None

        self.title("Gestión de Préstamos")

        self.geometry("1250x680")

        self._build_ui()

        self._load_combos()

        self._load_prestamos()


 

    def _build_ui(self):

        top = tk.Frame(self)

        top.pack(fill="x", padx=15, pady=10)


 

        form1 = tk.LabelFrame(top, text="DATOS DEL PRÉSTAMO", font=("Segoe UI", 10, "bold"), padx=10, pady=10)

        form1.pack(side="left", fill="both", expand=True, padx=(0, 5))


 

        tk.Label(form1, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.usuario_combo = ttk.Combobox(form1, width=30, state="readonly")

        self.usuario_combo.grid(row=0, column=1, padx=5, pady=5)


 

        tk.Label(form1, text="Fecha Préstamo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.fecha_prestamo_entry = ttk.Entry(form1, width=32)

        self.fecha_prestamo_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.fecha_prestamo_entry.grid(row=1, column=1, padx=5, pady=5)


 

        tk.Label(form1, text="Fecha Devolución:").grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.fecha_devolucion_entry = ttk.Entry(form1, width=32)

        self.fecha_devolucion_entry.grid(row=2, column=1, padx=5, pady=5)


 

        tk.Label(form1, text="Estado:").grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.estado_combo = ttk.Combobox(

            form1, width=30, state="readonly", values=["PRESTADO", "DEVUELTO", "ATRASADO"]

        )

        self.estado_combo.set("PRESTADO")

        self.estado_combo.grid(row=3, column=1, padx=5, pady=5)


 

        form2 = tk.LabelFrame(

            top, text="AGREGAR LIBRO AL PRÉSTAMO", font=("Segoe UI", 10, "bold"), padx=10, pady=10

        )

        form2.pack(side="left", fill="both", expand=True, padx=(5, 0))


 

        tk.Label(form2, text="Libro:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.libro_combo = ttk.Combobox(form2, width=30, state="readonly")

        self.libro_combo.grid(row=0, column=1, padx=5, pady=5)


 

        tk.Label(form2, text="Cantidad:").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.cantidad_spin = tk.Spinbox(form2, from_=1, to=99, width=30)

        self.cantidad_spin.grid(row=1, column=1, padx=5, pady=5)


 

        tk.Button(form2, text="Agregar Libro", bg="#22c55e", fg="white", command=self._agregar_libro_temp).grid(

            row=2, column=0, columnspan=2, sticky="ew", pady=10

        )


 

        mid = tk.Frame(self)

        mid.pack(fill="both", expand=True, padx=15, pady=5)


 

        libros_frame = tk.LabelFrame(

            mid, text="LIBROS DEL PRÉSTAMO (doble clic para quitar)", font=("Segoe UI", 10, "bold")

        )

        libros_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))


 

        cols1 = ("libro_id", "titulo", "cantidad")

        self.tree_libros = ttk.Treeview(libros_frame, columns=cols1, show="headings", height=10)

        for c, h in zip(cols1, ["ID Libro", "Título", "Cantidad"]):

            self.tree_libros.heading(c, text=h)

        self.tree_libros.column("libro_id", width=70)

        self.tree_libros.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree_libros.bind("<Double-1>", self._quitar_libro_temp)


 

        prestamos_frame = tk.LabelFrame(mid, text="LISTADO DE PRÉSTAMOS", font=("Segoe UI", 10, "bold"))

        prestamos_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))


 

        topp = tk.Frame(prestamos_frame)

        topp.pack(fill="x")

        tk.Label(topp, text="Buscar:").pack(side="right", padx=(0, 5))

        self.search_var = tk.StringVar()

        self.search_var.trace_add("write", lambda *a: self._load_prestamos())

        ttk.Entry(topp, textvariable=self.search_var, width=20).pack(side="right")


 

        cols2 = ("id", "usuario", "fecha", "estado")

        self.tree_prestamos = ttk.Treeview(prestamos_frame, columns=cols2, show="headings", height=10)

        for c, h in zip(cols2, ["ID", "Usuario", "Fecha", "Estado"]):

            self.tree_prestamos.heading(c, text=h)

        self.tree_prestamos.column("id", width=50)

        self.tree_prestamos.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree_prestamos.bind("<<TreeviewSelect>>", self._on_select_prestamo)


 

        bottom = tk.Frame(self)

        bottom.pack(fill="x", padx=15, pady=10)

        tk.Button(bottom, text="Quitar Seleccionado", bg="#dc2626", fg="white", command=self._quitar_prestamo).pack(

            side="left", padx=5

        )

        tk.Button(bottom, text="Limpiar Formulario", command=self._limpiar).pack(side="left", padx=5)

        tk.Button(bottom, text="Guardar Préstamo", bg="#22c55e", fg="white", command=self._guardar_prestamo).pack(

            side="right", padx=5

        )


 

        self.total_label = tk.Label(self, text="Total préstamos: 0", font=("Segoe UI", 9, "bold"))

        self.total_label.pack(anchor="w", padx=20, pady=(0, 10))


 

    def _load_combos(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT id, nombres, apellidos FROM usuarios ORDER BY nombres")

        self.usuarios = cur.fetchall()

        cur.execute("SELECT id, titulo FROM libros ORDER BY titulo")

        self.libros = cur.fetchall()

        conn.close()

        self.usuario_combo["values"] = [f"{u['nombres']} {u['apellidos']}" for u in self.usuarios]

        self.libro_combo["values"] = [l["titulo"] for l in self.libros]


 

    def _agregar_libro_temp(self):

        titulo = self.libro_combo.get()

        if not titulo:

            messagebox.showwarning("Validación", "Seleccione un libro.")

            return

        try:

            cantidad = int(self.cantidad_spin.get())

        except ValueError:

            cantidad = 1

        libro_id = None

        for l in self.libros:

            if l["titulo"] == titulo:

                libro_id = l["id"]

        for item in self.temp_libros:

            if item["libro_id"] == libro_id:

                item["cantidad"] += cantidad

                self._refresh_temp_tree()

                return

        self.temp_libros.append({"libro_id": libro_id, "titulo": titulo, "cantidad": cantidad})

        self._refresh_temp_tree()


 

    def _refresh_temp_tree(self):

        for r in self.tree_libros.get_children():

            self.tree_libros.delete(r)

        for item in self.temp_libros:

            self.tree_libros.insert("", "end", values=(item["libro_id"], item["titulo"], item["cantidad"]))


 

    def _quitar_libro_temp(self, event):

        sel = self.tree_libros.selection()

        if not sel:

            return

        vals = self.tree_libros.item(sel[0])["values"]

        self.temp_libros = [i for i in self.temp_libros if i["libro_id"] != vals[0]]

        self._refresh_temp_tree()


 

    def _guardar_prestamo(self):

        usuario_nombre = self.usuario_combo.get()

        if not usuario_nombre:

            messagebox.showwarning("Validación", "Seleccione un usuario.")

            return

        if not self.temp_libros:

            messagebox.showwarning("Validación", "Agregue al menos un libro al préstamo.")

            return

        usuario_id = None

        for u in self.usuarios:

            if f"{u['nombres']} {u['apellidos']}" == usuario_nombre:

                usuario_id = u["id"]


 

        fecha_prestamo = self.fecha_prestamo_entry.get().strip()

        fecha_devolucion = self.fecha_devolucion_entry.get().strip()

        estado = self.estado_combo.get()


 

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute(

                """INSERT INTO prestamos (usuario_id, fecha_prestamo, fecha_devolucion, estado)

                   VALUES (?,?,?,?)""",

                (usuario_id, fecha_prestamo, fecha_devolucion or None, estado),

            )

            prestamo_id = cur.lastrowid

            for item in self.temp_libros:

                cur.execute(

                    "INSERT INTO prestamo_libros (prestamo_id, libro_id, cantidad) VALUES (?,?,?)",

                    (prestamo_id, item["libro_id"], item["cantidad"]),

                )

            conn.commit()

            log_auditoria("prestamos", "INSERT", prestamo_id, f"Préstamo creado ID: {prestamo_id}")

            messagebox.showinfo("Éxito", "Préstamo guardado correctamente.")

            self._limpiar()

            self._load_prestamos()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo guardar el préstamo: {e}")

        finally:

            conn.close()


 

    def _load_prestamos(self):

        for r in self.tree_prestamos.get_children():

            self.tree_prestamos.delete(r)

        conn = get_connection()

        cur = conn.cursor()

        q = self.search_var.get().strip()

        base = """SELECT p.id, u.nombres || ' ' || u.apellidos as usuario, p.fecha_prestamo, p.estado

                  FROM prestamos p LEFT JOIN usuarios u ON p.usuario_id = u.id"""

        if q:

            base += " WHERE u.nombres LIKE ? OR u.apellidos LIKE ? ORDER BY p.id DESC"

            cur.execute(base, (f"%{q}%", f"%{q}%"))

        else:

            base += " ORDER BY p.id DESC"

            cur.execute(base)

        rows = cur.fetchall()

        for row in rows:

            self.tree_prestamos.insert(

                "", "end", values=(row["id"], row["usuario"], row["fecha_prestamo"], row["estado"])

            )

        cur.execute("SELECT COUNT(*) FROM prestamos")

        total = cur.fetchone()[0]

        conn.close()

        self.total_label.config(text=f"Total préstamos: {total}")


 

    def _on_select_prestamo(self, event):

        sel = self.tree_prestamos.selection()

        if not sel:

            return

        vals = self.tree_prestamos.item(sel[0])["values"]

        self.selected_prestamo_id = vals[0]

        self.usuario_combo.set(vals[1])

        self.fecha_prestamo_entry.delete(0, tk.END)

        self.fecha_prestamo_entry.insert(0, vals[2] or "")

        self.estado_combo.set(vals[3])


 

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(

            """SELECT pl.libro_id, l.titulo, pl.cantidad FROM prestamo_libros pl

               JOIN libros l ON pl.libro_id = l.id WHERE pl.prestamo_id=?""",

            (self.selected_prestamo_id,),

        )

        rows = cur.fetchall()

        conn.close()

        self.temp_libros = [

            {"libro_id": r["libro_id"], "titulo": r["titulo"], "cantidad": r["cantidad"]} for r in rows

        ]

        self._refresh_temp_tree()


 

    def _quitar_prestamo(self):

        if not self.selected_prestamo_id:

            messagebox.showwarning("Selección", "Seleccione un préstamo de la lista.")

            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este préstamo?"):

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute("DELETE FROM prestamo_libros WHERE prestamo_id=?", (self.selected_prestamo_id,))

            cur.execute("DELETE FROM prestamos WHERE id=?", (self.selected_prestamo_id,))

            conn.commit()

            log_auditoria(

                "prestamos", "DELETE", self.selected_prestamo_id, f"Préstamo eliminado ID: {self.selected_prestamo_id}"

            )

            messagebox.showinfo("Éxito", "Préstamo eliminado.")

            self._limpiar()

            self._load_prestamos()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

        finally:

            conn.close()


 

    def _limpiar(self):

        self.selected_prestamo_id = None

        self.temp_libros = []

        self._refresh_temp_tree()

        self.usuario_combo.set("")

        self.fecha_prestamo_entry.delete(0, tk.END)

        self.fecha_prestamo_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.fecha_devolucion_entry.delete(0, tk.END)

        self.estado_combo.set("PRESTADO")