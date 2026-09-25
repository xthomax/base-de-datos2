import tkinter as tk

from tkinter import ttk, messagebox

from database import get_connection, log_auditoria



 

class AutoresWindow(tk.Toplevel):

    def __init__(self, parent, on_change=None):

        super().__init__(parent)

        self.on_change = on_change

        self.selected_id = None

        self.title("Gestión de Autores")

        self.geometry("700x550")

        self._build_ui()

        self._load_data()


 

    def _build_ui(self):

        form = tk.LabelFrame(self, text="DATOS DEL AUTOR", font=("Segoe UI", 10, "bold"), padx=10, pady=10)

        form.pack(fill="x", padx=15, pady=10)


 

        tk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.nombre_entry = ttk.Entry(form, width=35)

        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)


 

        tk.Label(form, text="Nacionalidad:").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.nac_entry = ttk.Entry(form, width=35)

        self.nac_entry.grid(row=1, column=1, padx=5, pady=5)


 

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


 

        list_frame = tk.LabelFrame(self, text="LISTADO DE AUTORES", font=("Segoe UI", 10, "bold"))

        list_frame.pack(fill="both", expand=True, padx=15, pady=10)


 

        top = tk.Frame(list_frame)

        top.pack(fill="x")

        tk.Label(top, text="Buscar:").pack(side="right", padx=(0, 5))

        self.search_var = tk.StringVar()

        self.search_var.trace_add("write", lambda *a: self._load_data())

        ttk.Entry(top, textvariable=self.search_var, width=25).pack(side="right")


 

        cols = ("id", "nombre", "nacionalidad")

        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)

        for c, h in zip(cols, ["ID", "Nombre", "Nacionalidad"]):

            self.tree.heading(c, text=h)

            self.tree.column(c, width=150)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)


 

        self.total_label = tk.Label(self, text="Total autores: 0", font=("Segoe UI", 9, "bold"))

        self.total_label.pack(anchor="w", padx=20, pady=(0, 10))


 

    def _load_data(self):

        for r in self.tree.get_children():

            self.tree.delete(r)

        conn = get_connection()

        cur = conn.cursor()

        q = self.search_var.get().strip()

        if q:

            cur.execute("SELECT * FROM autores WHERE nombre LIKE ? ORDER BY id", (f"%{q}%",))

        else:

            cur.execute("SELECT * FROM autores ORDER BY id")

        rows = cur.fetchall()

        for row in rows:

            self.tree.insert("", "end", values=(row["id"], row["nombre"], row["nacionalidad"]))

        cur.execute("SELECT COUNT(*) FROM autores")

        total = cur.fetchone()[0]

        conn.close()

        self.total_label.config(text=f"Total autores: {total}")


 

    def _on_select(self, event):

        sel = self.tree.selection()

        if not sel:

            return

        vals = self.tree.item(sel[0])["values"]

        self.selected_id = vals[0]

        self.nombre_entry.delete(0, tk.END)

        self.nombre_entry.insert(0, vals[1])

        self.nac_entry.delete(0, tk.END)

        self.nac_entry.insert(0, vals[2] or "")


 

    def _guardar(self):

        nombre = self.nombre_entry.get().strip()

        nac = self.nac_entry.get().strip()

        if not nombre:

            messagebox.showwarning("Validación", "El nombre es obligatorio.")

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute("INSERT INTO autores (nombre, nacionalidad) VALUES (?,?)", (nombre, nac))

            conn.commit()

            new_id = cur.lastrowid

            log_auditoria("autores", "INSERT", new_id, f"Autor creado: {nombre}")

            messagebox.showinfo("Éxito", "Autor guardado correctamente.")

            self._limpiar()

            self._load_data()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo guardar: {e}")

        finally:

            conn.close()


 

    def _actualizar(self):

        if not self.selected_id:

            messagebox.showwarning("Selección", "Seleccione un autor de la lista.")

            return

        nombre = self.nombre_entry.get().strip()

        nac = self.nac_entry.get().strip()

        if not nombre:

            messagebox.showwarning("Validación", "El nombre es obligatorio.")

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute("UPDATE autores SET nombre=?, nacionalidad=? WHERE id=?", (nombre, nac, self.selected_id))

            conn.commit()

            log_auditoria("autores", "UPDATE", self.selected_id, f"Autor actualizado: {nombre}")

            messagebox.showinfo("Éxito", "Autor actualizado correctamente.")

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

            messagebox.showwarning("Selección", "Seleccione un autor de la lista.")

            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este autor?"):

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute("SELECT nombre FROM autores WHERE id=?", (self.selected_id,))

            row = cur.fetchone()

            nombre = row["nombre"] if row else ""

            cur.execute("DELETE FROM autores WHERE id=?", (self.selected_id,))

            conn.commit()

            log_auditoria("autores", "DELETE", self.selected_id, f"Autor eliminado: {nombre}")

            messagebox.showinfo("Éxito", "Autor eliminado.")

            self._limpiar()

            self._load_data()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo eliminar (verifique libros asociados): {e}")

        finally:

            conn.close()


 

    def _limpiar(self):

        self.selected_id = None

        self.nombre_entry.delete(0, tk.END)

        self.nac_entry.delete(0, tk.END)

