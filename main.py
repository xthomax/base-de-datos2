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