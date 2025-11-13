"""
login.py
-----------------------------------
Ventana de inicio de sesión para el sistema ECG Clínica del Corazón.
Permite ingresar con usuario y contraseña. Dependiendo del rol
almacenado en usuarios.json, se redirige a la interfaz correspondiente.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from .admin_gui import AdminWindow
from .doctor_gui import DoctorWindow
from .paciente_gui import PacienteWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Usuario
        ttk.Label(frame, text="Usuario:").grid(row=0, column=0, pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Contraseña
        ttk.Label(frame, text="Contraseña:").grid(row=1, column=0, pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Botón login
        ttk.Button(frame, text="Iniciar Sesión", command=self.validate_login).grid(row=2, column=0, columnspan=2, pady=20)

    def validate_login(self):
        usuario = self.username_entry.get()
        contraseña = self.password_entry.get()

        try:
            with open('data/usuarios.json', 'r') as f:
                users = json.load(f)
            
            # Modificado para usar los campos correctos de tu JSON
            user = next((u for u in users if u['usuario'] == usuario and u['contrasena'] == contraseña), None)
            
            if user:
                self.root.withdraw()  # Oculta ventana de login
                new_window = tk.Toplevel()
                new_window.title(f"Clínica del Corazón - {user['rol'].capitalize()}")
                new_window.geometry("800x600")
                
                if user['rol'] == 'admin':
                    AdminWindow(new_window)
                elif user['rol'] == 'doctor':
                        DoctorWindow(new_window, user['usuario'])
                elif user['rol'] == 'paciente':
                        PacienteWindow(new_window, user['usuario'])
                    
                new_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")


    def redirigir(self, rol, usuario):
        """Abre la ventana según el rol."""
        self.root.withdraw()  # Oculta ventana de login

        if rol == "admin":
            nueva_ventana = tk.Toplevel()
            AdminWindow(nueva_ventana, usuario)
        elif rol == "doctor":
            nueva_ventana = tk.Toplevel()
            DoctorWindow(nueva_ventana, rol["usuario"])
        elif rol == "paciente":
            nueva_ventana = tk.Toplevel()
            PacienteWindow(nueva_ventana, rol["usuario"])
        else:
            messagebox.showerror("Error", f"Rol desconocido: {rol}")
            self.root.deiconify()  # Muestra el login de nuevo
