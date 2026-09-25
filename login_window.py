import tkinter as tk

from tkinter import ttk, messagebox

from database import get_connection



 

class LoginWindow(tk.Tk):

    """Ventana de inicio de sesión. Usuario por defecto: admin / admin123"""


 

    def __init__(self, on_success):

        super().__init__()

        self.on_success = on_success

        self.title("Biblioteca Combarranquilla - Iniciar Sesión")

        self.geometry("900x520")

        self.resizable(False, False)

        self.configure(bg="#f0f2f5")

        self._build_ui()


 

    def _build_ui(self):

        left = tk.Frame(self, bg="#1e3a5f", width=450)

        left.pack(side="left", fill="both", expand=True)


 

        tk.Label(left, text="📖", font=("Segoe UI Emoji", 60), bg="#1e3a5f", fg="white").pack(pady=(140, 10))

        tk.Label(left, text="BIBLIOTECA", font=("Segoe UI", 22, "bold"), bg="#1e3a5f", fg="white").pack()

        tk.Label(left, text="COMBARRANQUILLA", font=("Segoe UI", 14), bg="#1e3a5f", fg="white").pack()

        tk.Label(left, text="Sistema de Gestión", font=("Segoe UI", 10), bg="#1e3a5f", fg="#bcd0e6").pack(pady=(30, 0))

        tk.Label(left, text="v1.0", font=("Segoe UI", 9), bg="#1e3a5f", fg="#7f9cc1").pack(pady=(5, 0))


 

        right = tk.Frame(self, bg="white", width=450)

        right.pack(side="right", fill="both", expand=True)


 

        form = tk.Frame(right, bg="white")

        form.place(relx=0.5, rely=0.5, anchor="center")


 

        tk.Label(form, text="INICIAR SESIÓN", font=("Segoe UI", 18, "bold"), bg="white", fg="#1e3a5f").grid(

            row=0, column=0, columnspan=2, pady=(0, 30)

        )


 

        tk.Label(form, text="Usuario:", font=("Segoe UI", 10), bg="white").grid(row=1, column=0, sticky="w", pady=8)

        self.user_entry = ttk.Entry(form, width=28, font=("Segoe UI", 10))

        self.user_entry.grid(row=1, column=1, pady=8, padx=(10, 0))

        self.user_entry.insert(0, "admin")


 

        tk.Label(form, text="Contraseña:", font=("Segoe UI", 10), bg="white").grid(row=2, column=0, sticky="w", pady=8)

        self.pass_entry = ttk.Entry(form, width=28, font=("Segoe UI", 10), show="•")

        self.pass_entry.grid(row=2, column=1, pady=8, padx=(10, 0))


 

        btn = tk.Button(

            form,

            text="🔒 Ingresar",

            font=("Segoe UI", 11, "bold"),

            bg="#2563eb",

            fg="white",

            activebackground="#1d4ed8",

            activeforeground="white",

            relief="flat",

            cursor="hand2",

            command=self._login,

        )

        btn.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(25, 0), ipady=8)


 

        tk.Label(form, text="Usuario de prueba: admin / admin123", font=("Segoe UI", 8), bg="white", fg="#999").grid(

            row=4, column=0, columnspan=2, pady=(15, 0)

        )


 

        self.bind("<Return>", lambda e: self._login())

        self.user_entry.focus()


 

    def _login(self):

        usuario = self.user_entry.get().strip()

        password = self.pass_entry.get().strip()

        if not usuario or not password:

            messagebox.showwarning("Campos requeridos", "Ingrese usuario y contraseña.")

            return

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("SELECT * FROM sistema_usuarios WHERE usuario=? AND password=?", (usuario, password))

        row = cur.fetchone()

        conn.close()

        if row:

            self.destroy()

            self.on_success()

        else:

            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


### main.py

"""

Biblioteca Combarranquilla - Sistema de Gestión

Ejecutar con: python main.py


 

Usuario de prueba: admin

Contraseña:        admin123

"""

from database import init_db

from login_window import LoginWindow

from dashboard import Dashboard



 

def iniciar_dashboard():

    Dashboard().mainloop()



 

if __name__ == "__main__":

    init_db()

    LoginWindow(iniciar_dashboard).mainloop()