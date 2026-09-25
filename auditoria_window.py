import tkinter as tk

from tkinter import ttk

from database import get_connection



 

class AuditoriaWindow(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Auditoría")

        self.geometry("950x520")

        self._build_ui()

        self._load_data()


 

    def _build_ui(self):

        frame = tk.LabelFrame(self, text="REGISTROS DE AUDITORÍA", font=("Segoe UI", 10, "bold"))

        frame.pack(fill="both", expand=True, padx=15, pady=15)


 

        cols = ("id", "tabla", "operacion", "id_registro", "fecha", "descripcion")

        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=18)

        headers = ["ID", "Tabla", "Operación", "ID Registro", "Fecha", "Descripción"]

        widths = [50, 100, 100, 90, 150, 380]

        for c, h, w in zip(cols, headers, widths):

            self.tree.heading(c, text=h)

            self.tree.column(c, width=w)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

 

        tk.Button(self, text="Actualizar", command=self._load_data).pack(pady=5)

        self.total_label = tk.Label(self, text="Total registros: 0", font=("Segoe UI", 9, "bold"))

        self.total_label.pack(anchor="w", padx=20, pady=(0, 10))


 

    def _load_data(self):

        for r in self.tree.get_children():

            self.tree.delete(r)

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT * FROM auditoria ORDER BY id DESC")

        rows = cur.fetchall()

        for row in rows:

            self.tree.insert(

                "",

                "end",

                values=(row["id"], row["tabla"], row["operacion"], row["id_registro"], row["fecha"], row["descripcion"]),

            )

        cur.execute("SELECT COUNT(*) FROM auditoria")

        total = cur.fetchone()[0]

        conn.close()

        self.total_label.config(text=f"Total registros: {total}")