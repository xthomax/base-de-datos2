import tkinter as tk

from tkinter import ttk, messagebox

from datetime import datetime

from database import get_connection, log_auditoria



 

class UsuariosWindow(tk.Toplevel):

    def __init__(self, parent, on_change=None):

        super().__init__(parent)

        self.on_change = on_change

        self.selected_id = None

        self.title("Gestión de Usuarios")

        self.geometry("950x600")

        self._build_ui()

        self._load_data()


 

    def _build_ui(self):

        form = tk.LabelFrame(self, text="DATOS DEL USUARIO", font=("Segoe UI", 10, "bold"), padx=10, pady=10)

        form.pack(fill="x", padx=15, pady=10)


 

        self.entries = {}

        fields = [

            ("Nombres:", "nombres", 0, 0),

            ("Correo:", "correo", 0, 2),

            ("Apellidos:", "apellidos", 1, 0),

            ("Dirección:", "direccion", 1, 2),

            ("Documento:", "documento", 2, 0),

            ("Fecha Registro:", "fecha_registro", 2, 2),

            ("Teléfono:", "telefono", 3, 0),

        ]

        for label, key, r, c in fields:

            tk.Label(form, text=label).grid(row=r, column=c, sticky="w", padx=5, pady=5)

            e = ttk.Entry(form, width=30)

            e.grid(row=r, column=c + 1, padx=5, pady=5)

            self.entries[key] = e

        self.entries["fecha_registro"].insert(0, datetime.now().strftime("%Y-%m-%d"))


 

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


 

        list_frame = tk.LabelFrame(self, text="LISTADO DE USUARIOS", font=("Segoe UI", 10, "bold"))

        list_frame.pack(fill="both", expand=True, padx=15, pady=10)


 

        top = tk.Frame(list_frame)

        top.pack(fill="x")

        tk.Label(top, text="Buscar:").pack(side="right", padx=(0, 5))

        self.search_var = tk.StringVar()

        self.search_var.trace_add("write", lambda *a: self._load_data())

        ttk.Entry(top, textvariable=self.search_var, width=25).pack(side="right")


 

        cols = ("id", "nombres", "apellidos", "documento", "telefono", "correo", "fecha_registro")

        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)

        headers = ["ID", "Nombres", "Apellidos", "Documento", "Teléfono", "Correo", "Fecha Registro"]

        for c, h in zip(cols, headers):

            self.tree.heading(c, text=h)

            self.tree.column(c, width=115)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)


 

        self.total_label = tk.Label(self, text="Total usuarios: 0", font=("Segoe UI", 9, "bold"))

        self.total_label.pack(anchor="w", padx=20, pady=(0, 10))


 

    def _load_data(self):

        for r in self.tree.get_children():

            self.tree.delete(r)

        conn = get_connection()

        cur = conn.cursor()

        q = self.search_var.get().strip()

        if q:

            cur.execute(

                """SELECT * FROM usuarios WHERE nombres LIKE ? OR apellidos LIKE ? OR documento LIKE ?

                   ORDER BY id""",

                (f"%{q}%", f"%{q}%", f"%{q}%"),

            )

        else:

            cur.execute("SELECT * FROM usuarios ORDER BY id")

        rows = cur.fetchall()

        for row in rows:

            self.tree.insert(

                "",

                "end",

                values=(

                    row["id"],

                    row["nombres"],

                    row["apellidos"],

                    row["documento"],

                    row["telefono"],

                    row["correo"],

                    row["fecha_registro"],

                ),

            )

        cur.execute("SELECT COUNT(*) FROM usuarios")

        total = cur.fetchone()[0]

        conn.close()

        self.total_label.config(text=f"Total usuarios: {total}")


 

    def _on_select(self, event):

        sel = self.tree.selection()

        if not sel:

            return

        vals = self.tree.item(sel[0])["values"]

        self.selected_id = vals[0]

        keys = ["id", "nombres", "apellidos", "documento", "telefono", "correo", "fecha_registro"]

        data = dict(zip(keys, vals))

        for k in ["nombres", "apellidos", "documento", "telefono", "correo", "fecha_registro"]:

            self.entries[k].delete(0, tk.END)

            self.entries[k].insert(0, data.get(k, ""))


 

    def _get_form(self):

        return {k: e.get().strip() for k, e in self.entries.items()}


 

    def _validar(self, data):

        if not data["nombres"] or not data["apellidos"] or not data["documento"]:

            messagebox.showwarning("Validación", "Nombres, Apellidos y Documento son obligatorios.")

            return False

        return True


 

    def _guardar(self):

        data = self._get_form()

        if not self._validar(data):

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute(

                """INSERT INTO usuarios (nombres, apellidos, documento, telefono, correo, direccion, fecha_registro)

                   VALUES (?,?,?,?,?,?,?)""",

                (

                    data["nombres"],

                    data["apellidos"],

                    data["documento"],

                    data["telefono"],

                    data["correo"],

                    data["direccion"],

                    data["fecha_registro"],

                ),

            )

            conn.commit()

            new_id = cur.lastrowid

            log_auditoria("usuarios", "INSERT", new_id, f"Usuario creado: {data['nombres']}")

            messagebox.showinfo("Éxito", "Usuario guardado correctamente.")

            self._limpiar()

            self._load_data()

            if self.on_change:

                self.on_change()

        except Exception as e:

            messagebox.showerror("Error", f"No se pudo guardar (¿documento duplicado?): {e}")

        finally:

            conn.close()


 

    def _actualizar(self):

        if not self.selected_id:

            messagebox.showwarning("Selección", "Seleccione un usuario de la lista.")

            return

        data = self._get_form()

        if not self._validar(data):

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute(

                """UPDATE usuarios SET nombres=?, apellidos=?, documento=?, telefono=?, correo=?, direccion=?,

                   fecha_registro=? WHERE id=?""",

                (

                    data["nombres"],

                    data["apellidos"],

                    data["documento"],

                    data["telefono"],

                    data["correo"],

                    data["direccion"],

                    data["fecha_registro"],

                    self.selected_id,

                ),

            )

            conn.commit()

            log_auditoria("usuarios", "UPDATE", self.selected_id, f"Usuario actualizado: {data['nombres']}")

            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")

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

            messagebox.showwarning("Selección", "Seleccione un usuario de la lista.")

            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):

            return

        conn = get_connection()

        cur = conn.cursor()

        try:

            cur.execute("SELECT nombres FROM usuarios WHERE id=?", (self.selected_id,))

            row = cur.fetchone()

            nombre = row["nombres"] if row else ""

            cur.execute("DELETE FROM usuarios WHERE id=?", (self.selected_id,))

            conn.commit()

            log_auditoria("usuarios", "DELETE", self.selected_id, f"Usuario eliminado: {nombre}")

            messagebox.showinfo("Éxito", "Usuario eliminado.")

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

        for k, e in self.entries.items():

            e.delete(0, tk.END)

        self.entries["fecha_registro"].insert(0, datetime.now().strftime("%Y-%m-%d"))

