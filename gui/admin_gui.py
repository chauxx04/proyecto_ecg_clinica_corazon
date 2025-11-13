"""
admin_gui.py
-----------------------------------
Interfaz del Admin del sistema ECG Clínica del Corazón.
Permite crear, actualizar, eliminar y listar usuarios del sistema.

Los datos se guardan en data/usuarios.json
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json

class AdminWindow:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.users_file = "data/usuarios.json"
        self.current_users = self.load_users()

    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Lista de usuarios
        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'Nombre', 'Rol', 'Documento'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Rol', text='Rol')
        self.tree.heading('Documento', text='Documento')
        self.tree.grid(row=0, column=0, columnspan=4, pady=10)

        # Botones CRUD
        ttk.Button(self.main_frame, text="Crear Usuario", command=self.show_create_window).grid(row=1, column=0, pady=5)
        ttk.Button(self.main_frame, text="Actualizar Usuario", command=self.show_update_window).grid(row=1, column=1, pady=5)
        ttk.Button(self.main_frame, text="Eliminar Usuario", command=self.delete_user).grid(row=1, column=2, pady=5)
        ttk.Button(self.main_frame, text="Refrescar Lista", command=self.refresh_users).grid(row=1, column=3, pady=5)

        self.refresh_users()

    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.current_users, f, indent=4)

    def refresh_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.current_users = self.load_users()
        for user in self.current_users:
            self.tree.insert('', 'end', values=(
                user.get('id', ''),
                user.get('nombre', ''),
                user.get('rol', ''),
                user.get('documento', '')
            ))

    def show_create_window(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Crear Usuario")
        create_window.geometry("300x400")

        ttk.Label(create_window, text="ID:").pack(pady=5)
        id_entry = ttk.Entry(create_window)
        id_entry.pack(pady=5)

        ttk.Label(create_window, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(create_window)
        nombre_entry.pack(pady=5)

        ttk.Label(create_window, text="Documento:").pack(pady=5)
        doc_entry = ttk.Entry(create_window)
        doc_entry.pack(pady=5)

        ttk.Label(create_window, text="Contraseña:").pack(pady=5)
        pass_entry = ttk.Entry(create_window, show="*")
        pass_entry.pack(pady=5)

        ttk.Label(create_window, text="Rol:").pack(pady=5)
        rol_combo = ttk.Combobox(create_window, values=['admin', 'doctor', 'paciente'])
        rol_combo.pack(pady=5)

        def save_user():
            new_user = {
                "id": id_entry.get(),
                "nombre": nombre_entry.get(),
                "documento": doc_entry.get(),
                "password": pass_entry.get(),
                "rol": rol_combo.get()
            }
            
            # Validaciones
            if not all([new_user['id'], new_user['nombre'], new_user['documento'], 
                       new_user['password'], new_user['rol']]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            if any(u['id'] == new_user['id'] for u in self.current_users):
                messagebox.showerror("Error", "El ID ya existe")
                return

            self.current_users.append(new_user)
            self.save_users()
            self.refresh_users()
            create_window.destroy()
            messagebox.showinfo("Éxito", "Usuario creado correctamente")

        ttk.Button(create_window, text="Guardar", command=save_user).pack(pady=20)

    def show_update_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor seleccione un usuario para actualizar")
            return

        user_values = self.tree.item(selected[0])['values']
        user = next((u for u in self.current_users if u['id'] == user_values[0]), None)

        if not user:
            return

        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizar Usuario")
        update_window.geometry("300x400")

        ttk.Label(update_window, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(update_window)
        nombre_entry.insert(0, user['nombre'])
        nombre_entry.pack(pady=5)

        ttk.Label(update_window, text="Documento:").pack(pady=5)
        doc_entry = ttk.Entry(update_window)
        doc_entry.insert(0, user['documento'])
        doc_entry.pack(pady=5)

        ttk.Label(update_window, text="Contraseña:").pack(pady=5)
        pass_entry = ttk.Entry(update_window, show="*")
        pass_entry.insert(0, user['password'])
        pass_entry.pack(pady=5)

        ttk.Label(update_window, text="Rol:").pack(pady=5)
        rol_combo = ttk.Combobox(update_window, values=['admin', 'doctor', 'paciente'])
        rol_combo.set(user['rol'])
        rol_combo.pack(pady=5)

        def update_user():
            user['nombre'] = nombre_entry.get()
            user['documento'] = doc_entry.get()
            user['password'] = pass_entry.get()
            user['rol'] = rol_combo.get()

            if not all([user['nombre'], user['documento'], user['password'], user['rol']]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            self.save_users()
            self.refresh_users()
            update_window.destroy()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")

        ttk.Button(update_window, text="Actualizar", command=update_user).pack(pady=20)

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Por favor seleccione un usuario para eliminar")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):
            return

        user_values = self.tree.item(selected[0])['values']
        self.current_users = [u for u in self.current_users if u['id'] != user_values[0]]
        self.save_users()
        self.refresh_users()
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente")