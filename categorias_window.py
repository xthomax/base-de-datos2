from catalogo_simple import SimpleCatalogWindow



 

class CategoriasWindow(SimpleCatalogWindow):

    def __init__(self, parent, on_change=None):

        super().__init__(parent, "categorias", "Gestión de Categorías", "Categoría", on_change)

 

## dashboard.py

import tkinter as tk

from database import get_connection

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


 

from usuarios_window import UsuariosWindow

from libros_window import LibrosWindow

from autores_window import AutoresWindow

from editoriales_window import EditorialesWindow

from categorias_window import CategoriasWindow

from prestamos_window import PrestamosWindow

from reportes_window import ReportesWindow

from auditoria_window import AuditoriaWindow



 

class Dashboard(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Biblioteca Combarranquilla - Sistema de Gestión")

        self.geometry("1300x760")

        self.configure(bg="#f0f2f5")

        self._build_sidebar()

        self._build_main()


 

    # ---------- Sidebar ----------

    def _build_sidebar(self):

        sidebar = tk.Frame(self, bg="#1e3a5f", width=220)

        sidebar.pack(side="left", fill="y")

        sidebar.pack_propagate(False)


 

        tk.Label(sidebar, text="📖 BIBLIOTECA", font=("Segoe UI", 13, "bold"), bg="#1e3a5f", fg="white").pack(

            pady=(20, 0)

        )

        tk.Label(sidebar, text="COMBARRANQUILLA", font=("Segoe UI", 9), bg="#1e3a5f", fg="#bcd0e6").pack(

            pady=(0, 20)

        )


 

        items = [

            ("🏠  Dashboard", self.refresh),

            ("👥  Usuarios", lambda: UsuariosWindow(self, self.refresh)),

            ("📚  Libros", lambda: LibrosWindow(self, self.refresh)),

            ("✍️  Autores", lambda: AutoresWindow(self, self.refresh)),

            ("🏢  Editoriales", lambda: EditorialesWindow(self, self.refresh)),

            ("🏷️  Categorías", lambda: CategoriasWindow(self, self.refresh)),

            ("🔄  Préstamos", lambda: PrestamosWindow(self, self.refresh)),

            ("📊  Reportes", lambda: ReportesWindow(self)),

            ("🕵️  Auditoría", lambda: AuditoriaWindow(self)),

        ]

        for text, cmd in items:

            b = tk.Button(

                sidebar,

                text=text,

                font=("Segoe UI", 10),

                bg="#1e3a5f",

                fg="white",

                bd=0,

                activebackground="#2c4f7c",

                activeforeground="white",

                anchor="w",

                padx=20,

                cursor="hand2",

                command=cmd,

            )

            b.pack(fill="x", ipady=10)


 

        tk.Frame(sidebar, bg="#1e3a5f").pack(fill="both", expand=True)

        tk.Button(

            sidebar,

            text="🚪  Cerrar Sesión",

            font=("Segoe UI", 10),

            bg="#1e3a5f",

            fg="#ff8080",

            bd=0,

            anchor="w",

            padx=20,

            cursor="hand2",

            command=self._logout,

        ).pack(fill="x", ipady=10, pady=(0, 10))


 

    def _logout(self):

        self.destroy()

        from login_window import LoginWindow


 

        def on_success():

            Dashboard().mainloop()


 

        LoginWindow(on_success).mainloop()


 

    # ---------- Contenido principal ----------

    def _build_main(self):

        self.main = tk.Frame(self, bg="#f0f2f5")

        self.main.pack(side="left", fill="both", expand=True)

        tk.Label(self.main, text="DASHBOARD", font=("Segoe UI", 20, "bold"), bg="#f0f2f5", fg="#1e3a5f").pack(

            pady=20

        )


 

        self.cards_frame = tk.Frame(self.main, bg="#f0f2f5")

        self.cards_frame.pack(fill="x", padx=30)


 

        self.chart_frame = tk.Frame(self.main, bg="white", relief="solid", bd=1)

        self.chart_frame.pack(fill="both", expand=True, padx=30, pady=20)


 

        self.refresh()


 

    def _stat_card(self, parent, icon, label, value, color):

        card = tk.Frame(parent, bg=color, width=250, height=110)

        card.pack(side="left", padx=10, fill="both", expand=True)

        card.pack_propagate(False)

        tk.Label(card, text=icon, font=("Segoe UI Emoji", 16), bg=color).pack(anchor="w", padx=15, pady=(10, 0))

        tk.Label(card, text=label, font=("Segoe UI", 9, "bold"), bg=color, fg="#333").pack(anchor="w", padx=15)

        tk.Label(card, text=str(value), font=("Segoe UI", 22, "bold"), bg=color, fg="#111").pack(anchor="w", padx=15)

        tk.Label(card, text="Total registrados", font=("Segoe UI", 8), bg=color, fg="#555").pack(anchor="w", padx=15)


 

    def refresh(self):

        """Recarga las tarjetas de estadísticas y el gráfico con datos actuales de la BD."""

        for w in self.cards_frame.winfo_children():

            w.destroy()

        for w in self.chart_frame.winfo_children():

            w.destroy()


 

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM usuarios")

        n_usuarios = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM libros")

        n_libros = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM autores")

        n_autores = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM prestamos")

        n_prestamos = cur.fetchone()[0]


 

        self._stat_card(self.cards_frame, "👥", "USUARIOS", n_usuarios, "#cfe8ff")

        self._stat_card(self.cards_frame, "📚", "LIBROS", n_libros, "#d6f5d6")

        self._stat_card(self.cards_frame, "✍️", "AUTORES", n_autores, "#ffe8b3")

        self._stat_card(self.cards_frame, "🔄", "PRÉSTAMOS", n_prestamos, "#e6ccff")


 

        cur.execute(

            """

            SELECT c.nombre, COUNT(l.id) as total

            FROM categorias c LEFT JOIN libros l ON l.categoria_id = c.id

            GROUP BY c.id ORDER BY total DESC

            """

        )

        data = cur.fetchall()

        conn.close()


 

        labels = [r["nombre"] for r in data]

        values = [r["total"] for r in data]


 

        fig = Figure(figsize=(8, 4), dpi=90)

        ax = fig.add_subplot(111)

        bars = ax.bar(labels, values, color="#4a90d9")

        if values:

            max_idx = values.index(max(values))

            bars[max_idx].set_color("#999999")

        ax.set_title("LIBROS POR CATEGORÍA", fontsize=12, fontweight="bold")

        ax.set_xlabel("Categorías")

        ax.set_ylabel("Cantidad de Libros")

        for i, v in enumerate(values):

            ax.text(i, v + 0.3, str(v), ha="center", fontsize=9)

        fig.tight_layout()


 

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)

        canvas.draw()

        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

