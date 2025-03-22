import tkinter as tk
from tkinter import messagebox

def centrar_ventana(ventana, width=400, height=300):
    """ Centra la ventana en la pantalla """
    ventana.withdraw()  # Oculta temporalmente para calcular bien la posición
    ventana.update_idletasks()

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana.geometry(f"{width}x{height}+{x}+{y}")
    ventana.deiconify()  # Muestra la ventana ya centrada


def validar_login(entry_user, entry_pass, login_window, callback):
    USER_CREDENTIALS = {"admin": "1234"}

    usuario = entry_user.get()
    clave = entry_pass.get()
    
    if usuario in USER_CREDENTIALS and USER_CREDENTIALS[usuario] == clave:
        login_window.destroy()
        callback()  # Llama a la función para mostrar el menú
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


def iniciar_login(callback):
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.resizable(False, False)

    # Centrar la ventana de login
    centrar_ventana(login_window, 400, 300)

    bg_color = "#f0f0f0"
    login_window.configure(bg=bg_color)

    tk.Label(login_window, text="Usuario:", bg=bg_color, font=("Helvetica", 12)).pack(pady=10)
    entry_user = tk.Entry(login_window, font=("Helvetica", 12))
    entry_user.pack(pady=5)

    tk.Label(login_window, text="Contraseña:", bg=bg_color, font=("Helvetica", 12)).pack(pady=10)
    entry_pass = tk.Entry(login_window, show="*", font=("Helvetica", 12))
    entry_pass.pack(pady=5)

    tk.Button(login_window, text="Ingresar", 
              command=lambda: validar_login(entry_user, entry_pass, login_window, callback), 
              bg="#007BFF", fg="white", font=("Helvetica", 16), width=20, height=2).pack(pady=20)

    login_window.mainloop()
