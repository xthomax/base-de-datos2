import tkinter as tk

from tkinter import ttk, messagebox

from database import get_connection, log_auditoria



 

class LibrosWindow(tk.Toplevel):

    def __init__(self, parent, on_change=None):

        super().__init__(parent)

        self.on_change = on_change

        self.selected_id = None

        self.title("Gestión de Libros")

        self.geometry("950x600")

        self._build_ui()

        self._load_combos()

        self._load_data()


 

    def _build_ui(self):

        form = tk.LabelFrame(self, text="DATOS DEL LIBRO", font=("Segoe UI", 10, "bold"), padx=10, pady=10)

        form.pack(fill="x", padx=15, pady=10)


 

        tk.Label(form, text="Título:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.titulo_entry = ttk.Entry(form, width=30)

        self.titulo_entry.grid(row=0, column=1, padx=5, pady=5)


 

        tk.Label(form, text="Autor:").grid(row=0, column=2, sticky="w", padx=5, pady=5)

        self.autor_combo = ttk.Combobox(form, width=27, state="readonly")

        self.autor_combo.grid(row=0, column=3, padx=5, pady=5)


 

        tk.Label(form, text="ISBN:").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.isbn_entry = ttk.Entry(form, width=30)

        self.isbn_entry.grid(row=1, column=1, padx=5, pady=5)


 

        tk.Label(form, text="Editorial:").grid(row=1, column=2, sticky="w", padx=5, pady=5)

        self.editorial_combo = ttk.Combobox(form, width=27, state="readonly")

        self.editorial_combo.grid(row=1, column=3, padx=5, pady=5)


 

        tk.Label(form, text="Año Publicación:").grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.anio_entry = ttk.Entry(form, width=30)

        self.anio_entry.grid(row=2, column=1, padx=5, pady=5)


 

        tk.Label(form, text="Categoría:").grid(row=2, column=2, sticky="w", padx=5, pady=5)

        self.categoria_combo = ttk.Combobox(form, width=27, state="readonly")

        self.categoria_combo.grid(row=2, column=3, padx=5, pady=5)


 

        btns = tk.Frame(self)

        btns.pack(fill="x", padx=15)

        tk.Button(btns, text="Guardar", bg="#22c55e", fg="white", width=12, command=self._guardar).pack(

            side="left", padx=5

        )

        tk.Button(btns, text="Actualizar", bg="#2563eb", fg="white", width=12, command=self._actualizar).pack(

            side="left", padx=5

        )

        tk.Button(btns, text="Eliminar", bg="#dc2626", fg="white", width=12, command=self._eliminar).pack(

            side="left", padx=5

        )

        tk.Button(btns, text="Limpiar", width=12, command=self._limpiar).pack(side="left", padx=5)


 

        list_frame = tk.LabelFrame(self, text="LISTADO DE LIBROS", font=("Segoe UI", 10, "bold"))

        list_frame.pack(fill="both", expand=True, padx=15, pady=10)


 

        top = tk.Frame(list_frame)

        top.pack(fill="x")

        tk.Label(top, text="Buscar:").pack(side="right", padx=(0, 5))

        self.search_var = tk.StringVar()

        self.search_var.trace_add("write", lambda *a: self._load_data())

        ttk.Entry(top, textvariable=self.search_var, width=25).pack(side="right")


 

        cols = ("id", "titulo", "autor", "editorial", "categoria", "anio")

        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)

        headers = ["ID", "Título", "Autor", "Editorial", "Categoría", "Año"]

        for c, h in zip(cols, headers):

            self.tree.heading(c, text=h)

            self.tree.column(c, width=130)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)


 

        self.total_label = tk.Label(self, text="Total libros: 0", font=("Segoe UI", 9, "bold"))

        self.total_label.pack(anchor="w", padx=20, pady=(0, 10))


 

    def _load_combos(self):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT id, nombre FROM autores ORDER BY nombre")

        self.autores = cur.fetchall()

        cur.execute("SELECT id, nombre FROM editoriales ORDER BY nombre")

        self.editoriales = cur.fetchall()

        cur.execute("SELECT id, nombre FROM categorias ORDER BY nombre")

        self.categorias = cur.fetchall()

        conn.close()

        self.autor_combo["values"] = [a["nombre"] for a in self.autores]

        self.editorial_combo["values"] = [e["nombre"] for e in self.editoriales]

        self.categoria_combo["values"] = [c["nombre"] for c in self.categorias]


 

    def _load_data(self):

        for r in self.tree.get_children():

            self.tree.delete(r)

        conn = get_connection()

        cur = conn.cursor()

        q = self.search_var.get().strip()

        base = """SELECT l.id, l.titulo, a.nombre as autor, e.nombre as editorial, c.nombre as categoria,

                         l.anio_publicacion

                  FROM libros l

                  LEFT JOIN autores a ON l.autor_id=a.id

                  LEFT JOIN editoriales e ON l.editorial_id=e.id

                  LEFT JOIN categorias c ON l.categoria_id=c.id"""

        if q:

            base += " WHERE l.titulo LIKE ? OR a.nombre LIKE ? ORDER BY l.id"

            cur.execute(base, (f"%{q}%", f"%{q}%"))

        else:

            base += " ORDER BY l.id"

            cur.execute(base)

        rows = cur.fetchall()

        for row in rows:

            self.tree.insert(

                "",

                "end",

                values=(row["id"], row["titulo"], row["autor"], row["editorial"], row["categoria"], row["anio_publicacion"]),

            )

        cur.execute("SELECT COUNT(*) FROM libros")

        total = cur.fetchone()[0]

        conn.close()

        self.total_label.config(text=f"Total libros: {total}")


 

    def _on_select(self, event):

        sel = self.tree.selection()

        if not sel:

            return

        vals = self.tree.item(sel[0])["values"]

        self.selected_id = vals[0]

        self.titulo_entry.delete(0, tk.END)

        self.titulo_entry.insert(0, vals[1])

        self.autor_combo.set(vals[2] or "")

        self.editorial_combo.set(vals[3] or "")

        self.categoria_combo.set(vals[4] or "")

        self.anio_entry.delete(0, tk.END)

        self.anio_entry.insert(0, vals[5] or "")


 

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT isbn FROM libros WHERE id=?", (self.selected_id,))

        row = cur.fetchone()

        conn.close()

        self.isbn_entry.delete(0, tk.END)

        self.isbn_entry.insert(0, row["isbn"] if row and row["isbn"] else "")


 

    def _get_ids(self):

        autor_id = None

        for a in self.autores:

            if a["nombre"] == self.autor_combo.get():

                autor_id = a["id"]

        editorial_id = None

        for e in self.editoriales:

            if e["nombre"] == self.editorial_combo.get():

                editorial_id = e["id"]

        categoria_id = None

        for c in self.categorias:

            if c["nombre"] == self.categoria_combo.get():

                categoria_id = c["id"]

        return autor_id, editorial_id, categoria_id


 

    def _guardar(self):

        titulo = self.titulo_entry.get().strip()

        isbn = self.isbn_entry.get().strip()

        anio = self.anio_entry.get().strip()

        if not titulo:

            messagebox.showwarning("Validación", "El título es obligatorio.")

            return

        autor_id, editorial_id, categoria_id = self._get_ids()

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute(

                """INSERT INTO libros (titulo, isbn, anio_publicacion, autor_id, editorial_id, categoria_id)

                   VALUES (?,?,?,?,?,?)""",

                (titulo, isbn or None, anio, autor_id, editorial_id, categoria_id),

            )

            conn.commit()

            new_id = cur.lastrowid

            log_auditoria("libros", "INSERT", new_id, f"Libro creado: {titulo}")

            messagebox.showinfo("Éxito", "Libro guardado correctamente.")

            self._limpiar()

            self._load_data()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo guardar (¿ISBN duplicado?): {e}")

        finally:

            conn.close()


 

    def _actualizar(self):

        if not self.selected_id:

            messagebox.showwarning("Selección", "Seleccione un libro de la lista.")

            return

        titulo = self.titulo_entry.get().strip()

        isbn = self.isbn_entry.get().strip()

        anio = self.anio_entry.get().strip()

        if not titulo:

            messagebox.showwarning("Validación", "El título es obligatorio.")

            return

        autor_id, editorial_id, categoria_id = self._get_ids()

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute(

                """UPDATE libros SET titulo=?, isbn=?, anio_publicacion=?, autor_id=?, editorial_id=?,

                   categoria_id=? WHERE id=?""",

                (titulo, isbn or None, anio, autor_id, editorial_id, categoria_id, self.selected_id),

            )

            conn.commit()

            log_auditoria("libros", "UPDATE", self.selected_id, f"Libro actualizado: {titulo}")

            messagebox.showinfo("Éxito", "Libro actualizado correctamente.")

            self._limpiar()

            self._load_data()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        finally:

            conn.close()


 

    def _eliminar(self):

        if not self.selected_id:

            messagebox.showwarning("Selección", "Seleccione un libro de la lista.")

            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este libro?"):

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute("SELECT titulo FROM libros WHERE id=?", (self.selected_id,))

            row = cur.fetchone()

            titulo = row["titulo"] if row else ""

            cur.execute("DELETE FROM libros WHERE id=?", (self.selected_id,))

            conn.commit()

            log_auditoria("libros", "DELETE", self.selected_id, f"Libro eliminado: {titulo}")

            messagebox.showinfo("Éxito", "Libro eliminado.")

            self._limpiar()

            self._load_data()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo eliminar (verifique préstamos asociados): {e}")

        finally:

            conn.close()


 

    def _limpiar(self):

        self.selected_id = None

        self.titulo_entry.delete(0, tk.END)

        self.isbn_entry.delete(0, tk.END)

        self.anio_entry.delete(0, tk.END)

        self.autor_combo.set("")

        self.editorial_combo.set("")

        self.categoria_combo.set("")